#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verificar-faltantes.py - Comprueba EN VIVO si el remoto de cada repo candidato
existe realmente en GitHub (git ls-remote), y si el nombre aparece en el
inventario local. Solo lectura.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")


def run(repo, *args, timeout=90):
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "echo"},
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def main():
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    gh = json.loads((BASE / "github-inventario.json").read_text(encoding="utf-8"))
    gh_names = {r["name"].lower() for r in gh}
    gh_urls = {(r.get("url") or "").lower().rstrip(".git") for r in gh}

    cruce = json.loads((BASE / "auditoria-cruce.json").read_text(encoding="utf-8"))
    por_name = {x["name"]: x for x in estado}

    print("== 1. Comprobacion de nombres PROPIO en inventario ==")
    for x in cruce["faltantes_reales"]:
        rem = (x.get("remote") or "").lower().rstrip(".git")
        if not rem:
            continue
        en_inv = rem in gh_urls or x["name"].lower() in gh_names
        if x["name"] in ("2-icons-backup-export", "edu-engine", "william-game",
                         "Documents__01_PROYECTOS__william-game"):
            print(f'  {x["name"]:<38} url_en_inventario={en_inv}  {rem}')

    print("\n== 2. ls-remote en vivo de los SIN-REMOTO y PROPIO ==")
    cand = [x for x in cruce["faltantes_reales"]
            if (not (x.get("remote") or "").strip())
            or "belentani7" in (x.get("remote") or "")
            or "roberto7sena" in (x.get("remote") or "")]
    for x in cand:
        p = x["path"]
        rc, remote, _ = run(p, "remote", "-v")
        rc2, out, err = run(p, "ls-remote", "--heads", "origin", timeout=60)
        heads = len([l for l in out.splitlines() if l.strip()]) if rc2 == 0 else -1
        estado_ok = "OK" if rc2 == 0 else "FALLA"
        print(f'  {x["name"][:36]:<36} remote={(remote.splitlines()[0].split()[1] if remote else "(vacio)")}')
        print(f'      ls-remote: {estado_ok} heads={heads}  err={err[:150]}')

    print("\n== 3. Los 25 NO_REMOTE del estado.json ==")
    for s in estado:
        if s["verdict"] == "NO_REMOTE":
            rc, remote, _ = run(s["path"], "remote", "-v")
            rc2, cnt, _ = run(s["path"], "rev-list", "--count", "HEAD")
            rc3, last, _ = run(s["path"], "log", "-1", "--format=%cI|%s")
            existe = Path(s["path"]).exists()
            tenia_remoto = bool(remote)
            print(f'{s["name"][:34]:<34} {s["size_mb"]:>7} MB exists={existe} '
                  f'commits={cnt} remote_ahora={tenia_remoto}')
            print(f'      last={last[:110]}')
            if tenia_remoto:
                print(f'      REMOTE: {remote}')

    print("\n== 4. REMOTE_MISSING (6) y UNREACHABLE (1) ==")
    for s in estado:
        if s["verdict"] in ("REMOTE_MISSING", "UNREACHABLE"):
            rc, remote, _ = run(s["path"], "remote", "-v")
            rc2, out, err = run(s["path"], "ls-remote", "--heads", "origin", timeout=60)
            print(f'{s["verdict"]:<15} {s["name"][:32]:<32} {s["size_mb"]:>7} MB')
            print(f'      remote: {(remote.splitlines()[0].split()[1] if remote else "(vacio)")}')
            print(f'      err: {err[:180]}')


if __name__ == "__main__":
    main()
