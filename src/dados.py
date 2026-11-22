"""Carga da base e diagnóstico exploratório (Seção 4 do artigo)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import config as C


def carregar(caminho) -> pd.DataFrame:
    """Lê o CSV e valida o esquema esperado."""
    caminho = str(caminho)
    df = pd.read_excel(caminho) if caminho.lower().endswith((".xlsx", ".xls")) \
        else pd.read_csv(caminho)
    faltando = [c for c in C.COLUNAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes na base: {faltando}")
    df = df[list(C.COLUNAS)].copy()
    df[C.COL_FREQ] = df[C.COL_FREQ].astype(int)
    if (df[C.COL_FREQ] <= 0).any() or (df[C.COL_TICKET] <= 0).any():
        raise ValueError("Frequência e ticket devem ser positivos (log é aplicado).")
    return df.reset_index(drop=True)


def _flags_iqr(x: np.ndarray) -> int:
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    return int(((x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)).sum())


def _flags_mad(x: np.ndarray, limiar: float = C.LIMIAR_MAD) -> int:
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    if mad == 0:
        return 0
    z = 0.6745 * (x - med) / mad
    return int((np.abs(z) > limiar).sum())


def mascara_vazios(df: pd.DataFrame) -> np.ndarray:
    """Clientes que caem nos vazios entre os blocos (anomalias globais)."""
    f, t = df[C.COL_FREQ].to_numpy(), df[C.COL_TICKET].to_numpy()
    em_f = (f >= C.VAZIO_FREQ[0]) & (f <= C.VAZIO_FREQ[1])
    em_t = (t > C.VAZIO_TICKET[0]) & (t < C.VAZIO_TICKET[1])
    return em_f | em_t


def quadrantes(df: pd.DataFrame) -> np.ndarray:
    """Quadrantes descritivos (cortes em 20 compras e R$ 150)."""
    alta_f = (df[C.COL_FREQ] >= C.CORTE_FREQ).to_numpy().astype(int)
    alto_t = (df[C.COL_TICKET] >= C.CORTE_TICKET).to_numpy().astype(int)
    return 2 * alta_f + alto_t


def diagnostico(df: pd.DataFrame) -> dict:
    """Reproduz todos os números da Seção 'Base de Dados e Pré-processamento'."""
    v = df[C.COL_VALOR].to_numpy(float)
    f = df[C.COL_FREQ].to_numpy(float)
    t = df[C.COL_TICKET].to_numpy(float)
    trio = [C.COL_VALOR, C.COL_FREQ, C.COL_TICKET]

    dup_mask = df.duplicated(subset=trio, keep=False)
    n_grupos_dup = int(df[dup_mask].groupby(trio).ngroups)

    logs = np.log(np.column_stack([v, f, t]))
    pca = PCA().fit(StandardScaler().fit_transform(logs))

    vazio_f = (f >= C.VAZIO_FREQ[0]) & (f <= C.VAZIO_FREQ[1])
    vazio_t = (t > C.VAZIO_TICKET[0]) & (t < C.VAZIO_TICKET[1])

    return {
        "n_clientes": int(len(df)),
        "n_nulos": int(df.isna().sum().sum()),
        "n_ids_duplicados": int(df[C.COL_ID].duplicated().sum()),
        "n_clientes_valores_identicos": int(dup_mask.sum()),
        "n_grupos_valores_identicos": n_grupos_dup,
        "erro_max_ticket_vs_valor_sobre_freq": float(np.max(np.abs(t - v / f))),
        "pca_log_var_explicada": [float(x) for x in pca.explained_variance_ratio_],
        "assimetria_valor_bruto": float(stats.skew(v)),
        "assimetria_valor_log": float(stats.skew(np.log(v))),
        "n_clientes_vazio_freq": int(vazio_f.sum()),
        "n_clientes_vazio_ticket": int(vazio_t.sum()),
        "n_anomalias_globais": int((vazio_f | vazio_t).sum()),
        "spearman_freq_ticket": float(stats.spearmanr(f, t).statistic),
        "n_valores_freq": int(np.unique(f).size),
        "freq_min": int(f.min()),
        "outliers_iqr": {
            "bruto": {"valor": _flags_iqr(v), "freq": _flags_iqr(f), "ticket": _flags_iqr(t)},
            "log": {"valor": _flags_iqr(np.log(v)), "freq": _flags_iqr(np.log(f)),
                    "ticket": _flags_iqr(np.log(t))},
        },
        "outliers_mad": {
            "bruto": {"valor": _flags_mad(v), "freq": _flags_mad(f), "ticket": _flags_mad(t)},
            "log": {"valor": _flags_mad(np.log(v)), "freq": _flags_mad(np.log(f)),
                    "ticket": _flags_mad(np.log(t))},
        },
    }
