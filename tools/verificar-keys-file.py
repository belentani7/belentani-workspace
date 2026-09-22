#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verificar-keys-file.py - Comprueba que el archivo consolidado no tenga basura."""
import re
import subprocess
from collections import Counter
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
F = Path.home() / "Desktop" / "API-KEYS-TODAS.txt"

txt = F.read_text(encoding="utf-8", errors="replace")

# Extraer las lineas de valor (las que van indentadas con 6 espacios)
valores = []
for line in txt.splitlines():
    s = line.strip()
    if line.startswith("      ") and len(s) > 20 and " " not in s and "fuente" not in s:
        valores.append(s)

console.print(f"[cyan]Valores en el archivo:[/] {len(valores)}")
console.print(f"[cyan]Unicos:[/] {len(set(valores))}")

# Detectar duplicados
dups = [v for v, n in Counter(valores).items() if n > 1]
console.print(f"[yellow]Duplicados:[/] {len(dups)}")

# Clasificar y comprobar los sospechosos
t = Table(title="Comprobacion de claves", border_style="cyan")
t.add_column("Prefijo")
t.add_column("N", justify="right")
t.add_column("Comprobacion", max_width=40)

grupos = Counter()
for v in set(valores):
    if v.startswith("sk-or-v1"): grupos["sk-or-v1 (OpenRouter)"] += 1
    elif v.startswith("sk-ant"): grupos["sk-ant (Anthropic)"] += 1
    elif v.startswith("sk-mZA"): grupos["sk-mZA (Morph)"] += 1
    elif v.startswith("gsk_"): grupos["gsk_ (Groq)"] += 1
    elif v.startswith("csk-"): grupos["csk- (Cerebras)"] += 1
    elif v.startswith("nvapi-"): grupos["nvapi- (NVIDIA)"] += 1
    elif v.startswith("AIza"): grupos["AIza (Google)"] += 1
    elif v.startswith(("gho_", "ghp_", "ghu_", "ghs_")): grupos["gh*_ (GitHub)"] += 1
    elif v.startswith("hf_"): grupos["hf_ (HuggingFace)"] += 1
    elif v.startswith("vca_"): grupos["vca_ (Vercel)"] += 1
    elif re.fullmatch(r"[0-9a-f]{32}\..+", v): grupos["hex32.x (Z.AI)"] += 1
    elif v.startswith("sk-"): grupos["sk- generico (DeepSeek/OpenAI)"] += 1
    else: grupos[f"OTRO: {v[:12]}..."] += 1

for k, n in grupos.most_common():
    t.add_row(k, str(n), "")
console.print(t)

# Probar una muestra de cada grupo contra su API
console.print("\n[bold]Probando una muestra de cada grupo...[/]")
PRUEBAS = {
    "sk-or-v1": ("https://openrouter.ai/api/v1/key", "bearer"),
    "sk-ant": ("https://api.anthropic.com/v1/models", "anthropic"),
    "gsk_": ("https://api.groq.com/openai/v1/models", "bearer"),
    "csk-": ("https://api.cerebras.ai/v1/models", "bearer"),
    "nvapi-": ("https://integrate.api.nvidia.com/v1/models", "bearer"),
    "AIza": ("https://generativelanguage.googleapis.com/v1beta/models", "query"),
    "sk-mZA": ("https://api.morphllm.com/v1/models", "bearer"),
    "hf_": ("https://huggingface.co/api/models?limit=1", "bearer"),
}

vistos = set()
for v in sorted(set(valores)):
    pref = next((p for p in PRUEBAS if v.startswith(p)), None)
    if not pref or pref in vistos:
        continue
    vistos.add(pref)
    url, modo = PRUEBAS[pref]
    try:
        if modo == "bearer":
            r = httpx.get(url, headers={"Authorization": f"Bearer {v}"}, timeout=25)
        elif modo == "anthropic":
            r = httpx.get(url, headers={"x-api-key": v, "anthropic-version": "2023-06-01"}, timeout=25)
        else:
            r = httpx.get(url, params={"key": v}, timeout=25)
        estado = "[green]VALIDA[/]" if r.status_code == 200 else f"[red]HTTP {r.status_code}[/]"
        console.print(f"  {pref:<12} {estado}")
    except Exception as e:  # noqa: BLE001
        console.print(f"  {pref:<12} [red]error[/] {str(e)[:40]}")

console.print(f"\n[green]Archivo:[/] {F}  ({F.stat().st_size:,} bytes)")
