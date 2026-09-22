#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extraer-vercel-clientid.py - Saca el client_id del device flow del CLI de Vercel
para poder autenticar sin abrir el navegador del CLI.
"""
import re
from pathlib import Path

BASE = Path(r"C:\Users\USER\AppData\Roaming\npm\node_modules\vercel")

FICHEROS = [
    BASE / "dist/chunks/chunk-L243RUIR.js",
    BASE / "dist/chunks/chunk-5XJNPXQK.js",
    BASE / "node_modules/@vercel/cli-auth/oauth.js",
]

PATRONES = [
    r'clientId\s*[:=]\s*["\']([^"\']{6,80})["\']',
    r'client_id\s*[:=]\s*["\']([^"\']{6,80})["\']',
    r'VERCEL_CLIENT_ID\s*=\s*["\']([^"\']+)["\']',
    r'cl_[A-Za-z0-9]{15,40}',
    r'issuer\s*[:=]\s*new URL\(["\']([^"\']+)["\']\)',
    r'new OAuth\(\s*\{([^}]{0,300})\}',
]

for f in FICHEROS:
    if not f.exists():
        print(f"NO EXISTE: {f}")
        continue
    print(f"\n=== {f.name} ({f.stat().st_size:,} B)")
    txt = f.read_text(encoding="utf-8", errors="replace")
    encontrados = set()
    for p in PATRONES:
        for m in re.finditer(p, txt, re.S):
            v = m.group(0)
            if len(v) > 220:
                v = v[:220] + "..."
            v = " ".join(v.split())
            if v not in encontrados:
                encontrados.add(v)
                print(f"   [{p[:28]}] {v}")

# Ademas: buscar en TODO el arbol cualquier literal que parezca client id
print("\n=== barrido global de posibles client_id ===")
vistos = set()
for f in BASE.rglob("*.js"):
    try:
        if f.stat().st_size > 8_000_000:
            continue
        txt = f.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    for m in re.finditer(r'["\'](cl_[A-Za-z0-9]{10,60})["\']', txt):
        cid = m.group(1)
        if cid not in vistos:
            vistos.add(cid)
            print(f"   {cid}   ({f.relative_to(BASE)})")
if not vistos:
    print("   (ninguno encontrado con prefijo cl_)")
