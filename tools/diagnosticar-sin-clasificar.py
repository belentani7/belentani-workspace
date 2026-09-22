#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""diagnosticar-sin-clasificar.py - Por que fallan 67 repos al calcular ahead/behind."""
import json
import subprocess
from collections import Counter
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
                           env={"GIT_TERMINAL_PROMPT": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", str(e)


estado = json.loads((OUT / "estado.json").read_text(encoding="utf-8"))
div = [x for x in estado if x["verdict"] == "DIVERGED"]

motivos = Counter()
detalle = []
for s in div:
    p, b = s["path"], s["branch"] or "main"
    code, out, err = git(p, "rev-list", "--count", f"origin/{b}..HEAD")
    if code == 0 and out.isdigit():
        continue
    # falla: averiguar por que
    code_f, _, err_f = git(p, "fetch", "origin", "--quiet", timeout=60)
    code_lr, lr, err_lr = git(p, "ls-remote", "--heads", "origin")
    ramas = [l.split("refs/heads/")[-1] for l in lr.splitlines() if "refs/heads/" in l]
    if code_lr != 0:
        motivo = f"ls-remote falla: {err_lr[:50]}"
    elif b not in ramas:
        motivo = f"rama '{b}' no existe en remoto (tiene: {', '.join(ramas[:3]) or 'ninguna'})"
    else:
        motivo = f"otro: {err[:60]}"
    motivos[motivo.split("(")[0][:50]] += 1
    detalle.append((s["name"], b, ramas[:4], motivo))

t = Table(title="Motivos de fallo", border_style="cyan")
t.add_column("Motivo", max_width=60)
t.add_column("N", justify="right")
for m, n in motivos.most_common(10):
    t.add_row(m, str(n))
console.print(t)

console.print("\n[bold]Detalle (primeros 20):[/]")
for n, b, ramas, m in detalle[:20]:
    console.print(f"  {n[:34]:<34} rama_local={b:<10} remotas={ramas}")
    console.print(f"      {m[:95]}")

(OUT / "sin-clasificar.json").write_text(
    json.dumps([{"name": n, "branch": b, "remote_branches": r, "motivo": m}
                for n, b, r, m in detalle], indent=2, ensure_ascii=False), encoding="utf-8")
console.print(f"\n[green]Guardado: sin-clasificar.json ({len(detalle)})[/]")
