#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vercel-errores-main.py - Analiza los 51 builds fallidos en la rama main."""
from __future__ import annotations

import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")


def token() -> str:
    t = os.environ.get("VERCEL_TOKEN")
    if t:
        return t
    p = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "[Environment]::GetEnvironmentVariable('VERCEL_TOKEN','User')"],
                       capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


H = {"Authorization": f"Bearer {token()}", "User-Agent": "dsh"}

datos = json.loads((OUT / "vercel-builds-fallidos.json").read_text(encoding="utf-8"))

# Recoger los deploys fallidos de main con su mensaje
fallos = []
for a in datos:
    r = httpx.get("https://api.vercel.com/v6/deployments", headers=H,
                  params={"projectId": a["id"], "limit": 30, "state": "ERROR"},
                  timeout=45)
    if r.status_code != 200:
        continue
    for d in r.json().get("deployments", []):
        rama = (d.get("meta") or {}).get("githubCommitRef") or "?"
        if rama not in ("main", "master"):
            continue
        fallos.append({
            "proyecto": a["name"],
            "uid": d.get("uid"),
            "rama": rama,
            "creado": d.get("created"),
            "msg": (d.get("errorMessage") or "").strip(),
            "commit": (d.get("meta") or {}).get("githubCommitMessage", "")[:70],
        })

console.print(f"[cyan]Deploys fallidos en main:[/] {len(fallos)}")

# Normalizar mensajes
def norm(m: str) -> str:
    m = re.sub(r"\d{4,}", "N", m)
    m = re.sub(r"[0-9a-f]{7,40}", "SHA", m)
    return m[:90]

causas = Counter(norm(f["msg"]) for f in fallos)

t = Table(title="Causas de fallo en main", border_style="cyan")
t.add_column("N", justify="right")
t.add_column("Causa", max_width=78)
for c, n in causas.most_common(20):
    t.add_row(str(n), c or "(sin mensaje)")
console.print(t)

(OUT / "vercel-fallos-main.json").write_text(
    json.dumps(fallos, indent=2, ensure_ascii=False), encoding="utf-8")

# Agrupar por proyecto
porp = Counter(f["proyecto"] for f in fallos)
console.print(f"\n[bold]Proyectos afectados ({len(porp)}):[/]")
for p, n in porp.most_common(25):
    console.print(f"   {p[:42]:<42} {n} build(s) fallido(s)")

console.print(f"\n[green]Guardado: vercel-fallos-main.json[/]")
