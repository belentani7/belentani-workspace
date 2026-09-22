#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verificar-diverged.py - Verificacion INDEPENDIENTE de diverged-analisis.json.
Recalcula ahead/behind de los 123 DIVERGED (los refs ya estan fetcheados) y
compara con lo que reporto el analizador. Solo lectura.
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
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    div = [x for x in estado if x["verdict"] == "DIVERGED"]
    prev = json.loads((BASE / "diverged-analisis.json").read_text(encoding="utf-8"))
    prev_ahead = {x["name"]: x["ahead"] for x in prev["delante"]}
    prev_behind = {x["name"]: x["behind"] for x in prev["detras"]}
    prev_ambos = {x["name"]: (x["ahead"], x["behind"]) for x in prev["ambos"]}

    delante, detras, ambos, err = [], [], [], []
    for s in div:
        p = s["path"]
        br = (s.get("branch") or "").strip() or "main"
        rc, up, _ = git(p, "rev-parse", "--verify", f"origin/{br}")
        if rc != 0:
            # intentar descubrir la rama remota por defecto
            rc2, hd, _ = git(p, "symbolic-ref", "refs/remotes/origin/HEAD")
            br2 = hd.rsplit("/", 1)[-1] if rc2 == 0 else None
            if br2:
                br = br2
                rc, up, _ = git(p, "rev-parse", "--verify", f"origin/{br}")
        if rc != 0:
            err.append((s["name"], br))
            continue
        _, a, _ = git(p, "rev-list", "--count", f"origin/{br}..HEAD")
        _, b, _ = git(p, "rev-list", "--count", f"HEAD..origin/{br}")
        if not (a.isdigit() and b.isdigit()):
            err.append((s["name"], br))
            continue
        ai, bi = int(a), int(b)
        if ai > 0 and bi == 0:
            delante.append((s["name"], ai, br))
        elif ai == 0 and bi > 0:
            detras.append((s["name"], bi, br))
        elif ai > 0 and bi > 0:
            ambos.append((s["name"], ai, bi, br))
        else:
            err.append((s["name"], f"{br} (0/0)"))

    print(f"RECALCULO INDEPENDIENTE: delante={len(delante)} "
          f"detras={len(detras)} ambos={len(ambos)} err={len(err)}")
    print(f"ANALIZADOR PREVIO:       delante={len(prev['delante'])} "
          f"detras={len(prev['detras'])} ambos={len(prev['ambos'])}")

    print("\n-- DELANTE (nombre, +commits, rama) --")
    for n, a, br in sorted(delante, key=lambda x: -x[1]):
        marca = "OK" if prev_ahead.get(n) == a else f"DIFIERE(prev={prev_ahead.get(n)})"
        print(f"  {n[:44]:<44} +{a:<5} {br:<28} {marca}")

    print("\n-- AMBOS --")
    for n, a, b, br in sorted(ambos, key=lambda x: -(x[1] + x[2])):
        pv = prev_ambos.get(n)
        marca = "OK" if pv == (a, b) else f"DIFIERE(prev={pv})"
        print(f"  {n[:44]:<44} +{a:<5} -{b:<5} {br:<22} {marca}")

    if err:
        print("\n-- NO CLASIFICABLES --")
        for n, br in err:
            print(f"  {n[:44]:<44} rama={br}")

    # ¿hay algun repo DIVERGED que en realidad este al dia?
    print("\n-- Comprobacion: DIVERGED que ahora estan AL DIA (0/0) --")
    n0 = 0
    for n, br in err:
        if "(0/0)" in str(br):
            n0 += 1
            print(f"  {n}")
    print(f"  total={n0}")


if __name__ == "__main__":
    main()
