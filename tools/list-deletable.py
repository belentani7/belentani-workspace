#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""list-deletable.py - Muestra la lista completa de repos confirmados como borrables."""
import json
from pathlib import Path

OUT = Path(r"C:\Users\USER\Desktop\produccion")
d = json.loads((OUT / "estado.json").read_text(encoding="utf-8"))

safe = [x for x in d if x["verdict"] == "SAFE_TO_DELETE"]
safe.sort(key=lambda x: -(x.get("size_mb") or 0))

print("=" * 112)
print(f"{'REPO':<40} {'MB':>9}  RUTA")
print("=" * 112)
tot = 0.0
for s in safe:
    mb = s.get("size_mb") or 0
    tot += mb
    ruta = s["path"].replace("C:\\Users\\USER\\", "")
    print(f"{s['name'][:39]:<40} {mb:>9.1f}  {ruta[:58]}")
print("=" * 112)
print(f"{'TOTAL':<40} {tot:>9.1f} MB   ({len(safe)} repos)")
print()

edu = [x for x in d if x["verdict"] == "KEEP_EDU"]
print(f"PROTEGIDOS - educacionales ({len(edu)}):")
for s in sorted(edu, key=lambda x: x["name"]):
    print(f"   {s['name']}")
print()

# Aviso: proyectos activos en la lista
activos = ["judas", "Belentani", "belentani", "duck", "omega", "cad", "secure-t",
           "noiacore", "aion", "nexus"]
print("ATENCION - proyectos potencialmente ACTIVOS en la lista de borrado:")
for s in safe:
    if any(a.lower() in s["name"].lower() for a in activos):
        print(f"   {s['name']:<40} {(s.get('size_mb') or 0):>8.1f} MB")
