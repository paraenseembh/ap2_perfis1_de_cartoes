"""Scores de anomalia, ensemble de desquantizações e análise do topo."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.neighbors import KernelDensity

import config as C
from preprocessamento import espaco, rng_sorteio
from segmentacao import gmm, hdbscan, kmeans


# ----------------------------------------------------------------------------
# Scores de um sorteio
# ----------------------------------------------------------------------------
def scores_sorteio(df: pd.DataFrame, i: int) -> dict[str, np.ndarray]:
    """Os quatro scores (maior = mais suspeito) no i-ésimo sorteio."""
    X, _ = espaco(df, rng_sorteio(i))
    g = gmm().fit(X)
    kde = KernelDensity(kernel="gaussian", bandwidth=C.banda_scott(len(X))).fit(X)
    km = kmeans().fit(X)
    hdb = hdbscan().fit(X)
    return {
        "GMM": -g.score_samples(X),               # -log p(x)
        "KDE": -kde.score_samples(X),             # -log densidade
        "K-Means": km.transform(X).min(axis=1),   # distância ao centroide mais próximo
        "HDBSCAN": 1.0 - hdb.probabilities_,      # 1 - força de pertinência
    }


def matriz_sorteios(df: pd.DataFrame, n: int = C.N_SORTEIOS_SCORE,
                    verbose: bool = True) -> dict[str, np.ndarray]:
    """Empilha os scores de `n` sorteios: {nome: array (n, n_clientes)}."""
    acc = {k: [] for k in C.NOMES_SCORES}
    for i in range(n):
        s = scores_sorteio(df, i)
        for k in acc:
            acc[k].append(s[k])
        if verbose and (i + 1) % 10 == 0:
            print(f"    sorteio {i + 1}/{n}")
    return {k: np.vstack(v) for k, v in acc.items()}


# ----------------------------------------------------------------------------
# Utilitários de ranking
# ----------------------------------------------------------------------------
def n_top(n_total: int, frac: float = C.TOP) -> int:
    return int(round(frac * n_total))


def top(score: np.ndarray, frac: float = C.TOP) -> np.ndarray:
    """Índices dos `frac` maiores scores (desempate estável pelo índice)."""
    return np.argsort(-score, kind="stable")[: n_top(score.size, frac)]


def jaccard(a, b) -> float:
    a, b = set(map(int, a)), set(map(int, b))
    return len(a & b) / len(a | b) if (a or b) else 1.0


def posicoes(score: np.ndarray) -> np.ndarray:
    """Posição (1 = mais suspeito) de cada cliente."""
    ordem = np.argsort(-score, kind="stable")
    pos = np.empty_like(ordem)
    pos[ordem] = np.arange(1, ordem.size + 1)
    return pos


# ----------------------------------------------------------------------------
# Estabilidade e concordância
# ----------------------------------------------------------------------------
def estabilidade_scores(M: dict[str, np.ndarray]) -> dict:
    """Jaccard do top 2% entre sorteios únicos (pares 2i, 2i+1) e entre dois
    ensembles independentes (primeira x segunda metade dos sorteios)."""
    out = {}
    for nome, S in M.items():
        n = S.shape[0]
        pares = [jaccard(top(S[2 * i]), top(S[2 * i + 1])) for i in range(n // 2)]
        meio = n // 2
        ens = jaccard(top(S[:meio].mean(0)), top(S[meio:].mean(0)))
        out[nome] = {"unico_media": float(np.mean(pares)),
                     "unico_dp": float(np.std(pares, ddof=1)) if len(pares) > 1 else 0.0,
                     "ensemble": float(ens)}
    return out


def concordancia(final: dict[str, np.ndarray], ref: str = "GMM") -> dict:
    out = {}
    for nome, s in final.items():
        out[nome] = {
            "spearman": float(stats.spearmanr(final[ref], s).statistic),
            "jaccard_top": float(jaccard(top(final[ref]), top(s))),
        }
    return out


def consenso(final: dict[str, np.ndarray]) -> tuple[np.ndarray, dict]:
    """Em quantos scores cada cliente está no top 2%."""
    n = next(iter(final.values())).size
    cont = np.zeros(n, dtype=int)
    for s in final.values():
        cont[top(s)] += 1
    resumo = {str(k): int((cont == k).sum()) for k in range(len(final), 0, -1)}
    resumo["uniao"] = int((cont > 0).sum())
    return cont, resumo


# ----------------------------------------------------------------------------
# Análises de negócio sobre o score oficial (GMM)
# ----------------------------------------------------------------------------
def analise_globais(final, mascara_global: np.ndarray, cont: np.ndarray) -> dict:
    pos = posicoes(final["GMM"])
    idx = np.flatnonzero(mascara_global)
    k = n_top(pos.size)
    return {
        "n": int(idx.size),
        "posicoes_gmm": sorted(int(p) for p in pos[idx]),
        "n_no_top_gmm": int((pos[idx] <= k).sum()),
        "n_no_top_dos_quatro": int((cont[idx] == len(final)).sum()),
    }


def analise_grandes_gastadores(df, score_gmm: np.ndarray, perfil: np.ndarray) -> dict:
    k = n_top(score_gmm.size)
    top_valor = np.argsort(-df[C.COL_VALOR].to_numpy(), kind="stable")[:k]
    comuns = sorted(set(top_valor) & set(top(score_gmm)))
    linhas = df.iloc[comuns][[C.COL_ID, C.COL_FREQ, C.COL_TICKET, C.COL_VALOR]].copy()
    linhas["perfil"] = perfil[comuns]
    return {"n_comuns": len(comuns), "clientes": linhas.to_dict(orient="records")}


def analise_limiares(score: np.ndarray, perfil: np.ndarray, ordem_perfis) -> dict:
    limiar_global = np.sort(score)[::-1][n_top(score.size) - 1]
    out = {"global": {}, "por_perfil": {}}
    for p in ordem_perfis:
        m = perfil == p
        out["global"][p] = float(((score >= limiar_global) & m).sum() / m.sum())
        lim_p = np.percentile(score[m], C.PERCENTIL_PERFIL)
        out["por_perfil"][p] = int((score[m] >= lim_p).sum())
    return out
