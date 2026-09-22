#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
arreglar-auth-git.py - Configura git para que acceda a los repos privados.

Los repos privados de belentani7 fallan con "unable to access" porque git no
tiene credenciales. Solucion: credential helper con el GITHUB_TOKEN, sin
escribir el token en texto plano dentro de la URL.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def get_user_env(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def git(*args, timeout=60):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    p = subprocess.run(["git", *args], capture_output=True, text=True,
                       timeout=timeout, encoding="utf-8", errors="replace", env=env)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def main():
    token = get_user_env("GITHUB_TOKEN")
    if not token:
        console.print("[red]Sin GITHUB_TOKEN[/]")
        return

    # Repo de prueba (privado)
    prueba = None
    for cand in [r"C:\Users\USER\repos\belentani-atlas",
                 r"C:\Users\USER\repos\autonomous-flow",
                 r"C:\Users\USER\Documents\01_PROYECTOS\belentani-unified"]:
        if Path(cand).exists():
            prueba = cand
            break

    if prueba:
        console.print(f"[cyan]Repositorio de prueba:[/] {prueba}")
        code, out, err = git("-C", prueba, "ls-remote", "--heads", "origin", timeout=45)
        console.print(f"  ANTES -> codigo={code}")
        console.print(f"  {(err or out)[:140]}")

    # --- Aplicar credential helper basado en el token ---
    console.print("\n[bold]Configurando credential helper...[/]")
    helper = f'!f() {{ echo "username=belentani7"; echo "password={token}"; }}; f'
    code, out, err = git("config", "--global", "credential.https://github.com.helper", helper)
    console.print(f"  helper configurado: codigo={code} {err[:80]}")

    # Evitar que pida usuario interactivo
    git("config", "--global", "credential.interactive", "never")

    if prueba:
        code, out, err = git("-C", prueba, "ls-remote", "--heads", "origin", timeout=45)
        console.print(f"\n  DESPUES -> codigo={code}")
        if code == 0:
            ramas = [l.split("refs/heads/")[-1] for l in out.splitlines() if "refs/heads/" in l]
            console.print(f"  [green]ACCESO OK[/] ramas remotas: {ramas[:5]}")
        else:
            console.print(f"  [red]sigue fallando:[/] {(err or out)[:140]}")

    # --- Comprobar que no quedo el token en texto plano en .gitconfig ---
    console.print("\n[bold]Verificacion de seguridad:[/]")
    cg = Path.home() / ".gitconfig"
    if cg.exists():
        txt = cg.read_text(encoding="utf-8", errors="replace")
        # el helper contiene el token por necesidad; comprobar que no este como url
        urls_con_token = [l for l in txt.splitlines()
                          if "github.com" in l and token[:12] in l and "insteadOf" in l]
        console.print(f"  URLs con token embebido: {len(urls_con_token)} "
                      f"({'OK' if not urls_con_token else 'REVISAR'})")
        console.print("  [dim]El helper guarda el token en ~/.gitconfig (necesario para acceso "
                      "no interactivo). Rota el token si compartes ese archivo.[/]")


if __name__ == "__main__":
    main()
