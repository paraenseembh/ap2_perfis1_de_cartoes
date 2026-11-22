"""Pipeline completo do artigo: um único script gera todos os números,
tabelas e figuras.

Uso:
    python src/main.py --dados dados/clientes.csv
    python src/main.py --dados dados/clientes.csv --atualizar-artigo
    python src/main.py --dados dados/sintetica.csv --rapido   # teste de fumaça

Por padrão, as saídas vão para resultados/ (tabelas/, figuras/, numeros.json,
relatorio.md). Com --atualizar-artigo, tabelas e figuras são gravadas também
em artigo/tabelas e artigo/figuras, sobrescrevendo as versões do artigo.
"""
from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path

import numpy as np

import config as C
import dados
import figuras
import metricas
import perfis
import scores
import segmentacao as seg
import tabelas
from preprocessamento import espaco, rng_sorteio
from relatorio import escrever_relatorio


def _json(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(type(obj))


def executar(caminho_dados: Path, saida: Path, n_sorteios: int, com_figuras: bool) -> dict:
    t0 = time.time()
    dir_tab, dir_fig = saida / "tabelas", saida / "figuras"
    dir_tab.mkdir(parents=True, exist_ok=True)
    dir_fig.mkdir(parents=True, exist_ok=True)
    R: dict = {"semente": C.SEMENTE, "n_sorteios_score": n_sorteios}

    # ------------------------------------------------------------------ EDA
    print("[1/6] Diagnóstico da base")
    df = dados.carregar(caminho_dados)
    R["eda"] = dados.diagnostico(df)
    mask_global = dados.mascara_vazios(df)
    quad = dados.quadrantes(df)

    # --------------------------------------------------------- segmentação
    print("[2/6] Segmentação: K-Means, GMM/BIC, DBSCAN, HDBSCAN")
    X, _ = espaco(df, rng_sorteio(0))           # espaço final (sorteio base)
    R["kmeans"] = seg.varredura_kmeans(X)
    R["bic"] = seg.varredura_bic(df)
    R["bic_4x5"] = seg.bic4_menos_bic5(df)
    R["gmm_k5"] = seg.componente_extra_k5(df, X)
    R["hdbscan_sens"] = seg.varredura_hdbscan(df)

    curva = seg.curva_kdist(X)
    i_j, eps_j = seg.joelho(curva)
    R["dbscan"] = {"eps_joelho": eps_j, "varredura": seg.varredura_dbscan(X, eps_j)}

    # ----------------------------------------------- comparação de partições
    print("[3/6] Métricas internas e estabilidade (30 subamostras de 80%)")
    fabricas = {
        "K-Means": seg.kmeans,
        "GMM": seg.gmm,
        "DBSCAN": lambda: seg.dbscan(eps_j),
        "HDBSCAN": seg.hdbscan,
    }
    labs, comp = {}, []
    for nome, fab in fabricas.items():
        lab = seg.rotulos(fab(), X)
        labs[nome] = lab
        est = metricas.estabilidade(X, lab, fab)
        comp.append({"metodo": nome, **seg.resumo_rotulos(lab), **metricas.internas(X, lab),
                     "ari_quadrantes": metricas.ari(quad, lab),
                     "estab_media": est["media"], "estab_dp": est["dp"]})
    for r in comp:
        r["K"], r["ruido"] = r.pop("n_grupos"), r.pop("n_ruido")
    R["comparacao"] = comp
    R["ari_entre_metodos"] = {f"{a} x {b}": metricas.ari(labs[a], labs[b])
                              for a in labs for b in labs if a < b}

    perfil = perfis.nomear(df, labs["GMM"])
    ordem = perfis.ordem_perfis(perfil)
    R["perfis"] = perfis.descrever(df, perfil)

    # --------------------------------------------------------------- scores
    print(f"[4/6] Scores de anomalia em {n_sorteios} desquantizações")
    M = scores.matriz_sorteios(df, n_sorteios)
    final = {k: v.mean(axis=0) for k, v in M.items()}
    R["estab_scores"] = scores.estabilidade_scores(M)
    R["concordancia"] = scores.concordancia(final)
    cont, R["consenso"] = scores.consenso(final)
    R["globais"] = scores.analise_globais(final, mask_global, cont)
    R["grandes_gastadores"] = scores.analise_grandes_gastadores(df, final["GMM"], perfil)
    R["limiares"] = scores.analise_limiares(final["GMM"], perfil, ordem)

    ordem_top = np.argsort(-final["GMM"], kind="stable")[: C.N_TOP_TABELA]
    R["top10"] = [{"id": df.at[i, C.COL_ID], "freq": int(df.at[i, C.COL_FREQ]),
                   "ticket": float(df.at[i, C.COL_TICKET]), "perfil": perfil[i],
                   "score": float(final["GMM"][i]), "consenso": int(cont[i])}
                  for i in ordem_top]

    # -------------------------------------------------------------- tabelas
    print("[5/6] Tabelas LaTeX")
    tabelas.comparacao(comp, dir_tab / "comparacao.tex")
    tabelas.estabilidade_scores(R["estab_scores"], R["concordancia"],
                                dir_tab / "estab_scores.tex", C.NOMES_SCORES)
    tabelas.perfis(R["perfis"], dir_tab / "perfis.tex")
    tabelas.suspeitos(R["top10"], dir_tab / "suspeitos.tex", len(C.NOMES_SCORES))

    # -------------------------------------------------------------- figuras
    if com_figuras:
        print("[6/6] Figuras")
        figuras.f1_estrutura(df, dir_fig / "f1_estrutura.pdf")
        figuras.f2_bic(R["bic"], dir_fig / "f2_bic.pdf")
        figuras.f3_kdist(curva, i_j, eps_j, dir_fig / "f3_kdist.pdf")
        modelo = seg.gmm().fit(X)
        figuras.f4_gmm(X, modelo, modelo.predict(X), scores.top(final["GMM"]),
                       dir_fig / "f4_gmm.pdf")
        figuras.f5_score(final["GMM"], dir_fig / "f5_score.pdf")

    # ------------------------------------------------------------- saídas
    np.savetxt(saida / "scores_finais.csv",
               np.column_stack([final[k] for k in C.NOMES_SCORES]),
               delimiter=",", header=",".join(C.NOMES_SCORES), comments="")
    (saida / "ids_e_perfis.csv").write_text(
        "id_cliente,perfil,consenso\n"
        + "\n".join(f"{i},\"{p}\",{c}" for i, p, c in zip(df[C.COL_ID], perfil, cont))
        + "\n", encoding="utf-8")
    R["tempo_s"] = round(time.time() - t0, 1)
    (saida / "numeros.json").write_text(
        json.dumps(R, ensure_ascii=False, indent=2, default=_json), encoding="utf-8")
    escrever_relatorio(R, saida / "relatorio.md")
    print(f"Concluído em {R['tempo_s']} s. Saídas em {saida}")
    return R


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dados", type=Path, default=C.DADOS_PADRAO, help="CSV da base")
    ap.add_argument("--saida", type=Path, default=C.DIR_RESULTADOS)
    ap.add_argument("--rapido", action="store_true",
                    help="usa 10 sorteios no score (só para teste; não reproduz o artigo)")
    ap.add_argument("--sem-figuras", action="store_true")
    ap.add_argument("--atualizar-artigo", action="store_true",
                    help="copia tabelas e figuras para artigo/")
    a = ap.parse_args()

    n = 10 if a.rapido else C.N_SORTEIOS_SCORE
    executar(a.dados, a.saida, n, not a.sem_figuras)

    if a.atualizar_artigo:
        for sub in ("tabelas", "figuras"):
            for arq in (a.saida / sub).iterdir():
                shutil.copy2(arq, C.DIR_ARTIGO / sub / arq.name)
        print("Tabelas e figuras copiadas para artigo/.")


if __name__ == "__main__":
    main()
