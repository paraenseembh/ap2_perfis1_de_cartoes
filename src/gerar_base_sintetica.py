"""Gera uma base SINTÉTICA com o mesmo esquema da base do artigo.

ATENÇÃO: esta base NÃO é a base analisada no artigo. Ela serve apenas para
testar o pipeline (teste de fumaça) quando a base original não está
disponível. Os números obtidos com ela não correspondem aos do artigo.

Uso:
    python src/gerar_base_sintetica.py --saida dados/sintetica.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# (fração, faixa de frequência, mediana do ticket, dispersão log do ticket)
BLOCOS = [
    (0.34, (2, 7), 35.0, 0.25),     # esporádico, ticket baixo
    (0.21, (2, 7), 450.0, 0.15),    # esporádico, ticket alto
    (0.25, (25, 70), 30.0, 0.25),   # frequente, ticket baixo
    (0.20, (25, 70), 350.0, 0.15),  # frequente, ticket alto
]


def gerar(n: int = 3000, semente: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(semente)
    freq, ticket = [], []
    for frac, (fmin, fmax), med, dp in BLOCOS:
        m = int(round(frac * n))
        freq.append(rng.integers(fmin, fmax + 1, size=m))
        ticket.append(np.exp(rng.normal(np.log(med), dp, size=m)))
    freq, ticket = np.concatenate(freq)[:n], np.concatenate(ticket)[:n]
    # alguns pontos nos vazios (anomalias globais) e duplicatas (coletivas)
    freq[:2], ticket[:4] = [12, 15], [70.0, 120.0, 200.0, 90.0]
    ticket = np.round(ticket, 2)
    df = pd.DataFrame({
        "id_cliente": [f"C{i:06d}" for i in range(n)],
        "valor_total_gasto": np.round(freq * ticket, 2),
        "frequencia_compras": freq,
        "ticket_medio": ticket,
    })
    df.iloc[-5:, 1:] = df.iloc[-10:-5, 1:].to_numpy()
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", type=Path, default=Path("dados/sintetica.csv"))
    ap.add_argument("--n", type=int, default=3000)
    a = ap.parse_args()
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    gerar(a.n).to_csv(a.saida, index=False)
    print(f"Base sintética gravada em {a.saida}")
