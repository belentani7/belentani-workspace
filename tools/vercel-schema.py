#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vercel-schema.py - Inspecciona el esquema del proyecto para hallar el campo correcto."""
import json
import os
import subprocess
from pathlib import Path

import httpx
from rich.console import Console

console = Console()
OUT = Path(r"C:\Users\USER\Desktop\produccion")


def token() -> str:
    t = os.environ.get("VERCEL_TOKEN")
    if t:
        return t
    p = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "[Environment]::GetEnvironmentVariable('VERCEL_TOKEN','User')"],
                       capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


TOK = token()
console.print(f"token: {TOK[:12]}... ({len(TOK)} chars)")
H = {"Authorization": f"Bearer {TOK}", "User-Agent": "dsh"}

PID = "prj_zHebnvXhYCSmsCK5VErlX7E1mzVx"

for ver in ("v9", "v10", "v11"):
    r = httpx.get(f"https://api.vercel.com/{ver}/projects/{PID}", headers=H, timeout=45)
    console.print(f"\n=== /{ver}/projects -> HTTP {r.status_code}")
    if r.status_code == 200:
        d = r.json()
        (OUT / "vercel-proyecto-aprende.json").write_text(
            json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"  claves: {len(d)}")
        for k in ("git", "ignoredBuildStep", "commandForIgnoringBuildStep",
                  "buildCommand", "framework", "link", "name", "autoExposeSystemEnvs"):
            if k in d:
                console.print(f"  {k} = {json.dumps(d[k], ensure_ascii=False)[:150]}")
        break
    else:
        console.print(f"  {r.text[:200]}")

# Verificar el token
r = httpx.get("https://api.vercel.com/v2/user", headers=H, timeout=30)
console.print(f"\n=== /v2/user -> HTTP {r.status_code}")
if r.status_code == 200:
    u = r.json().get("user", {})
    console.print(f"  usuario: {u.get('username') or u.get('email')}")
