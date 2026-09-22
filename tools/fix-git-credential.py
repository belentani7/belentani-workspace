#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fix-git-credential.py - Sustituye el credential helper roto de gh
por uno basado en el GITHUB_TOKEN.

Problema: git tenia configurado
    credential.https://github.com.helper = !'gh.exe' auth git-credential
pero gh NO esta autenticado -> todo acceso a repos privados falla.

Solucion: quitar ese helper y poner uno que devuelva el token valido.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


def user_env(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def git(*args, timeout=60):
    p = subprocess.run(["git", *args], capture_output=True, text=True,
                       timeout=timeout, encoding="utf-8", errors="replace",
                       env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


token = user_env("GITHUB_TOKEN")
if not token:
    console.print("[red]Sin token[/]")
    raise SystemExit(1)

console.print("[bold]1. Quitando el helper roto de gh[/]")
code, out, err = git("config", "--global", "--unset-all",
                     "credential.https://github.com.helper")
console.print(f"  codigo={code} (5 = no existia)")

console.print("\n[bold]2. Poniendo el helper con token[/]")
helper = ("!f() { test \"$1\" = get && "
          f"echo username=belentani7 && echo password={token}; }}; f")
code, out, err = git("config", "--global", "--add",
                     "credential.https://github.com.helper", helper)
console.print(f"  codigo={code} {err[:80]}")

# Que no intente preguntar
git("config", "--global", "credential.interactive", "never")

console.print("\n[bold]3. Estado final de los helpers[/]")
for key in ("credential.helper", "credential.https://github.com.helper"):
    code, out, _ = git("config", "--global", "--get-all", key)
    valor = out or "(ninguno)"
    if token[:10] in valor:
        valor = valor.replace(token, "***TOKEN***")
    console.print(f"  {key} = {valor}")

console.print("\n[bold]4. Prueba de acceso[/]")
candidatos = [
    (r"C:\Users\USER\repos\BELENTANI-OS", "BELENTANI-OS (privado)"),
    (r"C:\Users\USER\Desktop\PROJECTOS\belentani-unified", "belentani-unified"),
    (r"C:\Users\USER\repos\belentani-atlas", "belentani-atlas"),
    (r"C:\Users\USER\Documents\01_PROYECTOS\belentani-unified", "Documents/belentani-unified"),
]
for ruta, nombre in candidatos:
    if not Path(ruta).exists():
        console.print(f"  {nombre:<32} [dim]ruta no existe[/]")
        continue
    code, out, err = git("-C", ruta, "ls-remote", "--heads", "origin", timeout=45)
    if code == 0:
        ramas = [l.split("refs/heads/")[-1] for l in out.splitlines() if "refs/heads/" in l]
        console.print(f"  {nombre:<32} [green]OK[/] ramas={ramas[:4]}")
    else:
        console.print(f"  {nombre:<32} [red]FALLA[/] {(err or out)[:70]}")
