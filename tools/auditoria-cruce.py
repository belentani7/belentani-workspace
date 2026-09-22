#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
auditoria-cruce.py - Tareas 2 y 3 del informe.

TAREA 2: cruza estado.json (locales) contra github-inventario.json (GitHub).
         Detecta repos locales que NO existen en GitHub y separa los que son
         subcarpetas anidadas dentro de otro repo (hay un .git en un padre).
TAREA 3: re-mide EN VIVO los repos PENDING (unpushed / dirty / untracked).

Solo lee. No modifica ningun repo.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")
OUT = BASE / "auditoria-cruce.json"


def git(repo, *args, timeout=90):
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def norm(s: str) -> str:
    return (s or "").strip().lower()


def parents_with_dot_git(path: str):
    """Devuelve la lista de directorios padre que contienen un .git.

    Sube desde el padre inmediato hasta la raiz de la unidad.
    """
    hits = []
    p = Path(path)
    try:
        cur = p.parent
    except Exception:  # noqa: BLE001
        return hits
    seen = 0
    while cur and str(cur) != cur.parent and seen < 12:
        seen += 1
        # un repo padre puede tener .git como dir o como fichero (worktree/submodule)
        if (cur / ".git").exists():
            hits.append(str(cur))
        cur = cur.parent
    return hits


def main():
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    gh = json.loads((BASE / "github-inventario.json").read_text(encoding="utf-8"))

    gh_by_name = {norm(r["name"]): r for r in gh}
    print(f"locales={len(estado)}  github={len(gh)}")

    faltantes = []
    presentes = 0
    for s in estado:
        name = s["name"]
        if norm(name) in gh_by_name:
            presentes += 1
            continue
        # tambien probar el nombre deducido del remote (a veces difiere)
        remote = s.get("remote") or ""
        rname = ""
        if remote:
            tail = remote.rstrip("/").rsplit("/", 1)[-1]
            rname = tail[:-4] if tail.endswith(".git") else tail
        match_by_remote = norm(rname) in gh_by_name if rname else False
        # y el basename de la ruta
        pname = Path(s["path"]).name
        match_by_path = norm(pname) in gh_by_name

        if match_by_remote or match_by_path:
            presentes += 1
            continue

        padres = parents_with_dot_git(s["path"])
        exists = Path(s["path"]).exists()
        faltantes.append({
            "name": name,
            "path": s["path"],
            "size_mb": s.get("size_mb"),
            "verdict": s.get("verdict"),
            "branch": s.get("branch"),
            "remote": s.get("remote"),
            "remote_name_guess": rname,
            "exists_on_disk": exists,
            "nested_in": padres,
            "is_nested": bool(padres),
        })

    reales = [x for x in faltantes if not x["is_nested"]]
    anidados = [x for x in faltantes if x["is_nested"]]
    print(f"presentes_en_github={presentes}  faltantes={len(faltantes)} "
          f"(reales={len(reales)} anidados={len(anidados)})")

    # ---------- TAREA 3: re-medir PENDING ----------
    pend = [x for x in estado if x["verdict"] == "PENDING"]
    print(f"\nPENDING a re-medir: {len(pend)}")
    pend_out = []
    for i, s in enumerate(pend, 1):
        p = s["path"]
        br = s.get("branch") or "main"
        rec = {
            "name": s["name"], "path": p, "branch": br,
            "size_mb": s.get("size_mb"), "exists": Path(p).exists(),
        }
        if not rec["exists"]:
            rec["error"] = "RUTA NO EXISTE"
            pend_out.append(rec)
            continue

        # rama actual real
        rc, cur, err = git(p, "rev-parse", "--abbrev-ref", "HEAD")
        rec["current_branch"] = cur if rc == 0 else f"<err> {err[:120]}"

        # upstream configurado
        rc, up, _ = git(p, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        rec["upstream"] = up if rc == 0 else None

        # estado del arbol: porcelain (dirty + untracked)
        rc, st, err = git(p, "status", "--porcelain")
        lines = [l for l in st.splitlines() if l.strip()] if rc == 0 else []
        untracked = [l for l in lines if l.startswith("??")]
        tracked_dirty = [l for l in lines if not l.startswith("??")]
        rec["status_error"] = None if rc == 0 else err[:200]
        rec["n_dirty_tracked"] = len(tracked_dirty)
        rec["n_untracked"] = len(untracked)
        rec["dirty_muestras"] = tracked_dirty[:12]
        rec["untracked_muestras"] = [l[3:] for l in untracked[:12]]

        # unpushed: contra upstream si existe, si no contra origin/<branch>
        if up:
            rc, o, _ = git(p, "rev-list", "--count", f"{up}..HEAD")
            rec["unpushed"] = int(o) if o.isdigit() else None
            rec["unpushed_ref"] = up
        else:
            rc, o, _ = git(p, "rev-list", "--count", f"origin/{br}..HEAD")
            if o.isdigit():
                rec["unpushed"] = int(o)
                rec["unpushed_ref"] = f"origin/{br} (sin upstream configurado)"
            else:
                rec["unpushed"] = None
                rec["unpushed_ref"] = None

        rc, head, _ = git(p, "rev-parse", "HEAD")
        rec["head"] = head[:12] if rc == 0 else None
        rc, cnt, _ = git(p, "rev-list", "--count", "HEAD")
        rec["n_commits"] = int(cnt) if cnt.isdigit() else None
        rc, last, _ = git(p, "log", "-1", "--format=%cI|%s")
        rec["last_commit"] = last[:160] if rc == 0 else None

        # causa / agrupacion
        causas = []
        if rec["unpushed"] is None:
            causas.append("INDETERMINADO")
        elif rec["unpushed"] > 0:
            causas.append("COMMITS_SIN_PUSHEAR")
        if rec["n_dirty_tracked"] > 0:
            causas.append("ARBOL_SUCIO")
        if rec["n_untracked"] > 0:
            causas.append("ARCHIVOS_SIN_TRACKEAR")
        if not causas:
            causas.append("AL_DIA")
        rec["causas"] = causas
        pend_out.append(rec)
        if i % 10 == 0:
            print(f"  ... {i}/{len(pend)}")

    # resumen causas
    from collections import Counter
    cc = Counter()
    for r in pend_out:
        for c in r.get("causas", []):
            cc[c] += 1
    print("\nCAUSAS PENDING:", dict(cc))

    OUT.write_text(json.dumps({
        "faltantes_reales": reales,
        "faltantes_anidados": anidados,
        "pendientes": pend_out,
        "resumen_causas": dict(cc),
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado: {OUT}")

    print("\n=== FALTANTES REALES (no anidados) ===")
    for x in sorted(reales, key=lambda y: -(y["size_mb"] or 0)):
        print(f'{x["name"][:44]:<44} {x["size_mb"]:>8} MB  {x["verdict"]:<14} {x["path"]}')


if __name__ == "__main__":
    main()
