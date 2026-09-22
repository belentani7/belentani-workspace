#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vercel-fix-masivo.py - Busca proyectos Vercel con builds rotos por ramas
de salida (gh-pages) y aplica el mismo fix que en aprende-brasil.
"""
from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")


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
COMANDO = 'if [ "$VERCEL_GIT_COMMIT_REF" = "gh-pages" ]; then exit 0; else exit 1; fi'


def main():
    # Proyectos
    proys, hasta = [], None
    while True:
        params = {"limit": 100}
        if hasta:
            params["until"] = hasta
        r = httpx.get("https://api.vercel.com/v9/projects", headers=H,
                      params=params, timeout=45)
        if r.status_code != 200:
            break
        d = r.json()
        proys.extend(d.get("projects", []))
        hasta = (d.get("pagination") or {}).get("next")
        if not hasta or len(proys) > 400:
            break
    console.print(f"[cyan]Proyectos:[/] {len(proys)}")

    # Analizar deploys fallidos por rama
    fallos_rama = Counter()
    afectados = []
    for i, p in enumerate(proys, 1):
        if i % 20 == 0:
            console.print(f"  ...{i}/{len(proys)}", style="dim")
        r = httpx.get("https://api.vercel.com/v6/deployments", headers=H,
                      params={"projectId": p["id"], "limit": 30}, timeout=45)
        if r.status_code != 200:
            continue
        deps = r.json().get("deployments", [])
        malas = [d for d in deps if d.get("state") == "ERROR"]
        if not malas:
            continue
        ramas = Counter((d.get("meta") or {}).get("githubCommitRef") or "?"
                        for d in malas)
        for rama, n in ramas.items():
            fallos_rama[rama] += n
        # si TODOS los fallos vienen de ramas que no son la de produccion
        rama_prod = (p.get("link") or {}).get("productionBranch") or "main"
        culpables = [r_ for r_ in ramas if r_ not in (rama_prod, "main", "master")]

        # errores tipo "exited with 127" = comando no encontrado
        err127 = [d for d in malas
                  if "127" in ((d.get("errorMessage") or ""))]
        afectados.append({
            "name": p.get("name"), "id": p["id"],
            "rama_prod": rama_prod,
            "ramas_fallidas": dict(ramas),
            "culpables": culpables,
            "n_fallos": len(malas),
            "n_127": len(err127),
            "ignoredStep": p.get("commandForIgnoringBuildStep"),
        })

    t = Table(title="Ramas que generan builds fallidos", border_style="cyan")
    t.add_column("Rama")
    t.add_column("Builds fallidos", justify="right")
    for rama, n in fallos_rama.most_common(15):
        color = "red" if rama not in ("main", "master") else "yellow"
        t.add_row(f"[{color}]{rama}[/]", str(n))
    console.print(t)

    # Candidatos a fix: tienen fallos de 127 en ramas que no son produccion
    cand = [a for a in afectados if a["n_127"] > 0 and a["culpables"]
            and not a["ignoredStep"]]
    console.print(f"\n[bold]Candidatos a aplicar el fix ({len(cand)}):[/]")
    for a in sorted(cand, key=lambda x: -x["n_127"]):
        console.print(f"   {a['name'][:38]:<38} prod={a['rama_prod']:<8} "
                      f"fallos={a['n_127']:<4} ramas={list(a['ramas_fallidas'])[:3]}")

    (OUT / "vercel-builds-fallidos.json").write_text(
        json.dumps(afectados, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]Guardado: vercel-builds-fallidos.json[/]")

    # Aplicar el fix
    if cand:
        console.print(f"\n[bold]Aplicando el fix a {len(cand)} proyectos...[/]")
        ok = 0
        for a in cand:
            r = httpx.patch(f"https://api.vercel.com/v9/projects/{a['id']}",
                            headers=H, json={"commandForIgnoringBuildStep": COMANDO},
                            timeout=45)
            if r.status_code in (200, 201):
                ok += 1
                console.print(f"   [green]OK[/] {a['name']}")
            else:
                console.print(f"   [red]FALLO[/] {a['name']}: {r.text[:80]}")
        console.print(f"\n[green]Aplicado en {ok}/{len(cand)} proyectos[/]")
    else:
        console.print("\n[yellow]Ningun candidato nuevo que arreglar.[/]")


if __name__ == "__main__":
    main()
