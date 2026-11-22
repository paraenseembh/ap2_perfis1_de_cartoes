# Reprodução dos números do artigo

Execução de `python src/main.py --dados dados/base01_perfil_compras.xlsx` sobre a base
original (3.000 clientes), semente 42, 60 desquantizações, scikit-learn 1.9.1.

## O que reproduz exatamente

- **Seção 4 (base):** 51 clientes em 25 grupos idênticos; erro máximo 0,005; PCA 68,9% / 31,1% /
  0,0%; assimetria 1,69 → 0,12; 1 cliente no vazio de frequência e 6 no de ticket (7 anomalias
  globais); Spearman 0,028; IQR = 609 e MAD = 1.358 na escala bruta; 47 valores de frequência.
- **K-Means:** inércia 1.237,6 → 144,8 → 119,3; silhueta máxima 0,857 em K = 4.
- **GMM:** BIC desquantizado escolhe K = 5 (*full* e *diag*); silhueta K = 5 = 0,715.
- **HDBSCAN:** 26, 10, 8, 8 grupos (discreta); 4 grupos sem ruído (desquantizada).
- **DBSCAN:** joelho ε = 0,043 → 14 grupos e 161 ruídos; ε = 0,1 → 5 e 17; ε = 0,15 → 4 e 2;
  ε ≥ 0,2 → 4 e 0.
- **Tabela 3:** linhas de K-Means, GMM e HDBSCAN idênticas; silhueta, DB e CH do DBSCAN idênticos.
- **Tabela 4 (perfis):** idêntica.
- **Scores:** GMM 0,664 (único) e 0,967 (ensemble); K-Means 0,818 (ensemble); as 7 anomalias
  globais no top 2% do GMM, nas posições 6 a 53, 5 delas no top dos quatro; 3 clientes em comum
  com os 60 maiores gastos; taxas de alerta 1,2% / 3,2% / 1,7% / 2,5%; alertas P98 por perfil
  21 / 13 / 15 / 13; união do top 2% = 93 clientes.
- **Tabela 6:** os mesmos 10 clientes, todos 4/4.

## O que diverge (pouco)

As diferenças vêm da sequência de números aleatórios (desquantização e subamostras): o
script original não está disponível e o esquema de sementes aqui é `default_rng(42 + i)`
para o i-ésimo sorteio.

| Item | Artigo | Este código |
|---|---|---|
| BIC *full/diag*, frequência discreta | K = 7 | K = 6 |
| BIC₄ − BIC₅ em 10 sorteios | −17,6 a 22,6; K = 4 em 2, K = 5 em 8 | −8,8 a 19,1; K = 4 em 1, K = 5 em 8 (outro K em 1) |
| DBSCAN: ARI c/ quadrantes / estabilidade | 0,969 / 0,937 ± 0,029 | 0,898 / 0,953 ± 0,022 |
| Jaccard único (dp) — GMM, KDE, K-Means, HDBSCAN | ±0,053; 0,536; 0,263; 0,538 | ±0,048; 0,540; 0,259; 0,549 |
| Jaccard ensemble — KDE, HDBSCAN | 0,905; 0,875 | 0,875; 0,875 |
| Spearman c/ GMM — KDE, K-Means, HDBSCAN | 0,816; 0,942; 0,954 | 0,817; 0,943; 0,955 |
| Jaccard top 2% c/ GMM — K-Means, HDBSCAN, KDE | 0,446; 0,690; 0,600 | 0,463; 0,739; 0,579 |
| Consenso 4/3/2/1 | 29 / 22 / 16 / 26 | 31 / 20 / 14 / 28 |
| Top 10: posição do C002240; score do 1º | 7º; 8,19 | 8º; 8,10 |

## Impacto nas conclusões

Nenhuma conclusão muda: os três métodos convergem para a mesma partição, o GMM continua sendo
o score mais estável (em execução única e em ensemble), captura as 7 anomalias globais, e os
limiares por perfil não mudam. A única afirmação ordinal afetada é "KDE (0,905) à frente do
HDBSCAN (0,875) em ensemble", que aqui vira empate (0,875). Para que texto e código coincidam,
as opções são (a) regenerar as tabelas com `--atualizar-artigo` e atualizar os números citados
no texto, ou (b) manter o artigo e citar este arquivo como nota de reprodução.
