#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
auditar-reparacion.py - Verifica las suposiciones del script de Gemini ANTES
de ejecutarlo. Comprueba:
  1. Si 'requests' esta instalado (el script lo usa)
  2. Tamano real de BELENTANI-OS_2 y sus archivos grandes (limite GitHub = 100 MB)
  3. Estructura REAL de vercel-fallos-main.json (el script asume otra)
  4. Estado de agentbox / nexus-data (detached HEAD)
  5. Si la tarea DelSystem32Transcript se puede desactivar
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
HOME = Path.home()
DESK = HOME / "Desktop"
PROD = DESK / "produccion"

console.rule("[bold]1. Dependencias del script de Gemini")
try:
    import requests  # noqa: F401
    console.print("  [green]requests INSTALADO[/]")
except ImportError:
    console.print("  [red]requests NO INSTALADO[/] -> el script fallaria al importar")
try:
    import httpx  # noqa: F401
    console.print("  [green]httpx disponible[/] (alternativa)")
except ImportError:
    console.print("  [red]httpx tampoco[/]")

console.rule("[bold]2. BELENTANI-OS_2 - archivos grandes")


def buscar_dir(nombre: str, bases) -> Path | None:
    """Busca un directorio tolerando enlaces rotos y errores de permisos.

    NOTA: Path.rglob() CRASHEA con enlaces rotos en node_modules. Se usa
    os.walk con onerror para sobrevivir.
    """
    import os
    for base in bases:
        if not base.exists():
            continue
        for root, dirs, _ in os.walk(base, onerror=lambda e: None):
            if Path(root).name == nombre:
                return Path(root)
    return None


objetivo = buscar_dir("BELENTANI-OS_2", (DESK, HOME / "Documents", HOME / "repos"))

if objetivo:
    console.print(f"  ruta: {objetivo}")
    gitdir = objetivo / ".git"
    console.print(f"  .git existe: {gitdir.exists()}")
    if gitdir.exists():
        entradas = list(gitdir.iterdir())
        console.print(f"  entradas en .git: {len(entradas)} -> {[e.name for e in entradas][:8]}")

    # archivos > 50 MB (GitHub avisa a 50, rechaza a 100)
    grandes = []
    for f in objetivo.rglob("*"):
        if f.is_file():
            try:
                sz = f.stat().st_size
            except OSError:
                continue
            if sz > 50 * 1024 * 1024:
                grandes.append((sz, f))
    grandes.sort(reverse=True)
    t = Table(title="Archivos >50 MB (GitHub rechaza >100 MB)", border_style="red")
    t.add_column("MB", justify="right")
    t.add_column("Ruta")
    for sz, f in grandes[:15]:
        color = "red" if sz > 100 * 1024 * 1024 else "yellow"
        t.add_row(f"[{color}]{sz/1024/1024:,.1f}[/]", str(f).replace(str(objetivo), ".")[:80])
    console.print(t)
    if any(sz > 100 * 1024 * 1024 for sz, _ in grandes):
        console.print("  [red bold]HAY ARCHIVOS >100 MB: el push a GitHub FALLARA[/]")
        console.print("  [red]Hay que usar Git LFS o excluirlos.[/]")

    # total
    total = sum(f.stat().st_size for f in objetivo.rglob("*") if f.is_file())
    console.print(f"  tamano total: {total/1024/1024:,.1f} MB")
else:
    console.print("  [red]No encontrado[/]")

console.rule("[bold]3. Estructura REAL de vercel-fallos-main.json")
vf = PROD / "vercel-fallos-main.json"
if vf.exists():
    d = json.loads(vf.read_text(encoding="utf-8"))
    console.print(f"  tipo raiz: [bold]{type(d).__name__}[/]")
    if isinstance(d, list):
        console.print(f"  elementos: {len(d)}")
        if d:
            console.print(f"  claves de un elemento: {list(d[0].keys())}")
            console.print(f"  ejemplo: {json.dumps(d[0], ensure_ascii=False)[:250]}")
        console.print("\n  [yellow]El script de Gemini hace data.get('projects', []) ->[/]")
        console.print("  [red]CRASH: una lista no tiene .get(). Y no existe 'error_type'.[/]")
    elif isinstance(d, dict):
        console.print(f"  claves: {list(d.keys())}")
else:
    console.print("  no existe")

console.rule("[bold]4. agentbox / nexus-data (detached HEAD)")
for nombre in ("agentbox", "nexus-data"):
    encontrado = False
    for base in (DESK, HOME / "Documents", HOME / "repos"):
        for p in base.rglob(nombre):
            if p.is_dir() and (p / ".git").exists():
                r = subprocess.run(["git", "-C", str(p), "branch", "--show-current"],
                                   capture_output=True, text=True, timeout=30,
                                   encoding="utf-8", errors="replace",
                                   env={**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"})
                rama = (r.stdout or "").strip()
                r2 = subprocess.run(["git", "-C", str(p), "status", "-sb"],
                                    capture_output=True, text=True, timeout=30,
                                    encoding="utf-8", errors="replace",
                                    env={**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"})
                console.print(f"  {nombre}: rama='{rama or '(DETACHED)'}'")
                console.print(f"     {r2.stdout.strip().splitlines()[0] if r2.stdout.strip() else ''}")
                encontrado = True
                break
        if encontrado:
            break
    if not encontrado:
        console.print(f"  {nombre}: [dim]no encontrado[/]")

console.rule("[bold]5. Tarea DelSystem32Transcript")
r = subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Get-ScheduledTask -TaskName 'DelSystem32Transcript' | "
                    "Select-Object TaskName,State | Format-List"],
                   capture_output=True, text=True, timeout=60,
                   encoding="utf-8", errors="replace")
console.print(r.stdout or r.stderr or "(sin salida)")
