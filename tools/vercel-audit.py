#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vercel-audit.py - Auditoria del proyecto Vercel via API:
  - Uso de almacenamiento
  - Proyectos sin deploy de produccion
  - Deploys antiguos que se pueden borrar
"""
from __future__ import annotations

import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")
UA = {"User-Agent": "vercel-audit/1.0"}


def token() -> str:
    t = os.environ.get("VERCEL_TOKEN")
    if t:
        return t
    p = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "[Environment]::GetEnvironmentVariable('VERCEL_TOKEN','User')"],
                       capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


TOK = token()
H = {**UA, "Authorization": f"Bearer {TOK}"}


def get(url, **kw):
    r = httpx.get(url, headers=H, timeout=45, **kw)
    return r


def main():
    if not TOK:
        console.print("[red]Sin VERCEL_TOKEN[/]")
        return
    console.print(f"[green]Token OK[/] ({TOK[:10]}...)")

    # --- Proyectos ---
    proyectos = []
    hasta = None
    while True:
        params = {"limit": 100}
        if hasta:
            params["until"] = hasta
        r = get("https://api.vercel.com/v9/projects", params=params)
        if r.status_code != 200:
            console.print(f"[red]projects HTTP {r.status_code}: {r.text[:150]}[/]")
            break
        d = r.json()
        proyectos.extend(d.get("projects", []))
        hasta = (d.get("pagination") or {}).get("next")
        if not hasta or len(proyectos) > 400:
            break

    console.print(f"[cyan]Proyectos en Vercel:[/] {len(proyectos)}")

    con_prod = []
    sin_prod = []
    for p in proyectos:
        # latest deployments
        r = get(f"https://api.vercel.com/v6/deployments",
                params={"projectId": p["id"], "limit": 20, "target": "production"})
        deps = r.json().get("deployments", []) if r.status_code == 200 else []
        if deps:
            con_prod.append((p, deps))
        else:
            sin_prod.append(p)

    t = Table(title="Estado de deploys de produccion", border_style="cyan")
    t.add_column("Categoria")
    t.add_column("N", justify="right")
    t.add_row("[green]Con deploy de produccion[/]", str(len(con_prod)))
    t.add_row("[red]SIN deploy de produccion[/]", str(len(sin_prod)))
    console.print(t)

    (OUT / "vercel-proyectos.json").write_text(json.dumps(
        [{"name": p.get("name"), "id": p["id"],
          "framework": p.get("framework"),
          "repo": (p.get("link") or {}).get("repo"),
          "produccion": bool([d for pp, dd in con_prod if pp["id"] == p["id"] for d in dd]),
          "updated": p.get("updatedAt")} for p in proyectos],
        indent=2, ensure_ascii=False), encoding="utf-8")

    if sin_prod:
        console.print(f"\n[red]SIN deploy de produccion ({len(sin_prod)}):[/]")
        for p in sorted(sin_prod, key=lambda x: x.get("name", "")):
            repo = (p.get("link") or {}).get("repo") or "(sin repo)"
            console.print(f"   {p.get('name','?'):<42} {repo}")

    # --- Deploys antiguos (candidatos a borrar para liberar storage) ---
    console.print("\n[bold]Analizando almacenamiento de deploys...[/]")
    total = 0
    antiguos = []
    for p in proyectos[:60]:
        r = get("https://api.vercel.com/v6/deployments",
                params={"projectId": p["id"], "limit": 100})
        if r.status_code != 200:
            continue
        for d in r.json().get("deployments", []):
            total += 1
            if d.get("state") == "READY" and not d.get("target"):
                antiguos.append((p.get("name"), d.get("uid"), d.get("created")))

    console.print(f"  deploys analizados: {total}")
    console.print(f"  previews antiguos (candidatos a purgar): {len(antiguos)}")


if __name__ == "__main__":
    main()
