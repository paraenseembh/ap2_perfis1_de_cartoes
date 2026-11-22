"""Configuração central do experimento.

Todos os hiperparâmetros citados na Metodologia do artigo estão aqui, para que
qualquer alteração fique explícita e rastreável.
"""
from pathlib import Path

# ----------------------------------------------------------------------------
# Caminhos
# ----------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[1]
DADOS_PADRAO = RAIZ / "dados" / "clientes.csv"
DIR_ARTIGO = RAIZ / "artigo"
DIR_RESULTADOS = RAIZ / "resultados"

# ----------------------------------------------------------------------------
# Colunas esperadas na base
# ----------------------------------------------------------------------------
COL_ID = "id_cliente"
COL_VALOR = "valor_total_gasto"
COL_FREQ = "frequencia_compras"
COL_TICKET = "ticket_medio"
COLUNAS = (COL_ID, COL_VALOR, COL_FREQ, COL_TICKET)

# ----------------------------------------------------------------------------
# Reprodutibilidade
# ----------------------------------------------------------------------------
SEMENTE = 42

# ----------------------------------------------------------------------------
# Análise exploratória
# ----------------------------------------------------------------------------
LIMIAR_MAD = 3.5               # z-score robusto (Iglewicz & Hoaglin)
VAZIO_FREQ = (8, 24)           # vazio de frequência: 8 <= f <= 24 (inclusivo)
VAZIO_TICKET = (60.0, 220.0)   # vazio entre blocos de ticket (exclusivo)
CORTE_FREQ = 20                # cortes dos quadrantes descritivos
CORTE_TICKET = 150.0

# ----------------------------------------------------------------------------
# Segmentação
# ----------------------------------------------------------------------------
K_KMEANS = list(range(2, 9))               # K = 2..8
K_GMM = list(range(1, 9))                  # K = 1..8
COVARIANCIAS = ("full", "diag", "spherical")
K_FINAL = 4
N_INIT = 10                                # reinicializações de K-Means/GMM
N_SORTEIOS_BIC = 10                        # sorteios para BIC_4 - BIC_5

MIN_PTS = 4                                # heurística 2d (d = 2)
EPS_GRADE = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

HDBSCAN_MCS = (10, 20, 40, 80)
HDBSCAN_MCS_FINAL = 40

# Estabilidade da partição
N_SUBAMOSTRAS = 30
FRACAO_SUBAMOSTRA = 0.8

# ----------------------------------------------------------------------------
# Scores de anomalia
# ----------------------------------------------------------------------------
N_SORTEIOS_SCORE = 60          # 60 desquantizações -> 30 pares / 2 ensembles de 30
TOP = 0.02                     # top 2% (60 de 3.000 clientes)
PERCENTIL_PERFIL = 98          # limiar por perfil
N_TOP_TABELA = 10


def banda_scott(n: int, d: int = 2) -> float:
    """Regra de Scott para KDE em dados padronizados: h = n^(-1/(d+4))."""
    return float(n ** (-1.0 / (d + 4)))


NOMES_SCORES = ("GMM", "KDE", "K-Means", "HDBSCAN")
