# Referências do artigo

Lista comentada das 27 referências de `artigo/referencias.bib`, com o papel de cada uma no
texto e o status de conferência. As pendências reproduzem as observações deixadas em
comentário no próprio `.bib` e devem ser resolvidas antes da entrega final.

Legenda de status: ✅ dados bibliográficos completos · ⚠️ conferir antes da entrega

## Algoritmos e métodos

| Chave | Referência | Onde é usada | Status |
|---|---|---|---|
| `macqueen1967kmeans` | MacQueen, J. (1967). *Some methods for classification and analysis of multivariate observations*. Proc. 5th Berkeley Symposium, v. 1, p. 281–297. | Metodologia — K-Means | ✅ |
| `dempster1977em` | Dempster, A. P.; Laird, N. M.; Rubin, D. B. (1977). *Maximum likelihood from incomplete data via the EM algorithm*. JRSS B, 39(1), 1–38. | Metodologia — GMM/EM | ✅ |
| `ester1996dbscan` | Ester, M. et al. (1996). *A density-based algorithm for discovering clusters in large spatial databases with noise*. KDD-96, p. 226–231. | Metodologia — DBSCAN | ✅ |
| `campello2013hdbscan` | Campello, R. J. G. B.; Moulavi, D.; Sander, J. (2013). *Density-based clustering based on hierarchical density estimates*. PAKDD 2013, LNCS 7819, p. 160–172. | Metodologia — HDBSCAN | ✅ |
| `hinneburg1998denclue` | Hinneburg, A.; Keim, D. A. (1998). *An efficient approach to clustering in large multimedia databases with noise*. KDD-98, p. 58–65. | Metodologia — KDE/DENCLUE | ✅ |
| `schwarz1978bic` | Schwarz, G. (1978). *Estimating the dimension of a model*. Annals of Statistics, 6(2), 461–464. | Metodologia — BIC | ✅ |
| `scott1992density` | Scott, D. W. (1992). *Multivariate Density Estimation*. Wiley. | Metodologia — banda do KDE | ✅ |
| `theis2016dequant` | Theis, L.; van den Oord, A.; Bethge, M. (2016). *A note on the evaluation of generative models*. ICLR. | Pré-processamento — desquantização | ⚠️ avaliar se Uria et al. (2013) é a citação mais adequada |
| `pedregosa2011sklearn` | Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*. JMLR, 12, 2825–2830. | Metodologia — implementação | ✅ |

## Validação de agrupamentos

| Chave | Referência | Onde é usada | Status |
|---|---|---|---|
| `rousseeuw1987silhouette` | Rousseeuw, P. J. (1987). *Silhouettes…*. J. Comput. Appl. Math., 20, 53–65. | Metodologia — silhueta | ✅ |
| `davies1979index` | Davies, D. L.; Bouldin, D. W. (1979). *A cluster separation measure*. IEEE TPAMI, PAMI-1(2), 224–227. | Metodologia — índice DB | ✅ |
| `calinski1974index` | Caliński, T.; Harabasz, J. (1974). *A dendrite method for cluster analysis*. Communications in Statistics, 3(1), 1–27. | Metodologia — índice CH | ✅ |
| `hubert1985ari` | Hubert, L.; Arabie, P. (1985). *Comparing partitions*. Journal of Classification, 2, 193–218. | Metodologia — ARI | ✅ |

## Fraude, segmentação e marketing

| Chave | Referência | Onde é usada | Status |
|---|---|---|---|
| `bolton2002fraud` | Bolton, R. J.; Hand, D. J. (2002). *Statistical fraud detection: A review*. Statistical Science, 17(3), 235–255. | Introdução, Fundamentação, Resultados | ✅ |
| `weston2008peer` | Weston, D. J. et al. (2008). *Plastic card fraud detection using peer group analysis*. Advances in Data Analysis and Classification. | Fundamentação, defesa do GMM | ⚠️ faltam volume, páginas e DOI |
| `fader2005rfm` | Fader, P. S.; Hardie, B. G. S.; Lee, K. L. (2005). *RFM and CLV…*. Journal of Marketing Research, 42(4), 415–430. | Fundamentação — RFM | ✅ |
| `wedel2000segmentation` | Wedel, M.; Kamakura, W. A. (2000). *Market Segmentation*. 2. ed. Kluwer. | Fundamentação — segmentação | ✅ |
| `anderson2004longtail` | Anderson, C. (2004). *The Long Tail*. Wired, 12(10). | Resultados — concentração de receita | ✅ |

