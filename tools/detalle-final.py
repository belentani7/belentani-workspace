#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
detalle-final.py - Datos finales para el informe: remotos y ramas de los 6
DELANTE, y contenido exacto de los archivos sin trackear de los PENDING.
Solo lectura.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")


def git(repo, *args, timeout=60):
    try:
        p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                           text=True, timeout=timeout, encoding="utf-8",
                           errors="replace",
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def main():
    prev = json.loads((BASE / "diverged-analisis.json").read_text(encoding="utf-8"))

    print("=== 6 DELANTE: destino de publicacion ===")
    for x in prev["delante"]:
        p, n = x["path"], x["name"]
        _, rem, _ = git(p, "remote", "get-url", "origin")
        _, br, _ = git(p, "rev-parse", "--abbrev-ref", "HEAD")
        rc, out, err = git(p, "ls-remote", "--heads", "origin", timeout=60)
        heads = [l.split("refs/heads/")[-1] for l in out.splitlines()
                 if "refs/heads/" in l] if rc == 0 else []
        rc2, subj, _ = git(p, "log", "--oneline", "-6",
                           f"origin/{br}..HEAD" if br in heads else "HEAD")
        print(f'\n  {n}  (+{x["ahead"]} commits, {x["mb"]} MB)')
        print(f'    ruta   : {p}')
        print(f'    remote : {rem or "(SIN REMOTO)"}')
        print(f'    rama   : {br}  -> {"EXISTE en remoto" if br in heads else "NO EXISTE en remoto (se crearia al pushear)"}')
        print(f'    ls-remote: {"OK (" + str(len(heads)) + " ramas)" if rc == 0 else "FALLA: " + err[:100]}')
        if subj:
            for l in subj.splitlines():
                print(f'      commit: {l[:110]}')

    print("\n\n=== PENDING: archivos sin trackear exactos ===")
    pe = json.loads((BASE / "pending-exacto.json").read_text(encoding="utf-8"))
    for f in pe["filas"]:
        if f["n_untracked"]:
            print(f'  {f["name"][:38]:<38} {f["n_untracked"]} -> {f["untracked_muestras"]}')

    print("\n=== PENDING: agrupacion por causa ===")
    grupos = {"SUCIO+UNTRACKED": [], "SOLO_SUCIO": [], "SOLO_UNTRACKED": [], "LIMPIO_Y_AL_DIA": []}
    for f in pe["filas"]:
        d, u = f["n_dirty"], f["n_untracked"]
        if d and u:
            grupos["SUCIO+UNTRACKED"].append(f["name"])
        elif d:
            grupos["SOLO_SUCIO"].append(f["name"])
        elif u:
            grupos["SOLO_UNTRACKED"].append(f["name"])
        else:
            grupos["LIMPIO_Y_AL_DIA"].append(f["name"])
    for k, v in grupos.items():
        print(f'\n  {k}: {len(v)}')
        for n in sorted(v):
            print(f'     - {n}')
    (BASE / "pending-grupos.json").write_text(
        json.dumps(grupos, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
