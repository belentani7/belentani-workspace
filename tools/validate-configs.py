#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
validate-configs.py - Cruza los modelos configurados en cada CLI contra los
catalogos REALES de cada proveedor. Detecta modelos inexistentes y claves muertas.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
HOME = Path.home()


def get_key(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def or_key():
    return get_key("OPENROUTER_API_KEY")


# --- 1. Probar las 4 claves de OpenRouter ------------------------------
def test_openrouter_keys():
    t = Table(title="Claves OpenRouter", border_style="cyan")
    t.add_column("Variable")
    t.add_column("Estado")
    t.add_column("Credito/uso", max_width=30)
    for name in ["OPENROUTER_API_KEY", "OPENROUTER_KEY_1", "OPENROUTER_KEY_2", "OPENROUTER_KEY_3", "OPENROUTER_KEY_4"]:
        k = get_key(name)
        if not k:
            t.add_row(name, "[dim]ausente[/]", "")
            continue
        try:
            r = httpx.get("https://openrouter.ai/api/v1/key",
                          headers={"Authorization": f"Bearer {k}"}, timeout=25)
            if r.status_code == 200:
                d = r.json().get("data", {})
                lim = d.get("limit")
                used = d.get("usage", 0)
                free = d.get("is_free_tier")
                info = f"uso={used}"
                if lim is not None:
                    info += f" / limite={lim}"
                t.add_row(name, "[green]VALIDA[/]", f"{info} free_tier={free}")
            else:
                t.add_row(name, "[red]MUERTA[/]", f"HTTP {r.status_code}")
        except Exception as e:  # noqa: BLE001
            t.add_row(name, "[red]ERROR[/]", str(e)[:40])
    console.print(t)


# --- 2. Catalogos reales ----------------------------------------------
def catalog_openrouter() -> set[str]:
    k = or_key()
    r = httpx.get("https://openrouter.ai/api/v1/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json()["data"]}


def catalog_groq() -> set[str]:
    k = get_key("GROQ_API_KEY")
    r = httpx.get("https://api.groq.com/openai/v1/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json()["data"]}


def catalog_zai() -> set[str]:
    k = get_key("Z_AI_API_KEY") or get_key("ZAI_API_KEY")
    r = httpx.get("https://api.z.ai/api/paas/v4/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json().get("data", [])}


def catalog_nvidia() -> set[str]:
    k = get_key("NVIDIA_API_KEY")
    r = httpx.get("https://integrate.api.nvidia.com/v1/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json()["data"]}


def catalog_cerebras() -> set[str]:
    k = get_key("CEREBRAS_API_KEY")
    r = httpx.get("https://api.cerebras.ai/v1/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json()["data"]}


def catalog_deepseek() -> set[str]:
    k = get_key("DEEPSEEK_API_KEY")
    r = httpx.get("https://api.deepseek.com/models",
                  headers={"Authorization": f"Bearer {k}"}, timeout=30)
    return {m["id"] for m in r.json()["data"]}


def main():
    console.rule("[bold]1. Claves OpenRouter")
    test_openrouter_keys()

    console.rule("[bold]2. Catalogos reales")
    cats: dict[str, set[str]] = {}
    for name, fn in [("openrouter", catalog_openrouter), ("groq", catalog_groq),
                     ("zai", catalog_zai), ("nvidia", catalog_nvidia),
                     ("cerebras", catalog_cerebras), ("deepseek", catalog_deepseek)]:
        try:
            cats[name] = fn()
            console.print(f"  [green]{name:<12}[/] {len(cats[name]):>4} modelos")
        except Exception as e:  # noqa: BLE001
            console.print(f"  [red]{name:<12} FALLO: {e}[/]")

    # --- 3. Validar modelos configurados ---
    console.rule("[bold]3. Modelos configurados vs catalogo")
    problems: list[tuple[str, str, str]] = []
    ok: list[tuple[str, str]] = []

    # codex
    codex = HOME / ".codex" / "config.toml"
    if codex.exists():
        txt = codex.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'^model\s*=\s*"([^"]+)"', txt, re.M)
        if m:
            model = m.group(1)
            if model in cats.get("zai", set()):
                ok.append(("codex", model))
            else:
                problems.append(("codex", model,
                                 f"no existe en Z.AI ({len(cats.get('zai',[]))} modelos)"))

    # opencode
    oc = HOME / ".config" / "opencode" / "opencode.jsonc"
    if oc.exists():
        txt = oc.read_text(encoding="utf-8", errors="replace")
        # jsonc -> json: solo comentarios al inicio de linea (no romper https://)
        txt = re.sub(r"(?m)^\s*//.*$", "", txt)
        txt = re.sub(r",(\s*[}\]])", r"\1", txt)
        try:
            cfg = json.loads(txt)
            for prov, pcfg in (cfg.get("provider") or {}).items():
                for mid in ((pcfg or {}).get("models") or {}):
                    base = {"openrouter-free": "openrouter", "groq": "groq",
                            "cerebras": "cerebras", "deepseek": "deepseek"}.get(prov)
                    if base and base in cats:
                        if mid not in cats[base] and mid != "openrouter/free":
                            problems.append((f"opencode/{prov}", mid, f"no existe en {base}"))
                        else:
                            ok.append((f"opencode/{prov}", mid))
        except json.JSONDecodeError as e:
            problems.append(("opencode", "config", f"JSON invalido: {e}"))

    # groq models referenced in codex
    if "groq" in cats:
        pass

    t = Table(title="Resultado", border_style="cyan")
    t.add_column("Origen")
    t.add_column("Modelo")
    t.add_column("Problema")
    for src, model, why in problems:
        t.add_row(src, model, f"[red]{why}[/]")
    if not problems:
        t.add_row("[green]todo correcto[/]", "", "")
    console.print(t)

    console.print(f"\n[green]Validos: {len(ok)}[/]   [red]Rotos: {len(problems)}[/]")
    Path(r"C:\Users\USER\Desktop\produccion\config-validation.json").write_text(
        json.dumps({"ok": ok, "problems": problems, "catalogs":
                    {k: sorted(v) for k, v in cats.items()}},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    console.print("[green]Guardado: config-validation.json[/]")


if __name__ == "__main__":
    main()