## Fontes brasileiras e recentes

| Chave | Referência | Onde é usada | Status |
|---|---|---|---|
| `febraban2025` | Febraban (2025). Notícia na Folha de S.Paulo sobre prejuízo de R$ 10 bi com golpes. [link](https://www1.folha.uol.com.br/mercado/2025/03/prejuizo-com-golpe-financeiro-subiu-a-mais-de-r-10-bi-ano-passado-diz-febraban.shtml) | Introdução | ⚠️ preferir o relatório original da Febraban |
| `serasa2025` | Serasa Experian (2025). Comunicado sobre o aumento de 104% nas tentativas de fraude. [link](https://www.serasaexperian.com.br/sala-de-imprensa/prevencao-a-fraude/tentativas-de-fraudes-bancarias-cresceram-104-em-2024-e-poderiam-gerar-prejuizo-de-ate-r-516-bilhoes-revela-serasa-experian/) | Introdução | ⚠️ confirmar título exato |
| `silva2025gmm` | da Silva, M. D.; Roma, W. C. (2025). *Fraudes em Cartões de Crédito: Uma Abordagem Híbrida e Unificada com Machine Learning e GMM*. Anais do WSIS. [link](https://sol.sbc.org.br/index.php/wsis/article/view/37632) | Trabalhos Relacionados | ⚠️ conferir nome completo do evento |
| `oliveira2023spending` | Oliveira, G. P.; Gertrudes, J. C.; Oliveira, R. B. (2023). *Spending pattern visualization using unsupervised machine learning*. SBBD, p. 167–178. [link](https://sol.sbc.org.br/index.php/sbbd/article/view/25525) | Trabalhos Relacionados | ✅ |
| `torres2020visual` | Torres, R. A. L. (2020). *Uma proposta de análise on-line e identificação de transações financeiras fraudulentas com visual analytics*. Dissertação, UnB. [link](https://repositorio.unb.br/handle/10482/40854) | Trabalhos Relacionados | ✅ |
| `santos2024sintetico` | dos Santos, A. C. B. et al. (2024). *Construção de um Modelo Orientado a Dados para Detecção de Fraudes em Cartões de Crédito utilizando Dados Sintéticos*. SBSeg. [link](https://sol.sbc.org.br/index.php/sbseg/article/view/30067) | Trabalhos Relacionados, Limitações | ✅ |
| `karnavou2025fraud` | Karnavou, E. et al. (2025). *I know you're a fraud…*. Expert Systems with Applications. DOI [10.1016/j.eswa.2025.128148](https://doi.org/10.1016/j.eswa.2025.128148) | Trabalhos Relacionados | ⚠️ confirmar volume |
| `kutz2025rfm` | Kutz, E. J.; Senefonte, H. C. M. (2025). *Mapeando perfis de consumidores de E-Commerce com RFM e K-Means*. CoURB, p. 99–112. DOI [10.5753/courb.2025.8768](https://doi.org/10.5753/courb.2025.8768) | Fundamentação | ✅ |
| `fernandes2022rfm` | Fernandes, A. C. A. (2022). *Segmentação e o modelo RFM no varejo brasileiro…*. PUC-Rio. [link](https://bdtd.ibict.br/vufind/Record/PUC_RIO-1_5340ff6115a29d9b20a328a2555ca6bc) | Fundamentação | ⚠️ o `.bib` usa `@phdthesis`; conferir se é tese ou dissertação |

## Pendências antes da entrega

1. `weston2008peer`: completar volume, páginas e DOI.
2. `theis2016dequant`: decidir entre Theis et al. (2016) e Uria et al. (2013) para a desquantização.
3. `febraban2025`: substituir a notícia pelo relatório original, se disponível.
4. `serasa2025`, `silva2025gmm`, `karnavou2025fraud`: confirmar título, evento e volume.
5. `fernandes2022rfm`: confirmar o tipo de trabalho (tese x dissertação).
6. `artigo/main.tex`: o comando `\repo` ainda está em vermelho, entre colchetes, como marcador.
