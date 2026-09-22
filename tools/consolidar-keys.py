#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
consolidar-keys.py - Reune TODAS las API keys del sistema en un solo archivo
en el Escritorio, tal como pidio el usuario.

Fuentes:
  1. Variables de entorno de usuario (registro)
  2. ~/.secrets/vault/*.env y *.txt
  3. Configs de CLIs: zcode, autoclaw, codex, continue, openclaw
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
HOME = Path.home()
DEST = HOME / "Desktop" / "API-KEYS-TODAS.txt"

# Patrones de VALOR de clave
PATTERNS = [
    ("OpenRouter", re.compile(r"sk-or-v1-[A-Za-z0-9]{32,}")),
    ("Anthropic", re.compile(r"sk-ant-[A-Za-z0-9\-_]{30,}")),
    ("OpenAI/DeepSeek", re.compile(r"sk-(?!or-|ant-|mZA)[A-Za-z0-9]{28,}")),
    ("Google/Gemini", re.compile(r"AIza[A-Za-z0-9\-_]{30,}")),
    ("Groq", re.compile(r"gsk_[A-Za-z0-9]{40,}")),
    ("Cerebras", re.compile(r"csk-[A-Za-z0-9]{40,}")),
    ("NVIDIA", re.compile(r"nvapi-[A-Za-z0-9\-_]{40,}")),
    ("Morph", re.compile(r"sk-mZA[A-Za-z0-9\-_]{20,}")),
    ("GitHub", re.compile(r"gh[opusr]_[A-Za-z0-9]{30,}")),
    ("HuggingFace", re.compile(r"hf_[A-Za-z0-9]{30,}")),
    ("Z.AI", re.compile(r"[0-9a-f]{32}\.[A-Za-z0-9_\-]{12,}")),
    ("Vercel", re.compile(r"vca_[A-Za-z0-9]{20,}")),
]


def get_user_env() -> dict[str, str]:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariables('User').GetEnumerator() | "
         "ForEach-Object { \"$($_.Key)=$($_.Value)\" }"],
        capture_output=True, text=True, timeout=30)
    out = {}
    for line in (p.stdout or "").splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip()
            if k and v:
                out[k] = v
    return out


def main():
    found: dict[str, dict] = {}   # nombre -> {valor, fuente, tipo}

    def add(nombre: str, valor: str, fuente: str):
        if not valor or valor.startswith("[") or "ELIMINADA" in valor.upper():
            return
        if nombre not in found:
            found[nombre] = {"valor": valor, "fuente": fuente}

    # --- 1. Variables de entorno de usuario ---
    uenv = get_user_env()
    for k, v in uenv.items():
        if re.search(r"KEY|TOKEN|SECRET", k, re.I):
            add(k, v, "env:usuario")

    # --- 2. Ficheros de .secrets/vault ---
    vault = HOME / ".secrets" / "vault"
    if vault.exists():
        for f in list(vault.glob("*.env")) + list(vault.glob("*.txt")) + list(vault.glob("*.json")):
            if "QUARANTINE" in f.name or f.stat().st_size > 3_000_000:
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            # pares NOMBRE=valor
            for m in re.finditer(r"(?m)^([A-Z][A-Z0-9_]{3,})\s*=\s*(\S{16,})", txt):
                add(m.group(1), m.group(2), f"vault/{f.name}")
            # valores sueltos por patron
            for tipo, pat in PATTERNS:
                for m in pat.finditer(txt):
                    add(f"{tipo}_{m.group(0)[:8]}", m.group(0), f"vault/{f.name}")

    # --- 3. Configs de CLIs ---
    configs = {
        HOME / ".zcode/v2/config.json": "zcode",
        HOME / ".openclaw-autoclaw/openclaw.json": "autoclaw",
        HOME / ".codex/config.toml": "codex",
        HOME / ".continue/.env": "continue",
        HOME / ".aider.conf.yml": "aider",
    }
    for path, nombre in configs.items():
        if not path.exists():
            continue
        try:
            txt = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for tipo, pat in PATTERNS:
            for m in pat.finditer(txt):
                add(f"{tipo}_{nombre}", m.group(0), nombre)

    # --- 4. Clasificar por proveedor ---
    def proveedor(nombre: str, valor: str) -> str:
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
        if valor.startswith("sk-"): return "DeepSeek/OpenAI"
        if re.fullmatch(r"[0-9a-f]{32}\..+", valor): return "Z.AI"
        return "Otro"

    for v in found.values():
        v["prov"] = proveedor("", v["valor"])

    # --- 5. Escribir el archivo ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = [
        "=" * 78,
        "  API KEYS - CONSOLIDADO",
        f"  Generado: {now}",
        "=" * 78,
        "",
        "  !! AVISO DE SEGURIDAD !!",
        "  Este archivo contiene TODAS tus claves API en texto plano.",
        "  - NO lo subas a GitHub ni a ninguna nube.",
        "  - NO lo dejes en carpetas sincronizadas (OneDrive/Drive).",
        "  - Si lo compartes o lo pierdes, ROTA todas las claves.",
        "",
        f"  Claves encontradas: {len(found)}",
        "",
        "=" * 78,
        "",
    ]

    por_prov: dict[str, list] = {}
    for nombre, v in found.items():
        por_prov.setdefault(v["prov"], []).append((nombre, v))

    for prov in sorted(por_prov):
        lineas.append(f"### {prov}  ({len(por_prov[prov])})")
        lineas.append("")
        for nombre, v in sorted(por_prov[prov]):
            lineas.append(f"  {nombre}")
            lineas.append(f"      {v['valor']}")
            lineas.append(f"      fuente: {v['fuente']}")
            lineas.append("")
        lineas.append("")

    lineas += [
        "=" * 78,
        "  COMO USARLAS",
        "=" * 78,
        "",
        "  En PowerShell, carga todas de golpe:",
        "      . C:\\Users\\USER\\.secrets\\vault\\load-env.ps1",
        "",
        "  O usa los atajos del perfil:",
        "      load-keys      # carga las claves en la sesion",
        "      keys-check     # prueba inferencia en los free tiers",
        "      prod-keys      # prueba que las claves responden",
        "",
        "=" * 78,
    ]

    DEST.write_text("\n".join(lineas), encoding="utf-8")

    t = Table(title="Claves consolidadas por proveedor", border_style="cyan")
    t.add_column("Proveedor")
    t.add_column("N", justify="right")
    for prov in sorted(por_prov, key=lambda x: -len(por_prov[x])):
        t.add_row(prov, str(len(por_prov[prov])))
    console.print(t)
    console.print(f"\n[green]Archivo creado:[/] {DEST}")
    console.print(f"[green]Total de claves:[/] {len(found)}")

    # --- 6. Proteger el archivo ---
    subprocess.run(["icacls", str(DEST), "/inheritance:r",
                    "/grant:r", f"{HOME.name}:(R,W)"],
                   capture_output=True, text=True)
    console.print("[green]Permisos restringidos a tu usuario.[/]")


if __name__ == "__main__":
    main()
