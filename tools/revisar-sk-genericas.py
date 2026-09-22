#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""revisar-sk-genericas.py - Comprueba si las claves sk- genericas son reales."""
import re
from collections import Counter
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
F = Path.home() / "Desktop" / "API-KEYS-TODAS.txt"
txt = F.read_text(encoding="utf-8", errors="replace")

vals = []
for line in txt.splitlines():
    s = line.strip()
    if line.startswith("      ") and len(s) > 20 and " " not in s:
        vals.append(s)

genericas = sorted({v for v in vals if v.startswith("sk-")
                    and not v.startswith(("sk-or-", "sk-ant", "sk-mZA"))})
console.print(f"[cyan]Claves sk- genericas unicas:[/] {len(genericas)}")

t = Table(title="Comprobacion contra DeepSeek", border_style="cyan")
t.add_column("#", justify="right")
t.add_column("Prefijo/forma")
t.add_column("Longitud", justify="right")
t.add_column("Resultado", max_width=42)

for i, v in enumerate(genericas, 1):
    forma = v[:10] + "..." + v[-4:]
    try:
        r = httpx.get("https://api.deepseek.com/models",
                      headers={"Authorization": f"Bearer {v}"}, timeout=25)
        if r.status_code == 200:
            res = "[green]VALIDA DeepSeek[/]"
        elif r.status_code == 401:
            res = "[dim]no es DeepSeek (401)[/]"
        else:
            res = f"[yellow]HTTP {r.status_code}[/]"
    except Exception as e:  # noqa: BLE001
        res = f"[red]error[/] {str(e)[:30]}"
    t.add_row(str(i), forma, str(len(v)), res)

console.print(t)

# Detectar si son variaciones de la misma clave (mismo prefijo/sufijo)
console.print("\n[bold]Analisis de similitud:[/]")
prefijos = Counter(v[:12] for v in genericas)
sufijos = Counter(v[-8:] for v in genericas)
console.print(f"  prefijos distintos (12 chars): {len(prefijos)}")
console.print(f"  sufijos distintos (8 chars):   {len(sufijos)}")
console.print(f"  longitudes: {sorted(set(len(v) for v in genericas))}")
