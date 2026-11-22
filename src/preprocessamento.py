"""Construção do espaço de modelagem x = (log f~, log t), padronizado.

O valor total é descartado da modelagem porque é exatamente freq x ticket
(redundância linear em log) e é usado só na interpretação.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

import config as C


def desquantizar(freq: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Soma ruído U(-0,5; 0,5) à contagem inteira (Theis et al., 2016)."""
    return freq + rng.uniform(-0.5, 0.5, size=freq.shape)


def espaco_log(df: pd.DataFrame, rng: np.random.Generator | None = None) -> np.ndarray:
    """Matriz (n, 2) em log. Se `rng` é None, usa a frequência discreta."""
    f = df[C.COL_FREQ].to_numpy(float)
    if rng is not None:
        f = desquantizar(f, rng)
    t = df[C.COL_TICKET].to_numpy(float)
    return np.column_stack([np.log(f), np.log(t)])


def espaco(df: pd.DataFrame, rng: np.random.Generator | None = None):
    """Retorna (X padronizado, scaler). `rng=None` -> frequência discreta."""
    Xlog = espaco_log(df, rng)
    scaler = StandardScaler().fit(Xlog)
    return scaler.transform(Xlog), scaler


def rng_sorteio(i: int) -> np.random.Generator:
    """Gerador do i-ésimo sorteio de desquantização (i = 0 é o sorteio base)."""
    return np.random.default_rng(C.SEMENTE + i)
