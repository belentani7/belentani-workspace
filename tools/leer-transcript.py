#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
leer-transcript.py - Extrae el contenido util del transcript de System32
para averiguar QUE proceso lo escribe.
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
F = Path(r"C:\Windows\System32\5E37410B-D6F1-471D-AE27-563CEAC0D6B2")

if not F.exists():
    console.print("[red]El archivo no existe (ya lo borro la tarea en el ultimo arranque)[/]")
    raise SystemExit(0)

raw = F.read_bytes()
BOM = b"\xff\xfe"
console.print(f"[cyan]Tamano:[/] {len(raw):,} bytes")
console.print(f"[cyan]Lleva BOM UTF-16LE:[/] {raw[:2] == BOM}")

# Decodificar UTF-16LE
try:
    txt = raw.decode("utf-16-le", errors="replace")
except Exception:
    txt = raw.decode("utf-8", errors="replace")
txt = txt.replace("\x00", "")

lineas = [l.strip() for l in txt.splitlines() if l.strip()]
console.print(f"[cyan]Lineas con contenido:[/] {len(lineas)}")

console.print("\n[bold]--- Primeras 25 lineas ---[/]")
for l in lineas[:25]:
    console.print(f"  {l[:150]}")

console.print("\n[bold]--- Patrones encontrados ---[/]")
patrones = {
    "Host Application": r"Host Application:\s*(.+)",
    "Process ID": r"Process ID:\s*(\d+)",
    "Username": r"Username:\s*(.+)",
    "RunAs User": r"RunAs User:\s*(.+)",
    "Machine": r"Machine:\s*(.+)",
    "Start time": r"Start time:\s*(.+)",
    "Command": r"(?:Command|Comando|Sending command)[:\s]+(.{0,120})",
    "Script": r"\.ps1|\.psm1|\.cmd|\.bat|\.exe",
}
for nombre, pat in patrones.items():
    ms = re.findall(pat, txt, re.I)
    if ms:
        c = Counter(m.strip()[:110] for m in ms)
        console.print(f"\n  [bold]{nombre}[/] ({len(ms)} veces)")
        for v, n in c.most_common(6):
            console.print(f"     [{n}x] {v}")

console.print("\n[bold]--- Todas las lineas unicas (excluyendo 'Log File Opened') ---[/]")
utiles = [l for l in lineas if "Log File Opened" not in l]
if utiles:
    for l in utiles[:60]:
        console.print(f"  {l[:150]}")
else:
    console.print("  (solo hay 'Log File Opened' — el transcript esta practicamente vacio)")

# Volcar todo a un archivo para inspeccion
salida = Path(r"C:\Users\USER\Desktop\produccion\transcript-system32.txt")
salida.write_text("\n".join(lineas), encoding="utf-8")
console.print(f"\n[green]Volcado completo:[/] {salida}")

# Buscar Start-Transcript en scripts del usuario
console.print("\n[bold]--- Scripts que llaman a Start-Transcript ---[/]")
p = subprocess.run(
    ["powershell", "-NoProfile", "-Command",
     "Get-ChildItem 'C:\\Users\\USER','C:\\ProgramData' -Recurse -File "
     "-Include *.ps1,*.psm1,*.cmd,*.bat -ErrorAction SilentlyContinue -Depth 6 | "
     "Select-String -Pattern 'Start-Transcript' -List -ErrorAction SilentlyContinue | "
     "Select-Object -First 15 | ForEach-Object { $_.Path + ' :: ' + $_.Line.Trim() }"],
    capture_output=True, text=True, timeout=300, encoding="utf-8", errors="replace")
console.print(p.stdout or "(ninguno)")
