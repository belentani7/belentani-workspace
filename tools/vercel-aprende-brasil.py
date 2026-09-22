#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vercel-aprende-brasil.py - Diagnostico del proyecto aprende-brasil en Vercel."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


def token() -> str:
    t = os.environ.get("VERCEL_TOKEN")
    if t:
        return t
    p = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "[Environment]::GetEnvironmentVariable('VERCEL_TOKEN','User')"],
                       capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


TOK = token()
H = {"Authorization": f"Bearer {TOK}", "User-Agent": "dsh"}

# Buscar el proyecto
r = httpx.get("https://api.vercel.com/v9/projects", headers=H,
              params={"limit": 100, "search": "aprende"}, timeout=45)
proyectos = r.json().get("projects", [])
console.print(f"[cyan]Proyectos que coinciden con 'aprende':[/] {len(proyectos)}")

for p in proyectos:
    console.print(f"\n[bold]=== {p.get('name')} (id={p['id']})[/]")
    console.print(f"  framework     : {p.get('framework')}")
    console.print(f"  repo          : {(p.get('link') or {}).get('repo')}")
    console.print(f"  rama prod     : {p.get('link', {}).get('productionBranch')}")
    console.print(f"  creado        : {p.get('createdAt')}")
    console.print(f"  actualizado   : {p.get('updatedAt')}")
    console.print(f"  rootDirectory : {p.get('rootDirectory')}")
    console.print(f"  buildCommand  : {p.get('buildCommand')}")
    console.print(f"  outputDir     : {p.get('outputDirectory')}")
    console.print(f"  installCommand: {p.get('installCommand')}")

    # Deploys
    d = httpx.get("https://api.vercel.com/v6/deployments", headers=H,
                  params={"projectId": p["id"], "limit": 12}, timeout=45)
    deps = d.json().get("deployments", [])
    console.print(f"\n  [bold]Ultimos {len(deps)} deploys:[/]")
    t = Table(border_style="cyan")
    t.add_column("Estado")
    t.add_column("Target")
    t.add_column("Rama")
    t.add_column("Creado")
    t.add_column("Error", max_width=40)
    for dep in deps:
        t.add_row(
            dep.get("state", "?"),
            dep.get("target") or "preview",
            (dep.get("meta") or {}).get("githubCommitRef") or "-",
            str(dep.get("created"))[:10],
            (dep.get("errorMessage") or "")[:40],
        )
    console.print(t)

    # Deploy de produccion concreto
    prod = [x for x in deps if x.get("target") == "production"]
    if prod:
        ultimo = prod[0]
        console.print(f"\n  [green]Deploy de produccion mas reciente:[/] "
                      f"{ultimo.get('url')} ({ultimo.get('state')})")
        console.print(f"     commit: {(ultimo.get('meta') or {}).get('githubCommitMessage','')[:90]}")
    else:
        console.print(f"\n  [red]SIN deploy de produccion[/]")
