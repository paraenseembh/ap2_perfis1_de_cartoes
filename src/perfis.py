"""Nomeação e descrição dos perfis de consumo."""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as C

ORDEM = ("Esporádico, ticket baixo", "Esporádico, ticket alto",
         "Frequente, ticket baixo", "Frequente, ticket alto")


def nomear(df: pd.DataFrame, lab: np.ndarray) -> np.ndarray:
    """Dá nome a cada grupo pela mediana de frequência e de ticket."""
    nomes = {}
    for c in np.unique(lab):
        m = lab == c
        f = np.median(df.loc[m, C.COL_FREQ])
        t = np.median(df.loc[m, C.COL_TICKET])
        nome = (("Frequente" if f >= C.CORTE_FREQ else "Esporádico")
                + ", ticket " + ("alto" if t >= C.CORTE_TICKET else "baixo"))
        if nome in nomes.values():          # salvaguarda para K != 4
            nome = f"{nome} ({c})"
        nomes[c] = nome
    return np.array([nomes[c] for c in lab], dtype=object)


def ordem_perfis(perfil: np.ndarray) -> list[str]:
    presentes = list(dict.fromkeys(perfil))
    return [p for p in ORDEM if p in presentes] + sorted(p for p in presentes if p not in ORDEM)


def descrever(df: pd.DataFrame, perfil: np.ndarray) -> list[dict]:
    receita = df[C.COL_VALOR].sum()
    out = []
    for p in ordem_perfis(perfil):
        m = perfil == p
        sub = df[m]
        out.append({
            "perfil": p,
            "n": int(m.sum()),
            "pct_clientes": float(m.mean()),
            "freq_mediana": float(sub[C.COL_FREQ].median()),
            "ticket_mediano": float(sub[C.COL_TICKET].median()),
            "valor_mediano": float(sub[C.COL_VALOR].median()),
            "pct_receita": float(sub[C.COL_VALOR].sum() / receita),
        })
    return out
