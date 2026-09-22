#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pending-exacto.py - Mide el estado real de los 42 PENDING SIN escribir nada en
los repos (no hace fetch ni crea refs).

Metodo:
  1. git ls-remote origin refs/heads/<rama>   -> SHA del remoto (red, solo lectura)
  2. Si ese objeto YA existe localmente, se calcula ahead/behind exacto con
     rev-list --count (sin escribir refs).
  3. Si el objeto no existe localmente, se informa NO MEDIBLE SIN FETCH en vez
     de inventar un numero.
Tambien comprueba el refspec remote.origin.fetch, que explica por que faltan
las refs origin/<rama>.
"""
from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
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
        p = s["path"]
        br = (s.get("branch") or "").strip() or "main"
        f = {"name": s["name"], "path": p, "branch": br, "size_mb": s.get("size_mb")}

        rc, refspec, _ = git(p, "config", "--get-all", "remote.origin.fetch")
        f["refspec_fetch"] = refspec or "(NINGUNO)"

        rc, head, _ = git(p, "rev-parse", "HEAD")
        f["head"] = head[:12] if rc == 0 else None
        rc, cnt, _ = git(p, "rev-list", "--count", "HEAD")
        f["n_commits"] = int(cnt) if cnt.isdigit() else 0

        rc, st, _ = git(p, "status", "--porcelain")
        lines = [l for l in st.splitlines() if l.strip()] if rc == 0 else []
        dirty = [l for l in lines if not l.startswith("??")]
        untracked = [l[3:] for l in lines if l.startswith("??")]
        f["n_dirty"] = len(dirty)
        f["n_untracked"] = len(untracked)
        f["dirty_muestras"] = dirty[:8]
        f["untracked_muestras"] = untracked[:8]

        # SHA remoto de la rama (solo lectura)
        rc, out, err = git(p, "ls-remote", "origin", f"refs/heads/{br}", timeout=60)
        remote_sha = None
        if rc == 0 and out.strip():
            remote_sha = out.split()[0]
        f["remote_sha"] = remote_sha[:12] if remote_sha else None
        f["ls_remote_err"] = err[:120] if rc != 0 else None

        if f["n_commits"] == 0:
            f["estado_push"] = "REPO_VACIO"
            f["ahead"] = 0
            f["behind"] = 0
        elif not remote_sha:
            f["estado_push"] = "RAMA_NO_EN_REMOTO"
            f["ahead"] = None
            f["behind"] = None
        elif remote_sha == head:
            f["estado_push"] = "AL_DIA"
            f["ahead"] = 0
            f["behind"] = 0
        else:
            # ¿tenemos el objeto remoto localmente?
            rc2, _, _ = git(p, "cat-file", "-e", remote_sha + "^{commit}")
            if rc2 == 0:
                rc3, a, _ = git(p, "rev-list", "--count", f"{remote_sha}..HEAD")
                rc4, b, _ = git(p, "rev-list", "--count", f"HEAD..{remote_sha}")
                f["ahead"] = int(a) if a.isdigit() else None
                f["behind"] = int(b) if b.isdigit() else None
                if f["ahead"] and f["ahead"] > 0 and f["behind"] == 0:
                    f["estado_push"] = "ADELANTE"
                elif f["ahead"] == 0 and f["behind"] and f["behind"] > 0:
                    f["estado_push"] = "DETRAS"
                elif f["ahead"] and f["behind"]:
                    f["estado_push"] = "DIVERGED"
                else:
                    f["estado_push"] = "AL_DIA"
            else:
                f["estado_push"] = "NO_MEDIBLE_SIN_FETCH"
                f["ahead"] = None
                f["behind"] = None
        filas.append(f)

    res = Counter(f["estado_push"] for f in filas)
    print("ESTADO DE PUSH:", dict(res), "\n")
    res2 = Counter("refspec_ok" if f["refspec_fetch"].startswith("+refs/heads/")
                   else "refspec_ausente_o_raro" for f in filas)
    print("REFSPEC remote.origin.fetch:", dict(res2), "\n")

    for f in sorted(filas, key=lambda x: x["name"].lower()):
        print(f'{f["name"][:38]:<38} {f["estado_push"]:<22} '
              f'ahead={str(f["ahead"]):<5} behind={str(f["behind"]):<5} '
              f'dirty={f["n_dirty"]:<4} untracked={f["n_untracked"]:<4} '
              f'commits={f["n_commits"]}')
        if f["refspec_fetch"] == "(NINGUNO)":
            print(f'      !! SIN refspec de fetch -> nunca se crean refs origin/*')
        if f["estado_push"] == "NO_MEDIBLE_SIN_FETCH":
            print(f'      remote_sha={f["remote_sha"]} no esta en el repo local')
        if f["ls_remote_err"]:
            print(f'      ls-remote err: {f["ls_remote_err"]}')

    (BASE / "pending-exacto.json").write_text(
        json.dumps({"filas": filas, "estado_push": dict(res),
                    "refspec": dict(res2)}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"\nGuardado: {BASE / 'pending-exacto.json'}")


if __name__ == "__main__":
    main()
