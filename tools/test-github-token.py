#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test-github-token.py - Comprueba si el GITHUB_TOKEN sirve para la API."""
import subprocess

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


def getk(n: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % n],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def main():
    t = Table(title="Tokens de GitHub disponibles", border_style="cyan")
    t.add_column("Variable")
    t.add_column("Tamano", justify="right")
    t.add_column("Resultado", max_width=58)

    found = False
    for name in ["GITHUB_TOKEN", "GH_TOKEN", "GITHUB_PAT"]:
        k = getk(name)
        if not k:
            t.add_row(name, "-", "[dim]ausente[/]")
            continue
        found = True
        try:
            r = httpx.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {k}",
                         "Accept": "application/vnd.github+json",
                         "User-Agent": "dsh"},
                timeout=25)
            if r.status_code == 200:
                d = r.json()
                scopes = r.headers.get("x-oauth-scopes", "")
                t.add_row(name, str(len(k)),
                          f"[green]VALIDO[/] user={d.get('login')} "
                          f"pub={d.get('public_repos')} priv={d.get('total_private_repos')} "
                          f"scopes=[{scopes or 'ninguno'}]")
            elif r.status_code == 401:
                t.add_row(name, str(len(k)), "[red]INVALIDO (401)[/]")
            else:
                t.add_row(name, str(len(k)), f"[yellow]HTTP {r.status_code}[/] {r.text[:40]}")
        except Exception as e:  # noqa: BLE001
            t.add_row(name, str(len(k)), f"[red]error[/] {str(e)[:40]}")

    console.print(t)
    if not found:
        console.print("[yellow]No hay ningun token de GitHub en el entorno de usuario.[/]")


if __name__ == "__main__":
    main()
