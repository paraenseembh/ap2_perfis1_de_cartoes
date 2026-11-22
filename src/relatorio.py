"""Relatório em Markdown com os números citados no texto do artigo,
na ordem em que aparecem, para conferência manual."""
from __future__ import annotations

from pathlib import Path

from tabelas import br


def escrever_relatorio(R: dict, destino: Path) -> None:
    e, km, bic, b45 = R["eda"], R["kmeans"], R["bic"], R["bic_4x5"]
    L = ["# Relatório de números do artigo", "",
         f"Semente {R['semente']}; {R['n_sorteios_score']} sorteios de desquantização no score.", ""]

    L += ["## Seção 4 — Base de dados", "",
          f"- Clientes: {e['n_clientes']}; nulos: {e['n_nulos']}; ids repetidos: {e['n_ids_duplicados']}",
          f"- Valores idênticos: {e['n_clientes_valores_identicos']} clientes em "
          f"{e['n_grupos_valores_identicos']} grupos",
          f"- Erro máximo |ticket − valor/freq|: {e['erro_max_ticket_vs_valor_sobre_freq']:.4f}",
          "- PCA (3 variáveis em log): " + ", ".join(f"{100*v:.1f}%" for v in e["pca_log_var_explicada"]),
          f"- Assimetria do valor total: {e['assimetria_valor_bruto']:.2f} (bruto) → "
          f"{e['assimetria_valor_log']:.2f} (log)",
          f"- Clientes no vazio de frequência: {e['n_clientes_vazio_freq']}; "
          f"no vazio de ticket: {e['n_clientes_vazio_ticket']}; anomalias globais: {e['n_anomalias_globais']}",
          f"- Spearman(freq, ticket): {e['spearman_freq_ticket']:.3f}",
          f"- IQR (bruto) no valor total: {e['outliers_iqr']['bruto']['valor']}; "
          f"MAD (bruto) na frequência: {e['outliers_mad']['bruto']['freq']}",
          f"- IQR/MAD em log: {e['outliers_iqr']['log']} / {e['outliers_mad']['log']}",
          f"- Valores distintos de frequência: {e['n_valores_freq']} (mínimo {e['freq_min']})", ""]

    ine = dict(zip(km["K"], km["inercia"]))
    L += ["## Seção 6.1 — Segmentação", "",
          f"- K-Means: inércia K=3 {br(ine[3],1)}, K=4 {br(ine[4],1)}, K=5 {br(ine[5],1)}; "
          f"silhueta máxima em K={km['K_melhor_silhueta']} ({br(max(km['silhueta']))})",
          "- BIC (K mínimo): " + "; ".join(
              f"{cov}: discreta K={bic['discreta'][cov]['K_min']}, desquantizada K={bic['desquantizada'][cov]['K_min']}"
              for cov in bic["discreta"]),
          f"- BIC4 − BIC5 em {len(b45['dif_bic4_bic5'])} sorteios: de {br(b45['min'],1)} a {br(b45['max'],1)}; "
          f"K=4 em {b45['n_K4']}, K=5 em {b45['n_K5']}",
          f"- Clientes com a frequência mínima: {R['gmm_k5']['n_clientes_freq_minima']}; "
          f"silhueta K=5: {br(R['gmm_k5']['silhueta_K5'])}",
          "- HDBSCAN (grupos) discreta: " + ", ".join(str(r["n_grupos"]) for r in R["hdbscan_sens"]["discreta"])
          + " | desquantizada: " + ", ".join(f"{r['n_grupos']} (ruído {r['n_ruido']})"
                                              for r in R["hdbscan_sens"]["desquantizada"]),
          f"- DBSCAN: ε do joelho = {R['dbscan']['eps_joelho']:.3f}",
          ""]
    L += ["| ε | grupos | ruído |", "|---|---|---|"]
    L += [f"| {r['eps']:.3f} | {r['n_grupos']} | {r['n_ruido']} |" for r in R["dbscan"]["varredura"]]
    L += ["", "| Método | K | Ruído | Silh. | DB | CH | ARI quadr. | Estab. |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| {r['metodo']} | {r['K']} | {r['ruido']} | {r['silhueta']:.3f} | {r['db']:.3f} | "
          f"{r['ch']:.1f} | {r['ari_quadrantes']:.3f} | {r['estab_media']:.3f} ± {r['estab_dp']:.3f} |"
          for r in R["comparacao"]]
    L += ["", "| Perfil | n | % clientes | % receita |", "|---|---|---|---|"]
    L += [f"| {p['perfil']} | {p['n']} | {100*p['pct_clientes']:.1f}% | {100*p['pct_receita']:.1f}% |"
          for p in R["perfis"]]

    c, s, g = R["concordancia"], R["estab_scores"], R["globais"]
    L += ["", "## Seção 6.2 — Anomalias", "",
          "- Spearman com GMM: " + ", ".join(f"{k} {v['spearman']:.3f}" for k, v in c.items() if k != "GMM"),
          "- Jaccard top 2% com GMM: " + ", ".join(f"{k} {v['jaccard_top']:.3f}" for k, v in c.items() if k != "GMM"),
          "- Estabilidade (único / ensemble): " + "; ".join(
              f"{k} {v['unico_media']:.3f}±{v['unico_dp']:.3f} / {v['ensemble']:.3f}" for k, v in s.items()),
          f"- Anomalias globais no top 2% do GMM: {g['n_no_top_gmm']}/{g['n']} "
          f"(posições {g['posicoes_gmm']}); no top dos quatro: {g['n_no_top_dos_quatro']}",
          f"- Top 60 em valor total ∩ top 2% GMM: {R['grandes_gastadores']['n_comuns']}",
          "- Taxa de alerta com limiar global: " + ", ".join(
              f"{k} {100*v:.1f}%" for k, v in R["limiares"]["global"].items()),
          "- Alertas com limiar P98 por perfil: " + ", ".join(
              f"{k} {v}" for k, v in R["limiares"]["por_perfil"].items()),
          "- Consenso (nº de scores com o cliente no top 2%): " + ", ".join(
              f"{k}: {v}" for k, v in R["consenso"].items()), ""]
    L += ["| Cliente | Freq. | Ticket | Perfil | Score | Cons. |", "|---|---|---|---|---|---|"]
    L += [f"| {r['id']} | {r['freq']} | {r['ticket']:.2f} | {r['perfil']} | {r['score']:.2f} | {r['consenso']}/4 |"
          for r in R["top10"]]
    destino.write_text("\n".join(L) + "\n", encoding="utf-8")
