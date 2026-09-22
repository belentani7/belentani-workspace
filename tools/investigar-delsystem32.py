#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
investigar-delsystem32.py - Origen de la tarea que borra logs de PowerShell
en C:\\Windows\\System32 en cada arranque.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
OBJETIVO = r"C:\Windows\System32\5E37410B-D6F1-471D-AE27-563CEAC0D6B2"


def ps(cmd: str, timeout: int = 90) -> str:
    p = subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                       capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return (p.stdout or "") + (p.stderr or "")


console.rule("[bold]1. Definicion XML de la tarea")
xml = ps("Export-ScheduledTask -TaskName 'DelSystem32Transcript'")
console.print(xml[:2500] if xml else "(sin salida)")

console.rule("[bold]2. Fechas del archivo de tarea")
console.print(ps(
    "Get-Item 'C:\\Windows\\System32\\Tasks\\DelSystem32Transcript' "
    "-ErrorAction SilentlyContinue | "
    "Select-Object FullName,CreationTime,LastWriteTime,Length | Format-List"))

console.rule("[bold]3. El archivo objetivo")
console.print(ps(
    f"if(Test-Path '{OBJETIVO}'){{ "
    f"$i=Get-Item '{OBJETIVO}' -Force; "
    f"'existe: ' + $i.Length + ' B, creado ' + $i.CreationTime + ', mod ' + $i.LastWriteTime "
    f"}} else {{ 'no existe ahora' }}"))

console.rule("[bold]4. Contenido (primeras lineas legibles)")
console.print(ps(
    f"if(Test-Path '{OBJETIVO}'){{ "
    f"Get-Content '{OBJETIVO}' -TotalCount 6 -Encoding Unicode | "
    "ForEach-Object { $_.Substring(0,[Math]::Min(160,$_.Length)) } }"))

console.rule("[bold]5. Transcripcion de PowerShell: politica del registro")
for k in [r"HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription",
          r"HKCU:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription",
          r"HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging",
          r"HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging"]:
    console.print(f"[dim]{k}[/]")
    console.print(ps(f"if(Test-Path '{k}'){{ Get-ItemProperty '{k}' | "
                     f"Format-List * }} else {{ '  (no existe)' }}")[:700])

console.rule("[bold]6. Perfiles de PowerShell (posible Start-Transcript)")
for p in [r"C:\Users\USER\Documents\PowerShell\Microsoft.PowerShell_profile.ps1",
          r"C:\Users\USER\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1",
          r"C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1"]:
    console.print(f"[dim]{p}[/]")
    console.print(ps(f"if(Test-Path '{p}'){{ "
                     f"$c=Get-Content '{p}' -Raw; "
                     f"if($c -match 'Transcript'){{ 'CONTIENE Transcript' }} else {{ 'sin Transcript (' + $c.Length + ' B)' }} "
                     f"}} else {{ 'no existe' }}"))

console.rule("[bold]7. Buscar Start-Transcript en scripts del usuario")
r = ps("Get-ChildItem 'C:\\Users\\USER' -Recurse -File -Include *.ps1,*.psm1,*.cmd,*.bat "
       "-ErrorAction SilentlyContinue -Depth 5 | "
       "Select-String -Pattern 'Start-Transcript' -List -ErrorAction SilentlyContinue | "
       "Select-Object -First 12 | ForEach-Object { $_.Path }")
console.print(r or "(ninguno)")

console.rule("[bold]8. Tareas programadas que mencionan Transcript")
console.print(ps("Get-ScheduledTask -ErrorAction SilentlyContinue | "
                 "Where-Object { $_.Actions.Arguments -match 'Transcript|[0-9A-F]{8}-' } | "
                 "Select-Object TaskName,TaskPath,State | Format-Table -AutoSize | Out-String"))
