#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
limpieza-dbs.py - Limpieza de bases de datos y caches bloqueados.
  - Compacta (VACUUM) las bases SQLite de opencode sin perder datos
  - Borra la cache de TeraBox (TeraBox estaba parado)
Maneja el bloqueo por proceso en curso: si esta en uso, lo reporta y no toca.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
HOME = Path.home()

DBS = [
    HOME / ".local/share/opencode/opencode.db",
    HOME / "Documents/AgentStorage/data/opencode/opencode.db",
]

TB_FILES = [
    HOME / "AppData/Roaming/TeraBox/users/98809a46f100e7f2f5c50678d6bbfffc/TeraBoxCacheFileV1.db",
    HOME / "AppData/Roaming/TeraBox/users/98809a46f100e7f2f5c50678d6bbfffc/TeraBoxCacheFileV1.db-wal",
]


def mb(p: Path) -> float:
    try:
        return round(p.stat().st_size / 1024 / 1024, 1)
    except OSError:
        return 0.0


def vacuum(path: Path) -> tuple[str, float, float]:
    """Devuelve (estado, MB antes, MB despues)."""
    if not path.exists():
        return ("no existe", 0.0, 0.0)
    before = mb(path)
    try:
        # timeout corto: si otro proceso la tiene, fallara sin corromper nada
        con = sqlite3.connect(str(path), timeout=5.0)
        try:
            con.execute("PRAGMA busy_timeout=5000")
            con.execute("VACUUM")
            con.commit()
        finally:
            con.close()
        after = mb(path)
        return ("compactada", before, after)
    except sqlite3.OperationalError as e:
        return (f"bloqueada ({str(e)[:40]})", before, before)
    except Exception as e:  # noqa: BLE001
        return (f"error ({str(e)[:40]})", before, before)


def main():
    t = Table(title="Limpieza de bases de datos", border_style="cyan")
    t.add_column("Objetivo", max_width=40)
    t.add_column("Estado", max_width=26)
    t.add_column("Antes MB", justify="right")
    t.add_column("Despues MB", justify="right")
    t.add_column("Ganado MB", justify="right")

    total = 0.0

    # --- 1. Bases de opencode ---
    for db in DBS:
        label = str(db).replace(str(HOME), "~")
        estado, before, after = vacuum(db)
        gain = max(0.0, before - after)
        total += gain
        color = "green" if "compactada" in estado else "yellow"
        t.add_row(label[-40:], f"[{color}]{estado}[/]", f"{before:,.1f}", f"{after:,.1f}", f"{gain:,.1f}")

    # --- 2. Cache de TeraBox ---
    for f in TB_FILES:
        if not f.exists():
            t.add_row(f.name, "[dim]no existe[/]", "", "", "")
            continue
        size = mb(f)
        try:
            f.unlink()
            total += size
            t.add_row(f.name, "[green]borrada[/]", f"{size:,.1f}", "0,0", f"{size:,.1f}")
        except Exception as e:  # noqa: BLE001
            t.add_row(f.name, f"[red]bloqueada[/]", f"{size:,.1f}", f"{size:,.1f}", "0,0")

    console.print(t)
    console.print(f"\n[green]Total ganado: {total:,.1f} MB[/]")

    # Verificacion posterior
    console.print("\n[bold]Comprobacion:[/]")
    for db in DBS:
        if db.exists():
            console.print(f"  {db.name} ({str(db.parent).replace(str(HOME),'~')}): {mb(db):,.1f} MB")


if __name__ == "__main__":
    main()
