#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""list-free.py - Enumera modelos gratuitos reales por proveedor."""
import json
import subprocess
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


def get_key(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def main():
    out = {}

    k = get_key("OPENROUTER_API_KEY")
    if k:
        r = httpx.get("https://openrouter.ai/api/v1/models",
                      headers={"Authorization": f"Bearer {k}"}, timeout=30)
        free = []
        for m in r.json()["data"]:
            pr = m.get("pricing", {})
            try:
                if float(pr.get("prompt", 1)) == 0 and float(pr.get("completion", 1)) == 0:
                    free.append((m["id"], m.get("context_length", 0)))
            except (TypeError, ValueError):
                continue
        out["openrouter_free"] = [f[0] for f in free]
        t = Table(title=f"OpenRouter - {len(free)} modelos GRATIS", border_style="green")
        t.add_column("Modelo")
        t.add_column("Contexto", justify="right")
        for mid, ctx in sorted(free):
            t.add_row(mid, f"{ctx:,}")
        console.print(t)

    k2 = get_key("GROQ_API_KEY")
    if k2:
        r2 = httpx.get("https://api.groq.com/openai/v1/models",
                       headers={"Authorization": f"Bearer {k2}"}, timeout=30)
        models = sorted(m["id"] for m in r2.json()["data"])
        out["groq"] = models
        t2 = Table(title=f"Groq - {len(models)} modelos (free tier)", border_style="cyan")
        t2.add_column("Modelo")
        for m in models:
            t2.add_row(m)
        console.print(t2)

    k3 = get_key("NVIDIA_API_KEY")
    if k3:
        r3 = httpx.get("https://integrate.api.nvidia.com/v1/models",
                       headers={"Authorization": f"Bearer {k3}"}, timeout=30)
        ids = sorted(m["id"] for m in r3.json()["data"])
        out["nvidia"] = ids
        console.print(f"\n[cyan]NVIDIA NIM: {len(ids)} modelos[/] (free credits)")
        for i in ids[:20]:
            console.print(f"   {i}")

    k4 = get_key("Z_AI_API_KEY") or get_key("ZAI_API_KEY")
    if k4:
        r4 = httpx.get("https://api.z.ai/api/paas/v4/models",
                       headers={"Authorization": f"Bearer {k4}"}, timeout=30)
        ids = sorted(m["id"] for m in r4.json().get("data", []))
        out["zai"] = ids
        console.print(f"\n[cyan]Z.AI GLM: {len(ids)} modelos[/]")
        for i in ids:
            console.print(f"   {i}")

    Path(r"C:\Users\USER\Desktop\produccion\free-models.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    console.print("\n[green]Guardado: free-models.json[/]")


if __name__ == "__main__":
    main()
