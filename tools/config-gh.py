#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
config-gh.py - Configura GH_TOKEN para que el CLI gh funcione
y descarga el inventario completo de repos (publicos + privados).

El CLI gh no estaba autenticado, pero el GITHUB_TOKEN de usuario SI es valido.
gh acepta la variable GH_TOKEN como alternativa al login interactivo.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")
OUT.mkdir(parents=True, exist_ok=True)
GH = r"C:\Program Files\GitHub CLI\gh.exe"


def user_env(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def set_user_env(name: str, value: str) -> None:
    subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::SetEnvironmentVariable('%s','%s','User')" % (name, value)],
        capture_output=True, text=True, timeout=20)


def main():
    token = user_env("GITHUB_TOKEN")
    if not token:
        console.print("[red]No hay GITHUB_TOKEN en el entorno de usuario.[/]")
        return

    console.print(f"[cyan]GITHUB_TOKEN encontrado[/] ({len(token)} chars)")
    set_user_env("GH_TOKEN", token)
    console.print("[green]GH_TOKEN escrito a nivel de usuario.[/]")

    env = {**os.environ, "GH_TOKEN": token}

    # --- Inventario completo via API (incluye privados) ---
    console.print("\n[bold]Descargando inventario completo...[/]")
    repos = []
    page = 1
    with httpx.Client(timeout=40, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "dsh"}) as c:
        while True:
            r = c.get("https://api.github.com/user/repos",
                      params={"per_page": 100, "page": page,
                              "affiliation": "owner", "sort": "updated"})
            if r.status_code != 200:
                console.print(f"[red]HTTP {r.status_code}: {r.text[:120]}[/]")
                break
            batch = r.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
            if page > 8:
                break

    console.print(f"[green]Repos encontrados: {len(repos)}[/]")
    pub = [x for x in repos if not x["private"]]
    priv = [x for x in repos if x["private"]]

    t = Table(title="Inventario GitHub real", border_style="cyan")
    t.add_column("Tipo")
    t.add_column("Cantidad", justify="right")
    t.add_column("Tamano total MB", justify="right")
    t.add_row("[green]Publicos[/]", str(len(pub)),
              f"{sum(x['size'] for x in pub)/1024:,.0f}")
    t.add_row("[yellow]Privados[/]", str(len(priv)),
              f"{sum(x['size'] for x in priv)/1024:,.0f}")
    t.add_row("[bold]TOTAL[/]", f"[bold]{len(repos)}[/]",
              f"[bold]{sum(x['size'] for x in repos)/1024:,.0f}[/]")
    console.print(t)

    (OUT / "github-inventario.json").write_text(
        json.dumps([{
            "name": x["name"], "private": x["private"],
            "size_kb": x["size"], "pushed": x["pushed_at"],
            "default_branch": x["default_branch"],
            "archived": x["archived"], "has_pages": x.get("has_pages"),
            "language": x.get("language"), "url": x["html_url"],
        } for x in repos], indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]Guardado:[/] github-inventario.json")

    # --- Cruzar con los NO_REMOTE locales ---
    estado = OUT / "estado.json"
    if estado.exists():
        local = json.loads(estado.read_text(encoding="utf-8"))
        sin_remoto = [x for x in local if x["verdict"] == "NO_REMOTE"]
        nombres_gh = {x["name"].lower() for x in repos}
        ya_existe, falta = [], []
        for s in sin_remoto:
            (ya_existe if s["name"].lower() in nombres_gh else falta).append(s["name"])
        console.print(f"\n[bold]De los {len(sin_remoto)} repos locales sin remoto:[/]")
        console.print(f"  [green]ya existen en GitHub (solo falta reconectar):[/] {len(ya_existe)}")
        console.print(f"  [red]no existen en GitHub:[/] {len(falta)}")
        (OUT / "sin-remoto-reconectar.json").write_text(
            json.dumps(sorted(ya_existe), indent=2, ensure_ascii=False), encoding="utf-8")
        (OUT / "sin-remoto-crear.json").write_text(
            json.dumps(sorted(falta), indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
