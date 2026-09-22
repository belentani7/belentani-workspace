#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test-inference.py - Prueba REAL de inferencia en los tiers gratuitos.
Manda un prompt minimo ("di OK") y mide si responde y cuanto tarda.
El listado de modelos es gratis; esto comprueba la inferencia de verdad.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
PROMPT = "Responde solo con: OK"


def get_key(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


CASES = [
    # (etiqueta, url, modelo, var_env, cuerpo_extra)
    ("Groq gpt-oss-120b", "https://api.groq.com/openai/v1/chat/completions",
     "openai/gpt-oss-120b", "GROQ_API_KEY", {}),
    ("Groq gpt-oss-20b", "https://api.groq.com/openai/v1/chat/completions",
     "openai/gpt-oss-20b", "GROQ_API_KEY", {}),
    ("Groq qwen3.8-27b", "https://api.groq.com/openai/v1/chat/completions",
     "qwen/qwen3.8-27b", "GROQ_API_KEY", {}),
    ("Cerebras gpt-oss-120b", "https://api.cerebras.ai/v1/chat/completions",
     "gpt-oss-120b", "CEREBRAS_API_KEY", {}),
    ("Cerebras qwen-3.8-27b", "https://api.cerebras.ai/v1/chat/completions",
     "qwen-3.8-27b", "CEREBRAS_API_KEY", {}),
    ("OR free deepseek-v4-flash", "https://openrouter.ai/api/v1/chat/completions",
     "deepseek/deepseek-v4-flash-0731:free", "OPENROUTER_API_KEY", {}),
    ("OR free qwen3.8-27b", "https://openrouter.ai/api/v1/chat/completions",
     "qwen/qwen3.8-27b:free", "OPENROUTER_API_KEY", {}),
    ("OR free glm-5.2", "https://openrouter.ai/api/v1/chat/completions",
     "z-ai/glm-5.2:free", "OPENROUTER_API_KEY", {}),
    ("OR free nemotron-ultra", "https://openrouter.ai/api/v1/chat/completions",
     "nvidia/nemotron-3-ultra-550b-a55b:free", "OPENROUTER_API_KEY", {}),
    ("NVIDIA nemotron", "https://integrate.api.nvidia.com/v1/chat/completions",
     "nvidia/nemotron-3-ultra-550b-a55b", "NVIDIA_API_KEY", {}),
    ("DeepSeek flash", "https://api.deepseek.com/chat/completions",
     "deepseek-flash", "DEEPSEEK_API_KEY", {}),
    ("Z.AI glm-4.5-air", "https://api.z.ai/api/paas/v4/chat/completions",
     "glm-4.5-air", "Z_AI_API_KEY", {}),
    ("Z.AI glm-5.3-flash", "https://api.z.ai/api/paas/v4/chat/completions",
     "glm-5.3-flash", "Z_AI_API_KEY", {}),
]


def main():
    t = Table(title="Prueba de INFERENCIA real en free tiers", border_style="cyan")
    t.add_column("Proveedor/modelo", max_width=30)
    t.add_column("Estado")
    t.add_column("ms", justify="right")
    t.add_column("Respuesta / error", max_width=42)

    results = {}
    for label, url, model, envvar, extra in CASES:
        key = get_key(envvar)
        if not key or "ELIMINADA" in key.upper():
            t.add_row(label, "[dim]sin clave[/]", "", "")
            results[label] = "nokey"
            continue
        body = {"model": model, "messages": [{"role": "user", "content": PROMPT}],
                "max_tokens": 20, **extra}
        hdrs = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        if "openrouter" in url:
            hdrs["HTTP-Referer"] = "https://belentani.vercel.app"
            hdrs["X-Title"] = "Belentani"
        start = time.time()
        try:
            r = httpx.post(url, headers=hdrs, json=body, timeout=60)
            ms = int((time.time() - start) * 1000)
            if r.status_code == 200:
                d = r.json()
                txt = ""
                try:
                    txt = d["choices"][0]["message"].get("content") or ""
                    if not txt and d["choices"][0]["message"].get("reasoning_content"):
                        txt = "(solo reasoning) " + d["choices"][0]["message"]["reasoning_content"][:30]
                except Exception:
                    txt = str(d)[:40]
                t.add_row(label, "[green]OK[/]", str(ms), txt[:42].replace("\n", " "))
                results[label] = "ok"
            elif r.status_code == 402:
                t.add_row(label, "[red]402 PAGO[/]", str(ms), "requiere pago")
                results[label] = "paid"
            elif r.status_code == 429:
                t.add_row(label, "[yellow]429 LIMITE[/]", str(ms), "pool free saturado")
                results[label] = "ratelimited"
            else:
                msg = ""
                try:
                    msg = json.dumps(r.json().get("error", {}))[:60]
                except Exception:
                    msg = (r.text or "")[:60]
                t.add_row(label, f"[red]HTTP {r.status_code}[/]", str(ms), msg.replace("\n", " "))
                results[label] = f"http{r.status_code}"
        except Exception as e:  # noqa: BLE001
            t.add_row(label, "[red]ERROR[/]", "", str(e)[:42])
            results[label] = "neterr"

    console.print(t)
    Path(r"C:\Users\USER\Desktop\produccion\inference-status.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    ok = [k for k, v in results.items() if v == "ok"]
    console.print(f"\n[green]Inferencia OK en {len(ok)}:[/] {', '.join(ok)}")


if __name__ == "__main__":
    main()
