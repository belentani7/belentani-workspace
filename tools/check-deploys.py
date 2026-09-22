#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check-deploys.py - Verifica el estado REAL de todos los deploys.
Cruza los listados de Netlify y Cloudflare Pages con una comprobacion HTTP.
"""
from __future__ import annotations

import json
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")


def check(url: str) -> tuple[str, int, str]:
    """Devuelve (estado, http_code, nota)."""
    if not url:
        return ("sin-url", 0, "")
    try:
        r = httpx.get(url, timeout=25, follow_redirects=True)
        code = r.status_code
        if code == 200:
            n = len(r.content)
            return ("VIVO", code, f"{n//1024} KB")
        if code in (401, 403):
            return ("PROTEGIDO", code, "requiere auth")
        if code == 404:
            return ("404", code, "no encontrado")
        return ("RARO", code, r.reason_phrase or "")
    except httpx.ConnectError:
        return ("NO RESUELVE", 0, "DNS/red")
    except httpx.TimeoutException:
        return ("TIMEOUT", 0, "")
    except Exception as e:  # noqa: BLE001
        return ("ERROR", 0, str(e)[:30])


def main():
    results = []

    # --- NETLIFY ---
    nf = OUT / "netlify-sites.json"
    if nf.exists():
        try:
            sites = json.loads(nf.read_text(encoding="utf-8"))
            console.print(f"[cyan]Netlify:[/] {len(sites)} sitios")
            for s in sites:
                pub = s.get("published_deploy") or {}
                url = s.get("ssl_url") or s.get("url") or ""
                state, code, note = check(url)
                err = pub.get("error_message") or s.get("error_message") or ""
                results.append({
                    "plataforma": "netlify", "nombre": s.get("name"),
                    "url": url, "estado": state, "http": code, "nota": note,
                    "deploy_state": pub.get("state") or s.get("state") or "",
                    "error": err,
                    "framework": pub.get("framework") or "",
                    "actualizado": (pub.get("published_at") or "")[:10],
                    "repo": (s.get("build_settings") or {}).get("repo_path") or "",
                })
        except Exception as e:  # noqa: BLE001
            console.print(f"[red]Netlify: error parseando: {e}[/]")

    # --- CLOUDFLARE PAGES ---
    cf = OUT / "cf-pages.json"
    if cf.exists():
        try:
            txt = cf.read_text(encoding="utf-8")
            # wrangler puede emitir avisos antes del JSON
            start = txt.find("[")
            projects = json.loads(txt[start:]) if start >= 0 else []
            console.print(f"[cyan]Cloudflare Pages:[/] {len(projects)} proyectos")
            for p in projects:
                # wrangler --json usa claves display ("Project Name", "Project Domains")
                name = p.get("name") or p.get("project_name") or p.get("Project Name") or "?"
                raw_domains = p.get("domains") or p.get("Project Domains") or []
                if isinstance(raw_domains, str):
                    domains = [d.strip() for d in raw_domains.split(",") if d.strip()]
                else:
                    domains = raw_domains
                url = ""
                for d in domains:
                    if isinstance(d, str) and d.endswith(".pages.dev"):
                        url = f"https://{d}"
                        break
                if not url:
                    url = f"https://{name}.pages.dev"
                state, code, note = check(url)
                results.append({
                    "plataforma": "cloudflare", "nombre": name,
                    "url": url, "estado": state, "http": code, "nota": note,
                    "deploy_state": "",
                    "error": "",
                    "framework": "",
                    "actualizado": str(p.get("Last Modified") or p.get("created_on") or "")[:10],
                    "repo": "",
                })
        except Exception as e:  # noqa: BLE001
            console.print(f"[red]Cloudflare: error parseando: {e}[/]")

    # --- Tabla ---
    t = Table(title="Estado de deploys", border_style="cyan")
    t.add_column("Plataforma", max_width=11)
    t.add_column("Proyecto", max_width=26)
    t.add_column("Estado")
    t.add_column("HTTP", justify="right")
    t.add_column("Nota", max_width=18)
    t.add_column("URL", max_width=38)

    color = {"VIVO": "green", "PROTEGIDO": "yellow", "404": "red",
             "NO RESUELVE": "red", "TIMEOUT": "red", "ERROR": "red", "RARO": "yellow"}
    for r in sorted(results, key=lambda x: (x["estado"] != "VIVO", x["plataforma"], x["nombre"] or "")):
        c = color.get(r["estado"], "white")
        t.add_row(r["plataforma"], (r["nombre"] or "")[:26],
                  f"[{c}]{r['estado']}[/]", str(r["http"]), r["nota"][:18],
                  r["url"].replace("https://", "")[:38])
    console.print(t)

    (OUT / "deploys-estado.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Resumen
    console.print()
    counts: dict[str, int] = {}
    for r in results:
        counts[r["estado"]] = counts.get(r["estado"], 0) + 1
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        col = color.get(k, "white")
        console.print(f"  [{col}]{k:<12}[/] {v}")
    console.print(f"\n  Total: {len(results)}")

    rotos = [r for r in results if r["estado"] in ("404", "NO RESUELVE", "TIMEOUT", "ERROR")]
    if rotos:
        console.print(f"\n[red]DEPLOYS ROTOS ({len(rotos)}):[/]")
        for r in rotos:
            console.print(f"   {r['plataforma']:<11} {r['nombre'][:30]:<30} {r['url']}")


if __name__ == "__main__":
    main()
