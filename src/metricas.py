"""Qualidade interna e estabilidade das partições."""
from __future__ import annotations

from typing import Callable

import numpy as np
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score,
                             davies_bouldin_score, silhouette_score)

import config as C


def internas(X: np.ndarray, lab: np.ndarray) -> dict:
    """Silhueta, Davies-Bouldin e Calinski-Harabasz, sem os pontos de ruído."""
    m = lab != -1
    if len(set(lab[m])) < 2:
        return {"silhueta": float("nan"), "db": float("nan"), "ch": float("nan")}
    return {
        "silhueta": float(silhouette_score(X[m], lab[m])),
        "db": float(davies_bouldin_score(X[m], lab[m])),
        "ch": float(calinski_harabasz_score(X[m], lab[m])),
    }


def estabilidade(X: np.ndarray, lab_completo: np.ndarray,
                 fabrica: Callable[[], object]) -> dict:
    """ARI entre o modelo ajustado em subamostras de 80% e o modelo completo,
    restrito aos pontos da subamostra."""
    rng = np.random.default_rng(C.SEMENTE)
    n = X.shape[0]
    m = int(round(C.FRACAO_SUBAMOSTRA * n))
    aris = []
    for _ in range(C.N_SUBAMOSTRAS):
        idx = rng.choice(n, size=m, replace=False)
        lab_sub = np.asarray(fabrica().fit_predict(X[idx]))
        aris.append(adjusted_rand_score(lab_completo[idx], lab_sub))
    return {"media": float(np.mean(aris)), "dp": float(np.std(aris, ddof=1))}


def ari(a: np.ndarray, b: np.ndarray) -> float:
    return float(adjusted_rand_score(a, b))
