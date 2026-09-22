#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
limpiar-keys-file.py - Elimina falsos positivos del archivo consolidado.

Problema detectado: el extractor por regex capturaba SUBSTRINGS de claves
mas largas (p.ej. "sk-jdx4x38..." dentro de "csk-jdx4x38..."). Este script
elimina cualquier valor que sea subcadena estricta de otro.
"""
from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
F = Path.home() / "Desktop" / "API-KEYS-TODAS.txt"
txt = F.read_text(encoding="utf-8", errors="replace")

# Reconstruir: bloques de (nombre, valor, fuente)
bloques = []
lineas = txt.splitlines()
i = 0
while i < len(lineas):
    l = lineas[i]
    if l.startswith("  ") and not l.startswith("      ") and l.strip() and not l.startswith("  ==="):
        nombre = l.strip()
        if i + 2 < len(lineas):
            vline = lineas[i + 1]
            fline = lineas[i + 2]
            if vline.startswith("      ") and fline.strip().startswith("fuente:"):
                bloques.append({
                    "nombre": nombre,
                    "valor": vline.strip(),
                    "fuente": fline.strip().replace("fuente:", "").strip(),
                })
    i += 1

console.print(f"Bloques leidos: {len(bloques)}")

# --- 1. Eliminar subcadenas -------------------------------------------------
valores = {b["valor"] for b in bloques}
subcadenas = set()
for v in valores:
    for w in valores:
        if v != w and v in w:
            subcadenas.add(v)
            break

limpios = [b for b in bloques if b["valor"] not in subcadenas]
console.print(f"[yellow]Subcadenas eliminadas:[/] {len(subcadenas)}")

# --- 2. Deduplicar por valor ------------------------------------------------
vistos = {}
for b in limpios:
    if b["valor"] not in vistos:
        vistos[b["valor"]] = b
    else:
        # conservar el nombre mas informativo
        if len(b["nombre"]) > len(vistos[b["valor"]]["nombre"]):
            vistos[b["valor"]] = b
finales = list(vistos.values())
console.print(f"[green]Claves unicas finales:[/] {len(finales)}")

# --- 3. Reescribir ----------------------------------------------------------
def proveedor(valor: str) -> str:
    if valor.startswith("sk-or-v1"): return "OpenRouter"
    if valor.startswith("sk-ant"): return "Anthropic"
    if valor.startswith("gsk_"): return "Groq"
    if valor.startswith("csk-"): return "Cerebras"
    if valor.startswith("nvapi-"): return "NVIDIA"
    if valor.startswith("sk-mZA"): return "Morph"
    if valor.startswith("AIza"): return "Google/Gemini"
    if valor.startswith(("gho_", "ghp_", "ghu_", "ghs_", "ghr_")): return "GitHub"
    if valor.startswith("hf_"): return "HuggingFace"
    if valor.startswith("vca_"): return "Vercel"
    if re.fullmatch(r"[0-9a-f]{32}\..+", valor): return "Z.AI"
    if valor.startswith("sk-proj-"): return "OpenAI"
    if valor.startswith("sk-") and len(valor) == 35: return "DeepSeek"
    if valor.startswith("sk-"): return "Otros (sk-)"
    return "Otro"

for b in finales:
    b["prov"] = proveedor(b["valor"])

por_prov: dict[str, list] = {}
for b in finales:
    por_prov.setdefault(b["prov"], []).append(b)

from datetime import datetime
lineas_out = [
    "=" * 78,
    "  API KEYS - CONSOLIDADO (limpio)",
    f"  Generado: {datetime.now():%Y-%m-%d %H:%M}",
    f"  Claves unicas: {len(finales)}",
    "=" * 78,
    "",
    "  !! AVISO DE SEGURIDAD !!",
    "  Todas tus claves API en texto plano.",
    "  - NO subir a GitHub ni a la nube.",
    "  - NO dejar en carpetas sincronizadas (OneDrive/Drive).",
    "  - Si se filtra, ROTAR todas las claves.",
    "",
    "  Cargar en la sesion:  . C:\\Users\\USER\\.secrets\\vault\\load-env.ps1",
    "",
    "=" * 78,
    "",
]
for prov in sorted(por_prov, key=lambda p: (-len(por_prov[p]), p)):
    lineas_out.append(f"### {prov}  ({len(por_prov[prov])})")
    lineas_out.append("")
    for b in sorted(por_prov[prov], key=lambda x: x["nombre"]):
        lineas_out.append(f"  {b['nombre']}")
        lineas_out.append(f"      {b['valor']}")
        lineas_out.append(f"      fuente: {b['fuente']}")
        lineas_out.append("")
    lineas_out.append("")

F.write_text("\n".join(lineas_out), encoding="utf-8")

t = Table(title="Archivo consolidado LIMPIO", border_style="cyan")
t.add_column("Proveedor")
t.add_column("N", justify="right")
for p in sorted(por_prov, key=lambda x: -len(por_prov[x])):
    t.add_row(p, str(len(por_prov[p])))
console.print(t)
console.print(f"\n[green]Archivo:[/] {F}  ({F.stat().st_size:,} bytes)")
console.print(f"[green]Antes:[/] {len(bloques)} entradas  ->  [green]Ahora:[/] {len(finales)} unicas")
