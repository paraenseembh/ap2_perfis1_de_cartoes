"""Escrita das linhas das tabelas LaTeX (formato numérico pt-BR).

Cada arquivo contém apenas o corpo da tabela; o cabeçalho, \\toprule e
\\bottomrule ficam em artigo/main.tex, que os inclui via \\tabinput.
"""
from __future__ import annotations

from pathlib import Path


def br(x: float, casas: int = 3) -> str:
    """Formata número no padrão brasileiro: 40370.0 -> '40.370,0'."""
    s = f"{x:,.{casas}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def br_auto(x: float) -> str:
    """Inteiro sem casas; caso contrário, uma casa decimal."""
    return br(x, 0) if float(x).is_integer() else br(x, 1)


def pct(x: float, casas: int = 1) -> str:
    return br(100 * x, casas) + r"\%"


def _escrever(linhas: list[str], destino: Path) -> None:
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def comparacao(linhas: list[dict], destino: Path) -> None:
    out = []
    for r in linhas:
        out.append(
            f"{r['metodo']} & {r['K']} & {r['ruido']} & {br(r['silhueta'])} & "
            f"{br(r['db'])} & {br(r['ch'], 1)} & {br(r['ari_quadrantes'])} & "
            f"{br(r['estab_media'])} $\\pm$ {br(r['estab_dp'])} \\\\"
        )
    _escrever(out, destino)


def estabilidade_scores(estab: dict, conc: dict, destino: Path, ordem) -> None:
    out = []
    for nome in ordem:
        e = estab[nome]
        out.append(
            f"{nome} & {br(e['unico_media'])} $\\pm$ {br(e['unico_dp'])} & "
            f"{br(e['ensemble'])} & {br(conc[nome]['spearman'])} \\\\"
        )
    _escrever(out, destino)


def perfis(desc: list[dict], destino: Path) -> None:
    out = []
    for p in desc:
        out.append(
            f"{p['perfil']} & {br(p['n'], 0)} ({pct(p['pct_clientes'])}) & "
            f"{br_auto(p['freq_mediana'])} & {br(p['ticket_mediano'], 2)} & "
            f"{br(p['valor_mediano'], 2)} & {pct(p['pct_receita'])} \\\\"
        )
    _escrever(out, destino)


def suspeitos(linhas: list[dict], destino: Path, n_scores: int) -> None:
    out = []
    for r in linhas:
        out.append(
            f"{r['id']} & {r['freq']} & {br(r['ticket'], 2)} & {r['perfil']} & "
            f"{br(r['score'], 2)} & {r['consenso']}/{n_scores} \\\\"
        )
    _escrever(out, destino)
