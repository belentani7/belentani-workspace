#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
clasificar-publicar.py - Lista DEFINITIVA de repos locales cuyo contenido no
esta publicado en GitHub, con la causa exacta.

Reglas:
  - Se excluyen subcarpetas anidadas dentro de otro repo (.git en un padre).
  - Se separan los clones de terceros (el remoto apunta a un repo upstream
    publico que SI existe) de los repos propios sin publicar.
  - Los remotos que devuelven 404 se cuentan como NO PUBLICADO (verificado
    antes con git ls-remote + API en test-auth-real.py / api-check-ausentes.py).
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
        p = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


UPSTREAM_HOSTS = ("github.com/ollama/", "github.com/audacity/", "github.com/spotify/",
                  "github.com/facebookresearch/", "github.com/anthropics/",
                  "github.com/deepseek-ai/", "github.com/onlook-dev/",
                  "github.com/Sanster/", "github.com/slhck/", "github.com/sergree/",
                  "github.com/RVC-Project/", "github.com/mattpocock/",
                  "github.com/adrianhajdin/", "github.com/openvideodev/",
                  "github.com/paperclipai/", "github.com/thoughtbot/",
                  "github.com/kreeti/", "github.com/eatonphil/",
                  "github.com/omacom/", "github.com/lidojs/", "github.com/Davronov-Alimardon/",
                  "github.com/affaan-m/", "github.com/tashfeenahmed/",
                  "github.com/Natively-AI-assistant/", "github.com/Augani/",
                  "github.com/willian-bl/", "github.com/xzm2004260/",
                  "github.com/BazedFrog/", "github.com/SpeechifyInc/",
                  "github.com/kakoman27/", "github.com/hccccc01333/",
                  "github.com/liuqing0224/", "github.com/unravel-team/")


def main():
    estado = json.loads((BASE / "estado.json").read_text(encoding="utf-8"))
    gh = json.loads((BASE / "github-inventario.json").read_text(encoding="utf-8"))
    cruce = json.loads((BASE / "auditoria-cruce.json").read_text(encoding="utf-8"))
    gh_names = {r["name"].lower() for r in gh}

    falt = cruce["faltantes_reales"] + cruce["faltantes_anidados"]

    propios, terceros, sinrem = [], [], []
    for x in falt:
        if x["is_nested"]:
            continue
        rem = (x.get("remote") or "").strip()
        # datos en vivo
        rc, head, _ = git(x["path"], "rev-parse", "HEAD")
        rc2, cnt, _ = git(x["path"], "rev-list", "--count", "HEAD")
        rc3, last, _ = git(x["path"], "log", "-1", "--format=%cI|%s")
        rc4, st, _ = git(x["path"], "status", "--porcelain")
        n_dirty = len([l for l in st.splitlines() if l.strip()]) if rc4 == 0 else None
        rec = dict(x)
        rec.update({
            "n_commits": int(cnt) if cnt.isdigit() else 0,
            "last_commit": last[:140] if rc3 == 0 else "",
            "n_cambios_sin_commit": n_dirty,
        })
        if not rem:
            sinrem.append(rec)
        elif any(u in rem for u in UPSTREAM_HOSTS):
            terceros.append(rec)
        else:
            propios.append(rec)

    print(f"=== A. PROPIOS con remoto que NO EXISTE en GitHub (404 verificado): {len(propios)} ===")
    for x in sorted(propios, key=lambda y: -(y["size_mb"] or 0)):
        print(f'  {x["name"][:36]:<36} {x["size_mb"]:>7} MB  commits={x["n_commits"]:<4} '
              f'sin_commit={x["n_cambios_sin_commit"]}')
        print(f'      {x["path"]}')
        print(f'      remote: {x["remote"]}')
        print(f'      last: {x["last_commit"]}')

    print(f"\n=== B. SIN REMOTO (no publicado, sin URL de destino): {len(sinrem)} ===")
    for x in sorted(sinrem, key=lambda y: -(y["size_mb"] or 0)):
        print(f'  {x["name"][:36]:<36} {x["size_mb"]:>7} MB  commits={x["n_commits"]:<4} '
              f'sin_commit={x["n_cambios_sin_commit"]}')
        print(f'      {x["path"]}')
        print(f'      last: {x["last_commit"]}')

    print(f"\n=== C. CLONES DE TERCEROS (upstream ya existe; local no es 'propio'): {len(terceros)} ===")
    for x in sorted(terceros, key=lambda y: -(y["size_mb"] or 0)):
        print(f'  {x["name"][:36]:<36} {x["size_mb"]:>7} MB  verdict={x["verdict"]:<14} '
              f'commits={x["n_commits"]:<5} sin_commit={x["n_cambios_sin_commit"]}')
        print(f'      {x["remote"]}')

    # comprobacion de los NO_REMOTE que SI casaron por nombre
    print("\n=== D. NO_REMOTE del estado que casaron por nombre en el inventario ===")
    for s in estado:
        if s["verdict"] == "NO_REMOTE" and s["name"].lower() in gh_names:
            rc, cnt, _ = git(s["path"], "rev-list", "--count", "HEAD")
            rc2, st, _ = git(s["path"], "status", "--porcelain")
            nd = len([l for l in st.splitlines() if l.strip()]) if rc2 == 0 else None
            print(f'  {s["name"][:34]:<34} {s["size_mb"]:>6} MB commits={cnt} '
                  f'sin_commit={nd}  -> el nombre existe en GitHub pero el local NO tiene remoto')

    out = {"propios_remoto_404": propios, "sin_remoto": sinrem,
           "clones_terceros": terceros}
    (BASE / "faltan-publicar.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado: {BASE / 'faltan-publicar.json'}")


if __name__ == "__main__":
    main()
