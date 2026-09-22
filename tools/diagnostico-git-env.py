#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""diagnostico-git-env.py - Compara git con distintos entornos para hallar el fallo."""
import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

# Coger un repo DIVERGED de ejemplo
import json
estado = json.loads(Path(r"C:\Users\USER\Desktop\produccion\estado.json").read_text(encoding="utf-8"))
div = [x for x in estado if x["verdict"] == "DIVERGED"]
ejemplos = div[:4]

VARIANTES = [
    ("env minimo", {"GIT_TERMINAL_PROMPT": "0"}),
    ("env completo", None),
    ("env completo + prompt off", "FULL_PROMPT"),
]

t = Table(title="Comparacion de entornos para git", border_style="cyan")
t.add_column("Repo", max_width=28)
t.add_column("Variante", max_width=24)
t.add_column("fetch", max_width=10)
t.add_column("rev-list", max_width=42)

for s in ejemplos:
    p = s["path"]
    b = s["branch"] or "main"
    if not Path(p).exists():
        continue
    for nombre, env in VARIANTES:
        if env is None:
            e = None
        elif env == "FULL_PROMPT":
            e = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        else:
            e = env

        try:
            f = subprocess.run(["git", "-C", p, "fetch", "origin", b, "--quiet"],
                               capture_output=True, text=True, timeout=90,
                               encoding="utf-8", errors="replace", env=e)
            f_ok = f.returncode == 0
            f_err = (f.stderr or "").strip()[:0] if f_ok else (f.stderr or "").strip()[:40]
        except subprocess.TimeoutExpired:
            f_ok, f_err = False, "TIMEOUT"
        except Exception as ex:  # noqa: BLE001
            f_ok, f_err = False, str(ex)[:40]

        try:
            r = subprocess.run(["git", "-C", p, "rev-list", "--count", f"origin/{b}..HEAD"],
                               capture_output=True, text=True, timeout=45,
                               encoding="utf-8", errors="replace", env=e)
            r_out = (r.stdout or "").strip()
            r_err = (r.stderr or "").strip()
            if r.returncode == 0 and r_out.isdigit():
                res = f"OK ahead={r_out}"
            else:
                res = (r_err or "sin resultado")[:42]
        except subprocess.TimeoutExpired:
            res = "TIMEOUT"
        except Exception as ex:  # noqa: BLE001
            res = str(ex)[:42]

        t.add_row(s["name"][:28], nombre, "OK" if f_ok else f_err[:10], res.replace("\n", " "))

console.print(t)

console.print("\n[bold]Variables de entorno relevantes en MI sesion:[/]")
for k in sorted(os.environ):
    if k.upper().startswith(("GIT", "HOME", "USER")):
        v = os.environ[k]
        console.print(f"  {k} = {v[:70]}")
