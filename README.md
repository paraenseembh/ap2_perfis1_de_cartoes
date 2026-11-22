# Detectando o anômalo pelo perfil

**Introdução ao aprendizado não supervisionado com dados de compra sem rótulos**

Trabalho da disciplina Aprendizado de Máquina II — Bacharelado em Ciência de Dados e
Inteligência Artificial, PUC Minas (2026/2).

Autores: Lucas Rafael Nascimento, Maria Vitoria Manhães, Rafael Cabral e Tainara Almeida.

## Resumo

Analisamos 3.000 perfis de clientes, sem rótulos, de uma operadora de pagamentos simulada,
para segmentar o consumo e priorizar clientes suspeitos de fraude. K-Means, GMM e HDBSCAN
recuperam a mesma partição em quatro perfis; a diferença entre eles está no **score de
anomalia**. O GMM com frequência desquantizada e score $-\log p(x)$ médio sobre 60
desquantizações foi o score mais estável (Jaccard do top 2% de 0,664 em execução única e
0,967 em ensemble).

## Estrutura do repositório

```
.
├── artigo/                  # fonte LaTeX do artigo (padrão SBC)
│   ├── main.tex
│   ├── referencias.bib
│   ├── sbc-template.sty, sbc.bst
│   ├── figuras/             # f1–f5 (PDF), geradas por src/main.py
│   └── tabelas/             # corpos das tabelas (.tex), gerados por src/main.py
├── src/                     # código dos experimentos
│   ├── config.py            # todos os hiperparâmetros e caminhos
│   ├── dados.py             # carga, validação e diagnóstico exploratório
│   ├── preprocessamento.py  # desquantização e espaço (log f~, log t) padronizado
│   ├── segmentacao.py       # K-Means, GMM/BIC, DBSCAN (k-distância), HDBSCAN
│   ├── metricas.py          # silhueta, DB, CH, ARI e estabilidade por subamostragem
│   ├── scores.py            # scores de anomalia, ensemble, Jaccard, consenso, limiares
│   ├── perfis.py            # nomeação e descrição dos perfis
│   ├── figuras.py           # figuras f1–f5
│   ├── tabelas.py           # tabelas LaTeX no formato numérico pt-BR
│   ├── relatorio.py         # relatório Markdown com os números citados no texto
│   ├── main.py              # pipeline completo (ponto de entrada)
│   └── gerar_base_sintetica.py  # base sintética só para teste do código
├── dados/                   # coloque aqui a base (ver dados/README.md)
├── REFERENCIAS.md           # referências comentadas e status de conferência
├── REPRODUCAO.md            # comparação dos números do código com os do artigo
└── requirements.txt
```

## Como reproduzir

Requer Python ≥ 3.10. Ver [REPRODUCAO.md](REPRODUCAO.md) para a comparação com os números do artigo.

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Coloque a base em `dados/` (`.csv` ou `.xlsx`, colunas `id_cliente`, `valor_total_gasto`,
`frequencia_compras`, `ticket_medio`) e execute:

```bash
python src/main.py --dados dados/clientes.csv
```

As saídas vão para `resultados/`:

| Arquivo | Conteúdo |
|---|---|
| `relatorio.md` | todos os números citados no texto, na ordem do artigo |
| `numeros.json` | os mesmos números em formato estruturado |
| `tabelas/*.tex` | corpos das Tabelas 3–6 do artigo |
| `figuras/*.pdf` | Figuras 1–5 do artigo |
| `scores_finais.csv` | score ensemble de cada método por cliente |
| `ids_e_perfis.csv` | perfil e consenso (0–4) de cada cliente |

Para sobrescrever as tabelas e figuras do artigo com as recém-geradas:

```bash
python src/main.py --dados dados/clientes.csv --atualizar-artigo
```

O modo completo (60 desquantizações) leva alguns minutos em CPU. A flag `--rapido`
usa 10 sorteios e serve **apenas** para testar o código.

### Teste sem a base original

```bash
python src/gerar_base_sintetica.py --saida dados/sintetica.csv
```

```bash
python src/main.py --dados dados/sintetica.csv --saida resultados_sinteticos --rapido
```

A base sintética imita a estrutura de quatro blocos, mas **não** reproduz os números do
artigo.

## Protocolo (resumo da Metodologia)

| Etapa | Escolha |
|---|---|
| Espaço | $(\log \tilde f, \log t)$ padronizado; $\tilde f = f + U(-0{,}5;\,0{,}5)$; valor total fora da modelagem (redundante) |
| K-Means | $K = 2..8$, cotovelo + silhueta; `n_init=10` |
| GMM | BIC para $K = 1..8$, covariâncias *full/diag/spherical*, com e sem desquantização; $K=4$ adotado |
| DBSCAN | `minPts = 4`; $\varepsilon$ pelo joelho da 4-distância (maior distância à corda); varredura $\varepsilon \in [0{,}05;\,0{,}5]$ |
| HDBSCAN | `min_cluster_size ∈ {10, 20, 40, 80}`; 40 adotado |
| KDE | kernel gaussiano, banda de Scott $h = n^{-1/6}$ |
| Qualidade | silhueta, Davies-Bouldin, Calinski-Harabasz (sem ruído) |
| Estabilidade da partição | ARI em 30 subamostras de 80% vs. modelo completo; ARI vs. quadrantes (20 compras, R$ 150) |
| Scores | GMM $-\log p(x)$; KDE $-\log \hat p(x)$; K-Means distância ao centroide; HDBSCAN $1-$ pertinência |
| Ensemble | média de 60 desquantizações (sementes 42..101) |
| Estabilidade do score | Jaccard do top 2% em 30 pares de sorteios únicos e entre 2 ensembles de 30 |
| Limiares | top 2% global e percentil 98 por perfil |

Semente global: 42. Todas as escolhas estão em `src/config.py`.

## Compilar o artigo

```bash
cd artigo && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

No Overleaf, envie a pasta `artigo/` inteira e use o compilador pdfLaTeX.

## Uso de IA

Um assistente de IA (Claude, Anthropic) apoiou a análise, a escrita do código, a busca de
referências e a redação, conforme declarado no artigo. A responsabilidade pelas escolhas
metodológicas e pelo conteúdo é dos autores.

## Licença

MIT — ver [LICENSE](LICENSE).
