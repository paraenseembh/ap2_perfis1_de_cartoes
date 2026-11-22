"""Algoritmos de segmentação: K-Means, GMM (EM), DBSCAN e HDBSCAN."""
from __future__ import annotations

import numpy as np
from sklearn.cluster import DBSCAN, HDBSCAN, KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors

import config as C
from preprocessamento import espaco, rng_sorteio


# ----------------------------------------------------------------------------
# Construtores (usados também na análise de estabilidade)
# ----------------------------------------------------------------------------
def kmeans(k: int = C.K_FINAL) -> KMeans:
    return KMeans(n_clusters=k, n_init=C.N_INIT, random_state=C.SEMENTE)


def gmm(k: int = C.K_FINAL, cov: str = "full") -> GaussianMixture:
    return GaussianMixture(n_components=k, covariance_type=cov, n_init=C.N_INIT,
                           random_state=C.SEMENTE)


def dbscan(eps: float) -> DBSCAN:
    return DBSCAN(eps=eps, min_samples=C.MIN_PTS)


def hdbscan(mcs: int = C.HDBSCAN_MCS_FINAL) -> HDBSCAN:
    return HDBSCAN(min_cluster_size=mcs, copy=True)


def rotulos(modelo, X: np.ndarray) -> np.ndarray:
    """Ajusta e devolve os rótulos (GMM não tem fit_predict com ruído)."""
    return np.asarray(modelo.fit_predict(X))


# ----------------------------------------------------------------------------
# K-Means: cotovelo + silhueta
# ----------------------------------------------------------------------------
def varredura_kmeans(X: np.ndarray) -> dict:
    out = {"K": [], "inercia": [], "silhueta": []}
    for k in C.K_KMEANS:
        km = kmeans(k).fit(X)
        out["K"].append(k)
        out["inercia"].append(float(km.inertia_))
        out["silhueta"].append(float(silhouette_score(X, km.labels_)))
    out["K_melhor_silhueta"] = int(out["K"][int(np.argmax(out["silhueta"]))])
    return out


# ----------------------------------------------------------------------------
# GMM: BIC por K e por tipo de covariância
# ----------------------------------------------------------------------------
def curva_bic(X: np.ndarray, cov: str) -> list[float]:
    return [float(gmm(k, cov).fit(X).bic(X)) for k in C.K_GMM]


def varredura_bic(df) -> dict:
    X_disc, _ = espaco(df, None)
    X_deq, _ = espaco(df, rng_sorteio(0))
    out = {"K": list(C.K_GMM), "discreta": {}, "desquantizada": {}}
    for cov in C.COVARIANCIAS:
        for nome, X in (("discreta", X_disc), ("desquantizada", X_deq)):
            bics = curva_bic(X, cov)
            out[nome][cov] = {"bic": bics, "K_min": int(C.K_GMM[int(np.argmin(bics))])}
    return out


def bic4_menos_bic5(df) -> dict:
    """Instabilidade da escolha 4 x 5 entre sorteios da desquantização."""
    difs, escolhas = [], []
    for i in range(C.N_SORTEIOS_BIC):
        X, _ = espaco(df, rng_sorteio(i))
        b = {k: gmm(k).fit(X).bic(X) for k in C.K_GMM}
        difs.append(float(b[4] - b[5]))
        escolhas.append(int(min(b, key=b.get)))
    return {
        "dif_bic4_bic5": difs,
        "min": float(min(difs)), "max": float(max(difs)),
        "K_escolhido": escolhas,
        "n_K4": int(sum(k == 4 for k in escolhas)),
        "n_K5": int(sum(k == 5 for k in escolhas)),
    }


def componente_extra_k5(df, X: np.ndarray) -> dict:
    """Descreve a componente que o K=5 acrescenta (piso de 2 compras)."""
    lab5 = rotulos(gmm(5), X)
    f = df[C.COL_FREQ].to_numpy()
    perfis = []
    for c in np.unique(lab5):
        m = lab5 == c
        perfis.append({"componente": int(c), "n": int(m.sum()),
                       "freq_min": int(f[m].min()), "freq_max": int(f[m].max()),
                       "frac_freq_2": float((f[m] == f.min()).mean())})
    n_piso = int((f == f.min()).sum())
    sil5 = float(silhouette_score(X, lab5))
    return {"componentes": perfis, "n_clientes_freq_minima": n_piso, "silhueta_K5": sil5}


# ----------------------------------------------------------------------------
# DBSCAN: joelho da k-distância e varredura de eps
# ----------------------------------------------------------------------------
def curva_kdist(X: np.ndarray, k: int = C.MIN_PTS) -> np.ndarray:
    """Distância ao k-ésimo vizinho (contando o próprio ponto, como no
    critério de ponto-núcleo do scikit-learn), em ordem crescente."""
    dist, _ = NearestNeighbors(n_neighbors=k).fit(X).kneighbors(X)
    return np.sort(dist[:, -1])


def joelho(curva: np.ndarray) -> tuple[int, float]:
    """Ponto de maior distância à corda que liga o primeiro ao último ponto."""
    n = curva.size
    x = np.arange(n, dtype=float)
    p1 = np.array([0.0, curva[0]])
    p2 = np.array([n - 1.0, curva[-1]])
    d = p2 - p1
    d /= np.linalg.norm(d)
    vec = np.column_stack([x, curva]) - p1
    proj = np.outer(vec @ d, d)
    dist = np.linalg.norm(vec - proj, axis=1)
    i = int(np.argmax(dist))
    return i, float(curva[i])


def resumo_rotulos(lab: np.ndarray) -> dict:
    return {"n_grupos": int(len(set(lab)) - (1 if -1 in lab else 0)),
            "n_ruido": int((lab == -1).sum())}


def varredura_dbscan(X: np.ndarray, eps_joelho: float) -> list[dict]:
    out = []
    for eps in sorted({round(eps_joelho, 3), *C.EPS_GRADE}):
        lab = rotulos(dbscan(eps), X)
        out.append({"eps": float(eps), **resumo_rotulos(lab)})
    return out


# ----------------------------------------------------------------------------
# HDBSCAN: sensibilidade a min_cluster_size, discreto x desquantizado
# ----------------------------------------------------------------------------
def varredura_hdbscan(df) -> dict:
    X_disc, _ = espaco(df, None)
    X_deq, _ = espaco(df, rng_sorteio(0))
    out = {"min_cluster_size": list(C.HDBSCAN_MCS), "discreta": [], "desquantizada": []}
    for mcs in C.HDBSCAN_MCS:
        out["discreta"].append(resumo_rotulos(rotulos(hdbscan(mcs), X_disc)))
        out["desquantizada"].append(resumo_rotulos(rotulos(hdbscan(mcs), X_deq)))
    return out
