#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test-claude-endpoint.py - Verifica que Claude Code funciona via OpenRouter."""
import json
import subprocess

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


def getk(n: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % n],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def main():
    t = Table(title="Claude Code -> OpenRouter (/v1/messages)", border_style="cyan")
    t.add_column("Clave")
    t.add_column("HTTP")
    t.add_column("Respuesta", max_width=50)

    cfg_path = r"C:\Users\USER\.claude\settings.json"
    cfg = json.loads(open(cfg_path, encoding="utf-8").read())
    env = cfg.get("env", {})
    console.print(f"[dim]ANTHROPIC_BASE_URL = {env.get('ANTHROPIC_BASE_URL')}[/]")
    console.print(f"[dim]modelo por defecto  = {cfg.get('model')}[/]")
    console.print(f"[dim]modelos mapeados    = {env.get('ANTHROPIC_DEFAULT_SONNET_MODEL')}[/]")
    console.print()

    for label, var in [("AUTH_TOKEN (KEY_2)", "OPENROUTER_KEY_2"),
                       ("FALLBACK (KEY_3)", "OPENROUTER_KEY_3"),
                       ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY")]:
        k = getk(var)
        if not k:
            t.add_row(label, "[dim]ausente[/]", "")
            continue
        try:
            r = httpx.post(
                "https://openrouter.ai/api/v1/messages",
                headers={"x-api-key": k, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json={"model": "openrouter/free", "max_tokens": 20,
                      "messages": [{"role": "user", "content": "Responde solo: OK"}]},
                timeout=60)
            body = ""
            try:
                d = r.json()
                if r.status_code == 200:
                    parts = d.get("content") or []
                    body = " ".join(p.get("text", "") for p in parts if isinstance(p, dict))
                else:
                    body = json.dumps(d.get("error", d))[:80]
            except Exception:
                body = (r.text or "")[:80]
            color = "green" if r.status_code == 200 else "red"
            t.add_row(label, f"[{color}]{r.status_code}[/]", body.replace("\n", " "))
        except Exception as e:  # noqa: BLE001
            t.add_row(label, "[red]ERR[/]", str(e)[:50])

    console.print(t)


if __name__ == "__main__":
    main()
