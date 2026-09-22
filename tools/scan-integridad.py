#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scan-integridad.py - Comprueba la integridad de git en los 264 repos del
estado.json: .git vacio, .git corrupto, HEAD invalido, ruta inexistente.
Solo lectura.
"""
from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")
ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def git(p, *a, timeout=45):
    try:
        r = subprocess.run(["git", "-C", str(p), *a], capture_output=True,
                           text=True, timeout=timeout, encoding="utf-8",
                           errors="replace", env=ENV)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def main():
    est = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    filas = []
    for s in est:
        p = Path(s["path"])
        f = {"name": s["name"], "path": s["path"], "verdict": s["verdict"],
             "size_mb": s.get("size_mb")}
        if not p.exists():
            f["diag"] = "RUTA_NO_EXISTE"
            filas.append(f)
            continue
        gd = p / ".git"
        if gd.exists() and gd.is_dir():
            try:
                n = len(list(gd.iterdir()))
            except Exception:  # noqa: BLE001
                n = -1
            f["entradas_git"] = n
        else:
            f["entradas_git"] = None
        rc, out, err = git(p, "rev-parse", "--git-dir")
        f["git_valido"] = rc == 0
        if rc != 0:
            f["diag"] = "GIT_INVALIDO: " + err.splitlines()[0][:90] if err else "GIT_INVALIDO"
        else:
            rc2, hd, err2 = git(p, "rev-parse", "--verify", "HEAD")
            f["head_valido"] = rc2 == 0
            if rc2 != 0:
                f["diag"] = "SIN_COMMITS (HEAD no nace)"
            else:
                rc3, cnt, _ = git(p, "rev-list", "--count", "HEAD")
                f["n_commits"] = int(cnt) if cnt.isdigit() else 0
                f["diag"] = "OK"
        filas.append(f)

    c = Counter(f["diag"].split(":")[0].split(" ")[0] for f in filas)
    print("DIAGNOSTICO INTEGRIDAD:", dict(c), "\n")
    for f in filas:
        if f["diag"] != "OK":
            print(f'{f["diag"][:34]:<34} {f["name"][:36]:<36} {f["size_mb"]:>8} MB '
                  f'verdict={f["verdict"]}')
            print(f'      {f["path"]}   (.git entradas={f.get("entradas_git")})')

    (BASE / "integridad-git.json").write_text(
        json.dumps({"filas": filas, "resumen": dict(c)}, indent=2,
                   ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado: {BASE / 'integridad-git.json'}")


if __name__ == "__main__":
    main()
