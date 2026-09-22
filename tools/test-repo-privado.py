#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test-repo-privado.py - Prueba acceso a repos que fallaban y limpia los helpers."""
import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def git(*args, cwd=None, timeout=60):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}
    p = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd,
                       timeout=timeout, encoding="utf-8", errors="replace", env=env)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


console.print("[bold]1. Helpers de credenciales configurados[/]")
for scope in ("--global", "--system"):
    code, out, _ = git("config", scope, "--get-all", "credential.helper")
    code2, out2, _ = git("config", scope, "--get-all", "credential.https://github.com.helper")
    console.print(f"  {scope} credential.helper          : {out or '(ninguno)'}")
    console.print(f"  {scope} ...github.com.helper        : {out2 or '(ninguno)'}")

console.print("\n[bold]2. Prueba real en repos que fallaban[/]")
candidatos = [
    (r"C:\Users\USER\repos\belentani-atlas", "belentani-atlas"),
    (r"C:\Users\USER\repos\autonomous-flow", "autonomous-flow"),
    (r"C:\Users\USER\repos\BELENTANI-OS", "BELENTANI-OS"),
    (r"C:\Users\USER\repos\agent-control-plane", "agent-control-plane"),
]
t = Table(border_style="cyan")
t.add_column("Repo")
t.add_column("ls-remote")
t.add_column("Detalle", max_width=50)
for ruta, nombre in candidatos:
    if not Path(ruta).exists():
        t.add_row(nombre, "[dim]no existe[/]", "")
        continue
    code, out, err = git("-C", ruta, "ls-remote", "--heads", "origin", timeout=45)
    if code == 0:
        ramas = [l.split("refs/heads/")[-1] for l in out.splitlines() if "refs/heads/" in l]
        t.add_row(nombre, "[green]OK[/]", f"ramas: {ramas[:4]}")
    else:
        t.add_row(nombre, "[red]FALLA[/]", (err or out)[:50])
console.print(t)

console.print("\n[bold]3. Reintento con GIT_ASKPASS desactivado y token explicito[/]")
p = subprocess.run(
    ["powershell", "-NoProfile", "-Command",
     "[Environment]::GetEnvironmentVariable('GITHUB_TOKEN','User')"],
    capture_output=True, text=True, timeout=20)
token = (p.stdout or "").strip()

if token:
    ruta = r"C:\Users\USER\repos\belentani-atlas"
    if Path(ruta).exists():
        env = {**os.environ,
               "GIT_TERMINAL_PROMPT": "0",
               "GIT_CONFIG_COUNT": "1",
               "GIT_CONFIG_KEY_0": "url.https://x-access-token:" + token + "@github.com/.insteadOf",
               "GIT_CONFIG_VALUE_0": "https://github.com/"}
        r = subprocess.run(["git", "-C", ruta, "ls-remote", "--heads", "origin"],
                           capture_output=True, text=True, timeout=45,
                           encoding="utf-8", errors="replace", env=env)
        if r.returncode == 0:
            ramas = [l.split("refs/heads/")[-1] for l in r.stdout.splitlines() if "refs/heads/" in l]
            console.print(f"  [green]CON TOKEN EXPLICITO: OK[/] ramas={ramas[:4]}")
        else:
            console.print(f"  [red]con token tambien falla:[/] {(r.stderr or '')[:120]}")
