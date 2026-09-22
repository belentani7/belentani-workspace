#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vercel-fix-aprende-brasil.py - Arregla los builds rotos de la rama gh-pages.

Problema: gh-pages es una rama de SALIDA estatica (sin package.json ni vite).
Vercel intenta compilarla con "vite build" -> exit 127 (comando no encontrado)
-> build roto en cada push, consumiendo minutos de build.

Solucion: deshabilitar los deploys automaticos para esa rama, manteniendo main.
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


TOK = token()
H = {"Authorization": f"Bearer {TOK}", "User-Agent": "dsh",
     "Content-Type": "application/json"}

PROYECTO = "aprende-brasil"

# 1. Localizar
r = httpx.get("https://api.vercel.com/v9/projects", headers=H,
              params={"limit": 100, "search": PROYECTO}, timeout=45)
proys = [p for p in r.json().get("projects", []) if p.get("name") == PROYECTO]
if not proys:
    console.print(f"[red]No se encontro el proyecto {PROYECTO}[/]")
    raise SystemExit(1)
p = proys[0]
pid = p["id"]
console.print(f"[cyan]Proyecto:[/] {p['name']} ({pid})")

# 2. Ver configuracion git actual
git = p.get("git") or {}
console.print(f"\n[bold]Configuracion git actual:[/]")
console.print(json.dumps(git, indent=2, ensure_ascii=False)[:600])

# 3. Deshabilitar la rama gh-pages
nueva = dict(git)
enabled = dict(nueva.get("deploymentEnabled") or {})
console.print(f"\n  deploymentEnabled antes: {enabled or '(vacio = todas habilitadas)'}")

enabled["gh-pages"] = False
# asegurar que main sigue activa
enabled.setdefault("main", True)
nueva["deploymentEnabled"] = enabled

console.print(f"  deploymentEnabled despues: {enabled}")

body = {"git": nueva}
r2 = httpx.patch(f"https://api.vercel.com/v9/projects/{pid}",
                 headers=H, json=body, timeout=45)
console.print(f"\n[bold]PATCH /v9/projects/{pid} -> HTTP {r2.status_code}[/]")
if r2.status_code in (200, 201):
    d = r2.json()
    g2 = d.get("git") or {}
    console.print("[green]APLICADO[/]")
    console.print(json.dumps(g2.get("deploymentEnabled") or {}, indent=2, ensure_ascii=False))
else:
    console.print(f"[red]{r2.text[:300]}[/]")

# 4. Verificar
r3 = httpx.get(f"https://api.vercel.com/v9/projects/{pid}", headers=H, timeout=45)
if r3.status_code == 200:
    g3 = (r3.json().get("git") or {}).get("deploymentEnabled") or {}
    console.print(f"\n[bold]Verificacion:[/] gh-pages -> {g3.get('gh-pages')}")
    if g3.get("gh-pages") is False:
        console.print("[green]OK: Vercel ya no compilara la rama gh-pages[/]")
    else:
        console.print("[yellow]No se pudo confirmar el cambio[/]")
