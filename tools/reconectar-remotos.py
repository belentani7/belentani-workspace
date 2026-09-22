#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
reconectar-remotos.py - Reconecta los repos locales que perdieron su remoto.

Hallazgo: de los 112 locales marcados NO_REMOTE, 91 SI existen en GitHub
(perdieron la config del remoto) y 21 son subcarpetas anidadas dentro de
otro repo, no proyectos reales.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")
HOME = Path.home()


def git(repo, *args, timeout=60):
    try:
        p = subprocess.run(["git", "-C", str(repo), *args],
                           capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace",
                           env={"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", str(e)


def es_anidado(p: Path) -> Path | None:
    padre = p.parent
    for _ in range(4):
        if (padre / ".git").exists():
            return padre
        if padre == padre.parent:
            break
        padre = padre.parent
    return None


def main():
    estado = json.loads((OUT / "estado.json").read_text(encoding="utf-8"))
    faltan = set(json.loads((OUT / "sin-remoto-crear.json").read_text(encoding="utf-8")))
    reconectar = set(json.loads((OUT / "sin-remoto-reconectar.json").read_text(encoding="utf-8")))

    sin_remoto = [x for x in estado if x["verdict"] == "NO_REMOTE"]

    # --- Clasificar los 21 ---
    reales, anidados = [], []
    for s in sin_remoto:
        if s["name"] not in faltan:
            continue
        p = Path(s["path"])
        if es_anidado(p):
            anidados.append(s)
        else:
            reales.append(s)

    t = Table(title="Clasificacion de los 112 sin remoto", border_style="cyan")
    t.add_column("Categoria")
    t.add_column("N", justify="right")
    t.add_column("Accion")
    t.add_row("[green]Existen en GitHub[/]", str(len(reconectar)), "reconectar remoto")
    t.add_row("[yellow]Subcarpetas anidadas[/]", str(len(anidados)), "ignorar (no son proyectos)")
    t.add_row("[red]Proyectos reales sin repo[/]", str(len(reales)), "crear + push")
    console.print(t)

    # --- Reconectar los 91 ---
    console.print("\n[bold]Reconectando los que existen en GitHub...[/]")
    ok, fallo, ya = 0, 0, 0
    resultados = []
    inv = json.loads((OUT / "github-inventario.json").read_text(encoding="utf-8"))
    por_nombre = {x["name"].lower(): x for x in inv}

    for s in sin_remoto:
        if s["name"] not in reconectar:
            continue
        p = Path(s["path"])
        gh = por_nombre.get(s["name"].lower())
        if not gh:
            continue
        url = f"https://github.com/belentani7/{gh['name']}.git"
        code, out, err = git(p, "remote", "add", "origin", url)
        if code != 0 and "already exists" in err:
            code, out, err = git(p, "remote", "set-url", "origin", url)
        if code == 0:
            ok += 1
            resultados.append({"name": s["name"], "url": url, "estado": "reconectado"})
        else:
            fallo += 1
            resultados.append({"name": s["name"], "url": url, "estado": f"fallo: {err[:60]}"})

    console.print(f"  [green]reconectados: {ok}[/]   [red]fallos: {fallo}[/]")

    (OUT / "reconexion.json").write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "anidados-ignorar.json").write_text(
        json.dumps([x["path"] for x in anidados], indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "reales-sin-repo.json").write_text(
        json.dumps([{"name": x["name"], "path": x["path"]} for x in reales],
                   indent=2, ensure_ascii=False), encoding="utf-8")

    if reales:
        console.print("\n[red]Proyectos reales sin repo en GitHub:[/]")
        for x in reales:
            console.print(f"   {x['name']:<24} {x['path'].replace(str(HOME),'~')[:70]}")
    if anidados:
        console.print("\n[yellow]Subcarpetas anidadas (se ignoran):[/]")
        for x in anidados[:10]:
            console.print(f"   {x['name']:<20} {x['path'].replace(str(HOME),'~')[:70]}")


if __name__ == "__main__":
    main()
