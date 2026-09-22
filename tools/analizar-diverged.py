#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
analizar-diverged.py - Clasifica los repos DIVERGED por adelante/detras.

Un repo DIVERGED puede estar:
  - solo por DELANTE  -> hay trabajo local sin publicar (NO borrar)
  - solo por DETRAS   -> el remoto es superconjunto (recuperable)
  - AMBOS lados       -> historiales separados (decision manual)
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")


def git(repo, *args, timeout=60):
    try:
        p = subprocess.run(["git", "-C", str(repo), *args],
                           capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace",
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", str(e)


def main():
    estado = json.loads((OUT / "estado.json").read_text(encoding="utf-8"))
    div = [x for x in estado if x["verdict"] == "DIVERGED"]
    console.print(f"[cyan]Repos DIVERGED a analizar:[/] {len(div)}\n")

    delante, detras, ambos, error = [], [], [], []

    for i, s in enumerate(div, 1):
        if i % 20 == 0:
            console.print(f"  ... {i}/{len(div)}", style="dim")
        p, b = s["path"], s["branch"] or "main"
        git(p, "fetch", "origin", b, "--quiet", timeout=60)
        _, o_a, _ = git(p, "rev-list", "--count", f"origin/{b}..HEAD")
        _, o_b, _ = git(p, "rev-list", "--count", f"HEAD..origin/{b}")
        a = int(o_a) if o_a.isdigit() else -1
        d = int(o_b) if o_b.isdigit() else -1
        rec = (s["name"], p, round(s.get("size_mb") or 0, 1), a, d)
        if a < 0 or d < 0:
            error.append(rec)
        elif a > 0 and d == 0:
            delante.append(rec)
        elif a == 0 and d > 0:
            detras.append(rec)
        elif a > 0 and d > 0:
            ambos.append(rec)
        else:
            error.append(rec)

    t = Table(title="Analisis de DIVERGED", border_style="cyan")
    t.add_column("Categoria")
    t.add_column("N", justify="right")
    t.add_column("MB", justify="right")
    t.add_column("Significado")
    t.add_row("[red]Solo DELANTE[/]", str(len(delante)),
              f"{sum(x[2] for x in delante):,.0f}",
              "trabajo local SIN publicar -> NO borrar")
    t.add_row("[green]Solo DETRAS[/]", str(len(detras)),
              f"{sum(x[2] for x in detras):,.0f}",
              "remoto es superconjunto -> recuperable")
    t.add_row("[yellow]AMBOS lados[/]", str(len(ambos)),
              f"{sum(x[2] for x in ambos):,.0f}",
              "historiales separados -> decision manual")
    t.add_row("[dim]Sin clasificar[/]", str(len(error)), "0", "")
    console.print(t)

    if delante:
        console.print(f"\n[red]POR DELANTE (trabajo sin publicar):[/]")
        for n, _, mb, a, _ in sorted(delante, key=lambda x: -x[3])[:25]:
            console.print(f"   {n[:44]:<44} +{a:<5} {mb:>8} MB")

    if ambos:
        console.print(f"\n[yellow]AMBOS LADOS:[/]")
        for n, _, mb, a, d in sorted(ambos, key=lambda x: -(x[3] + x[4]))[:25]:
            console.print(f"   {n[:44]:<44} +{a}/-{d:<5} {mb:>8} MB")

    if detras:
        console.print(f"\n[green]SOLO DETRAS (top 15 por tamano):[/]")
        for n, _, mb, a, d in sorted(detras, key=lambda x: -x[2])[:15]:
            console.print(f"   {n[:44]:<44} -{d:<5} {mb:>8} MB")

    (OUT / "diverged-analisis.json").write_text(json.dumps({
        "delante": [{"name": n, "path": p, "mb": mb, "ahead": a} for n, p, mb, a, _ in delante],
        "detras": [{"name": n, "path": p, "mb": mb, "behind": d} for n, p, mb, _, d in detras],
        "ambos": [{"name": n, "path": p, "mb": mb, "ahead": a, "behind": d} for n, p, mb, a, d in ambos],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]Guardado: diverged-analisis.json[/]")


if __name__ == "__main__":
    main()
