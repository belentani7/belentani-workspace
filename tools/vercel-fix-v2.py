#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vercel-fix-v2.py - Salta los builds de la rama gh-pages en aprende-brasil.

Vercel ejecuta `commandForIgnoringBuildStep` antes de construir:
  - salida 0  -> SALTA el build
  - salida !=0 -> CONTINUA el build

gh-pages es rama de salida estatica (sin package.json ni vite), asi que su
build siempre falla con exit 127. Saltandolo se eliminan los builds rotos.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import httpx
from rich.console import Console

console = Console()


def token() -> str:
    t = os.environ.get("VERCEL_TOKEN")
    if t:
        return t
    p = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "[Environment]::GetEnvironmentVariable('VERCEL_TOKEN','User')"],
                       capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


H = {"Authorization": f"Bearer {token()}", "User-Agent": "dsh",
     "Content-Type": "application/json"}
PID = "prj_zHebnvXhYCSmsCK5VErlX7E1mzVx"

COMANDO = 'if [ "$VERCEL_GIT_COMMIT_REF" = "gh-pages" ]; then exit 0; else exit 1; fi'

console.print(f"[cyan]Comando a instalar:[/]\n  {COMANDO}\n")

body = {"commandForIgnoringBuildStep": COMANDO}

for ver in ("v9", "v10"):
    r = httpx.patch(f"https://api.vercel.com/{ver}/projects/{PID}",
                    headers=H, json=body, timeout=45)
    console.print(f"PATCH /{ver}/projects -> HTTP {r.status_code}")
    if r.status_code in (200, 201):
        d = r.json()
        console.print(f"[green]APLICADO[/]")
        console.print(f"  commandForIgnoringBuildStep = {d.get('commandForIgnoringBuildStep')}")
        break
    else:
        console.print(f"  {r.text[:250]}\n")

# Verificar
r = httpx.get(f"https://api.vercel.com/v9/projects/{PID}", headers=H, timeout=45)
if r.status_code == 200:
    v = r.json().get("commandForIgnoringBuildStep")
    console.print(f"\n[bold]Verificacion:[/] {v}")
    if v == COMANDO:
        console.print("[green]OK: los builds de gh-pages se saltaran[/]")
    else:
        console.print("[yellow]No coincide; revisar[/]")

# Estado de los ultimos deploys tras el cambio
r = httpx.get("https://api.vercel.com/v6/deployments", headers=H,
              params={"projectId": PID, "limit": 6}, timeout=45)
console.print("\n[bold]Ultimos deploys:[/]")
for d in r.json().get("deployments", []):
    console.print(f"  {d.get('state'):<8} {d.get('target') or 'preview':<11} "
                  f"{(d.get('meta') or {}).get('githubCommitRef','-'):<10} "
                  f"{(d.get('errorMessage') or '')[:50]}")
