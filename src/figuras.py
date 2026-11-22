"""Figuras f1-f5 do artigo."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402

import config as C  # noqa: E402

TAM = (6.0, 3.6)
CORES = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b", "#e377c2"]


def _salvar(fig, destino: Path) -> None:
    fig.tight_layout()
    fig.savefig(destino, bbox_inches="tight")
    plt.close(fig)


def f1_estrutura(df, destino: Path) -> None:
    fig, ax = plt.subplots(figsize=TAM)
    ax.scatter(df[C.COL_FREQ], df[C.COL_TICKET], s=5, alpha=0.4, color="0.3", lw=0)
    ax.axvline(C.CORTE_FREQ, ls="--", lw=0.8, color="0.6")
    ax.axhline(C.CORTE_TICKET, ls="--", lw=0.8, color="0.6")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Frequência de compras (log)")
    ax.set_ylabel("Ticket médio, R$ (log)")
    _salvar(fig, destino)


def f2_bic(bic: dict, destino: Path, cov: str = "full") -> None:
    fig, ax = plt.subplots(figsize=TAM)
    K = bic["K"]
    for nome, cor, mk in (("discreta", CORES[0], "o"), ("desquantizada", CORES[1], "s")):
        y = bic[nome][cov]["bic"]
        ax.plot(K, y, marker=mk, color=cor, label=f"Frequência {nome}")
        kmin = bic[nome][cov]["K_min"]
        ax.scatter([kmin], [y[K.index(kmin)]], s=120, facecolors="none", edgecolors=cor, lw=1.5)
    ax.set_xlabel("Número de componentes $K$")
    ax.set_ylabel(f"BIC (covariância {cov})")
    ax.legend(frameon=False)
    _salvar(fig, destino)


def f3_kdist(curva: np.ndarray, i_joelho: int, eps: float, destino: Path) -> None:
    fig, ax = plt.subplots(figsize=TAM)
    ax.plot(np.arange(curva.size), curva, color=CORES[0], lw=1.2)
    ax.axhline(eps, ls="--", lw=0.8, color="0.5")
    ax.scatter([i_joelho], [eps], color="crimson", zorder=3,
               label=fr"joelho: $\varepsilon$ = {eps:.3f}".replace(".", ","))
    ax.set_xlabel("Pontos ordenados")
    ax.set_ylabel(f"Distância ao {C.MIN_PTS}º vizinho")
    ax.legend(frameon=False)
    _salvar(fig, destino)


def _elipse(ax, media, cov, n_dp, cor):
    vals, vecs = np.linalg.eigh(cov)
    ordem = vals.argsort()[::-1]
    vals, vecs = vals[ordem], vecs[:, ordem]
    ang = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    w, h = 2 * n_dp * np.sqrt(vals)
    ax.add_patch(Ellipse(media, w, h, angle=ang, fill=False, color=cor,
                         lw=1.0, ls="-" if n_dp == 2 else ":"))


def f4_gmm(X: np.ndarray, modelo, lab: np.ndarray, idx_top: np.ndarray, destino: Path) -> None:
    fig, ax = plt.subplots(figsize=TAM)
    for j, c in enumerate(np.unique(lab)):
        m = lab == c
        ax.scatter(X[m, 0], X[m, 1], s=4, alpha=0.35, color=CORES[j % len(CORES)], lw=0)
    for j in range(modelo.n_components):
        for n_dp in (2, 3):
            _elipse(ax, modelo.means_[j], modelo.covariances_[j], n_dp, CORES[j % len(CORES)])
    ax.scatter(X[idx_top, 0], X[idx_top, 1], s=22, marker="x", color="crimson", lw=1.0,
               label=f"top {C.TOP:.0%} do score ({idx_top.size} clientes)".replace(".", ","))
    ax.set_xlabel(r"$\log \tilde f$ (padronizado)")
    ax.set_ylabel(r"$\log t$ (padronizado)")
    ax.legend(frameon=False, loc="best", markerscale=1.5)
    _salvar(fig, destino)


def f5_score(score: np.ndarray, destino: Path) -> None:
    fig, ax = plt.subplots(figsize=TAM)
    ax.hist(score, bins=60, color="0.6", edgecolor="white", lw=0.3)
    for frac, ls in ((0.01, "-"), (0.02, "--"), (0.05, ":")):
        lim = np.quantile(score, 1 - frac)
        ax.axvline(lim, color="crimson", ls=ls, lw=1.0, label=f"top {frac:.0%}")
    ax.set_xlabel(r"Score GMM, $-\log p(x)$ (média dos sorteios)")
    ax.set_ylabel("Clientes")
    ax.legend(frameon=False)
    _salvar(fig, destino)
