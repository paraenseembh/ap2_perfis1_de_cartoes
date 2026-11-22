# Dados

A base do artigo (`base01_perfil_compras_*.xlsx`, compartilhada pelos autores no Google Drive)
**não está versionada neste repositório**. Coloque o arquivo nesta pasta e informe o caminho com
`--dados` (aceita `.csv` ou `.xlsx`); o padrão é `dados/clientes.csv`.

Esquema esperado (3.000 linhas, uma por cliente):

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_cliente` | texto | identificador (ex.: `C000724`) |
| `valor_total_gasto` | real | gasto total do cliente (R$) |
| `frequencia_compras` | inteiro ≥ 1 | número de compras |
| `ticket_medio` | real > 0 | gasto médio por compra (R$) = valor / frequência |

Para testar o código sem a base, gere uma base sintética com
`python src/gerar_base_sintetica.py --saida dados/sintetica.csv`. Ela não reproduz os
números do artigo.
