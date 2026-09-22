#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test-keys.py - Comprueba que API keys del sistema funcionan de verdad.
Usa endpoints BARATOS (listado de modelos), no inferencia, para no gastar.
"""
from __future__ import annotations
import os, re, sys, json
from pathlib import Path
import httpx
from rich.console import Console
from rich.table import Table

console = Console()
ENV_FILE = Path(r"C:\Users\USER\.secrets\vault\cli-coders-pack.api-keys.env")


def load_keys() -> dict[str, str]:
    keys: dict[str, str] = {}
    # 1. Nivel usuario (registro)
    try:
        for k, v in os.environ.items():
            if re.search(r"KEY|TOKEN", k, re.I):
                keys[k] = v
    except Exception:
        pass
    try:
        import subprocess
        p = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "[Environment]::GetEnvironmentVariables('User').GetEnumerator() | "
             "ForEach-Object { \"$($_.Key)=$($_.Value)\" }"],
            capture_output=True, text=True, timeout=30)
        for line in p.stdout.splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                if re.search(r"KEY|TOKEN", k, re.I):
                    keys.setdefault(k.strip(), v.strip())
    except Exception:
        pass
    # 2. Fichero canonico (gana)
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            keys[k.strip()] = v.strip()
    return keys


# (nombre, url, header_fn, notas)
def build_tests(keys: dict[str, str]):
    def bearer(k):
        return lambda key: {"Authorization": f"Bearer {key}"}

    tests = []

    if keys.get("OPENROUTER_API_KEY"):
        tests.append(("OpenRouter", "https://openrouter.ai/api/v1/models",
                      bearer(keys["OPENROUTER_API_KEY"]), keys["OPENROUTER_API_KEY"]))
    if keys.get("GROQ_API_KEY"):
        tests.append(("Groq", "https://api.groq.com/openai/v1/models",
                      bearer(keys["GROQ_API_KEY"]), keys["GROQ_API_KEY"]))
    if keys.get("DEEPSEEK_API_KEY"):
        tests.append(("DeepSeek", "https://api.deepseek.com/models",
                      bearer(keys["DEEPSEEK_API_KEY"]), keys["DEEPSEEK_API_KEY"]))
    if keys.get("GEMINI_API_KEY"):
        tests.append(("Gemini", "https://generativelanguage.googleapis.com/v1beta/models",
                      None, keys["GEMINI_API_KEY"]))
    if keys.get("CEREBRAS_API_KEY"):
        tests.append(("Cerebras", "https://api.cerebras.ai/v1/models",
                      bearer(keys["CEREBRAS_API_KEY"]), keys["CEREBRAS_API_KEY"]))
    if keys.get("NVIDIA_API_KEY"):
        tests.append(("NVIDIA NIM", "https://integrate.api.nvidia.com/v1/models",
                      bearer(keys["NVIDIA_API_KEY"]), keys["NVIDIA_API_KEY"]))
    if keys.get("NVIDIA_ALT_KEY"):
        tests.append(("NVIDIA alt", "https://integrate.api.nvidia.com/v1/models",
                      bearer(keys["NVIDIA_ALT_KEY"]), keys["NVIDIA_ALT_KEY"]))
    if keys.get("Z_AI_API_KEY") or keys.get("ZAI_API_KEY"):
        zk = keys.get("Z_AI_API_KEY") or keys.get("ZAI_API_KEY")
        tests.append(("Z.AI (GLM)", "https://api.z.ai/api/paas/v4/models",
                      bearer(zk), zk))
    if keys.get("MORPH_API_KEY"):
        tests.append(("Morph", "https://api.morphllm.com/v1/models",
                      bearer(keys["MORPH_API_KEY"]), keys["MORPH_API_KEY"]))
    if keys.get("OPENCODE_ZEN_KEY"):
        tests.append(("OpenCode Zen", "https://opencode.ai/zen/v1/models",
                      bearer(keys["OPENCODE_ZEN_KEY"]), keys["OPENCODE_ZEN_KEY"]))
    if keys.get("OPENZEN_API_KEY"):
        tests.append(("OpenZen", "https://api.openzen.ai/v1/models",
                      bearer(keys["OPENZEN_API_KEY"]), keys["OPENZEN_API_KEY"]))
    if keys.get("HF_TOKEN"):
        tests.append(("HuggingFace", "https://huggingface.co/api/models?limit=1",
                      bearer(keys["HF_TOKEN"]), keys["HF_TOKEN"]))
    if keys.get("OPENAI_API_KEY"):
        tests.append(("OpenAI", "https://api.openai.com/v1/models",
                      bearer(keys["OPENAI_API_KEY"]), keys["OPENAI_API_KEY"]))
    if keys.get("ANTHROPIC_API_KEY"):
        tests.append(("Anthropic", "https://api.anthropic.com/v1/models",
                      lambda k: {"x-api-key": k, "anthropic-version": "2023-06-01"},
                      keys["ANTHROPIC_API_KEY"]))
    return tests


def main():
    keys = load_keys()
    console.print(f"[cyan]Claves cargadas:[/] {len(keys)}")
    tests = build_tests(keys)

    table = Table(title="Prueba de API keys (endpoints baratos)", border_style="cyan")
    table.add_column("Proveedor", style="bold")
    table.add_column("Estado")
    table.add_column("Detalle", max_width=46)

    results = {}
    for name, url, hdr, key in tests:
        if not key or "ELIMINADA" in key.upper() or key.startswith("["):
            table.add_row(name, "[dim]SALTADO[/]", "clave ausente o eliminada")
            results[name] = "skip"
            continue
        headers = hdr(key) if hdr else {}
        params = {"key": key} if name == "Gemini" else {}
        try:
            r = httpx.get(url, headers=headers, params=params, timeout=25)
            if r.status_code == 200:
                try:
                    data = r.json()
                    n = len(data.get("data") or data.get("models") or [])
                except Exception:
                    n = 0
                table.add_row(name, "[green]FUNCIONA[/]", f"{n} modelos" if n else "OK")
                results[name] = "ok"
            elif r.status_code in (401, 403):
                table.add_row(name, "[red]CLAVE INVALIDA[/]", f"HTTP {r.status_code}")
                results[name] = "invalid"
            elif r.status_code == 429:
                table.add_row(name, "[yellow]LIMITE[/]", "HTTP 429")
                results[name] = "ratelimited"
            elif r.status_code == 404:
                table.add_row(name, "[yellow]URL?[/]", "HTTP 404")
                results[name] = "notfound"
            else:
                table.add_row(name, "[yellow]HTTP " + str(r.status_code) + "[/]",
                              (r.text or "")[:60].replace("\n", " "))
                results[name] = f"http{r.status_code}"
        except Exception as e:  # noqa: BLE001
            table.add_row(name, "[red]ERROR RED[/]", str(e)[:60])
            results[name] = "neterr"

    console.print(table)
    Path(r"C:\Users\USER\Desktop\produccion\keys-status.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")

    ok = [k for k, v in results.items() if v == "ok"]
    console.print(f"\n[green]Operativas: {len(ok)}[/] -> {', '.join(ok)}")


if __name__ == "__main__":
    main()
