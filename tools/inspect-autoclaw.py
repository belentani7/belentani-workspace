#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""inspect-autoclaw.py - Revisa la configuracion de autoclaw/openclaw."""
import json
import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
P = Path(r"C:\Users\USER\.openclaw-autoclaw\openclaw.json")

d = json.loads(P.read_text(encoding="utf-8"))

console.rule("Estructura")
for k, v in d.items():
    kind = type(v).__name__
    n = len(v) if isinstance(v, (dict, list)) else ""
    console.print(f"  {k:<14} {kind:<6} {n}")

console.rule("Proveedores de modelo")
provs = (d.get("models") or {}).get("providers") or {}
t = Table(border_style="cyan")
t.add_column("Proveedor")
t.add_column("baseUrl", max_width=44)
t.add_column("api", max_width=14)
t.add_column("modelos", justify="right")
for name, cfg in provs.items():
    models = cfg.get("models") or []
    t.add_row(name, str(cfg.get("baseUrl", ""))[:44],
              str(cfg.get("api", "")), str(len(models)))
console.print(t)

console.rule("Modelos por proveedor")
for name, cfg in provs.items():
    for m in (cfg.get("models") or []):
        cost = m.get("cost") or {}
        free = all((cost.get(k) or 0) == 0 for k in ("input", "output"))
        console.print(f"  [cyan]{name}[/]/{m.get('id')}  {'[green]GRATIS[/]' if free else '[yellow]pago[/]'}  ctx={m.get('contextWindow')}")

console.rule("Auth / gateway")
auth = d.get("auth") or {}
s = json.dumps(auth, indent=2, ensure_ascii=False)
s = re.sub(r'(eyJ[A-Za-z0-9_\-\.]{20,})', lambda m: m.group(1)[:22] + "...(JWT)", s)
console.print(s[:900])

gw = d.get("gateway") or {}
console.print("\n[bold]gateway:[/]")
console.print(json.dumps(gw, indent=2, ensure_ascii=False)[:700])

# Decodificar expiracion del JWT si existe
console.rule("Expiracion del token interno")
raw = P.read_text(encoding="utf-8")
for jwt in set(re.findall(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+", raw)):
    try:
        import base64
        payload = jwt.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        exp = data.get("exp")
        if exp:
            import datetime
            dt = datetime.datetime.fromtimestamp(exp)
            left = dt - datetime.datetime.now()
            console.print(f"  exp={dt:%Y-%m-%d %H:%M}  quedan {left}")
    except Exception:
        pass
