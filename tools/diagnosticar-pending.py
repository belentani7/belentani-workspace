#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
diagnosticar-pending.py - Causa REAL de los 42 PENDING, en particular los 20
cuyo 'unpushed' no se pudo medir (rev-list contra origin/<rama> no devolvio
un numero). No modifica nada.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")


def git(repo, *args, timeout=60):
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def main():
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    pend = [x for x in estado if x["verdict"] == "PENDING"]

    filas = []
    for s in pend:
        p, br = s["path"], (s.get("branch") or "main")
        f = {"name": s["name"], "path": p, "branch_cfg": br,
             "size_mb": s.get("size_mb")}
        rc, rem, _ = git(p, "remote", "-v")
        f["remote"] = rem.splitlines()[0].split()[1] if rem else None
        rc, refs, err = git(p, "for-each-ref", "--format=%(refname)", "refs/remotes/")
        f["remote_refs"] = [r for r in refs.splitlines() if r.strip()]
        rc, head, _ = git(p, "rev-parse", "--verify", "HEAD")
        f["tiene_head"] = rc == 0
        rc, cnt, _ = git(p, "rev-list", "--count", "HEAD")
        f["n_commits"] = int(cnt) if cnt.isdigit() else 0
        rc, st, _ = git(p, "status", "--porcelain")
        lines = [l for l in st.splitlines() if l.strip()] if rc == 0 else []
        f["n_dirty_tracked"] = len([l for l in lines if not l.startswith("??")])
        f["n_untracked"] = len([l for l in lines if l.startswith("??")])
        f["dirty_muestras"] = [l for l in lines if not l.startswith("??")][:6]
        f["untracked_muestras"] = [l[3:] for l in lines if l.startswith("??")][:6]

        # intentar determinar unpushed de varias formas
        up_ref = f"origin/{br}"
        f["up_ref_existe"] = up_ref in f["remote_refs"]
        if f["n_commits"] == 0:
            f["unpushed"] = 0
            f["diag"] = "REPO VACIO (0 commits) - nada que pushear"
        elif f["up_ref_existe"]:
            rc, o, _ = git(p, "rev-list", "--count", f"{up_ref}..HEAD")
            f["unpushed"] = int(o) if o.isdigit() else None
            f["diag"] = f"comparado con {up_ref}"
        else:
            # no hay ref remoto: comprobar en vivo con ls-remote
            rc2, out2, err2 = git(p, "ls-remote", "--heads", "origin", timeout=60)
            if rc2 != 0:
                f["unpushed"] = None
                f["diag"] = f"ls-remote FALLA: {err2[:80]}"
                f["ls_remote_heads"] = None
            else:
                heads = [l.split("refs/heads/")[-1] for l in out2.splitlines()
                         if "refs/heads/" in l]
                f["ls_remote_heads"] = heads
                if not heads:
                    f["unpushed"] = f["n_commits"]
                    f["diag"] = ("REMOTO EXISTE PERO VACIO (0 ramas) -> "
                                 f"TODO sin publicar ({f['n_commits']} commits)")
                else:
                    f["unpushed"] = None
                    f["diag"] = (f"rama '{br}' no esta en el remoto; ramas remotas: "
                                 f"{heads[:6]}")
        filas.append(f)

    # resumen por causa
    from collections import Counter
    causas = Counter()
    for f in filas:
        c = []
        if f["n_commits"] == 0:
            c.append("REPO_VACIO")
        elif f["up_ref_existe"] and f["unpushed"] and f["unpushed"] > 0:
            c.append("COMMITS_SIN_PUSHEAR")
        elif not f["up_ref_existe"]:
            c.append("SIN_REF_REMOTO_DE_LA_RAMA")
        if f["n_dirty_tracked"] > 0:
            c.append("ARBOL_SUCIO")
        if f["n_untracked"] > 0:
            c.append("ARCHIVOS_SIN_TRACKEAR")
        if not c:
            c.append("AL_DIA")
        f["causas"] = c
        for x in c:
            causas[x] += 1

    print("RESUMEN CAUSAS:", dict(causas), "\n")
    for f in filas:
        print(f'{f["name"][:38]:<38} commits={f["n_commits"]:<5} '
              f'dirty={f["n_dirty_tracked"]:<4} untracked={f["n_untracked"]:<4} '
              f'unpushed={f["unpushed"]}')
        print(f'      {f["diag"]}')
        if f["n_dirty_tracked"]:
            print(f'      dirty: {f["dirty_muestras"]}')
        if f["n_untracked"]:
            print(f'      untracked: {f["untracked_muestras"]}')

    (BASE / "pending-diagnostico.json").write_text(
        json.dumps({"filas": filas, "resumen": dict(causas)},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado: {BASE / 'pending-diagnostico.json'}")


if __name__ == "__main__":
    main()
