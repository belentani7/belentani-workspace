#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test-auth-real.py - Determina si "Repository not found" es un problema de
autenticacion o si el repo realmente no existe.

Estrategia:
 1. Probar ls-remote contra repos del inventario marcados private=true.
    Si funciona -> las credenciales sirven -> "not found" es genuino.
 2. Consultar la API de GitHub (si hay token) por los nombres concretos.
Solo lectura.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\USER\Desktop\produccion")
ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def run(*args, timeout=90):
    try:
        p = subprocess.run(list(args), capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace",
                           env=ENV)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return 1, "", f"EXC: {e}"


def main():
    gh = json.loads((BASE / "github-inventario.json").read_text(encoding="utf-8"))
    priv = [r for r in gh if r.get("private")][:6]
    publ = [r for r in gh if not r.get("private")][:4]

    print("== A. ls-remote contra repos PRIVADOS del inventario (test de credenciales) ==")
    for r in priv:
        url = r["url"].rstrip("/") + ".git"
        rc, out, err = run("git", "ls-remote", "--heads", url, timeout=60)
        heads = len([l for l in out.splitlines() if l.strip()])
        print(f'  PRIV {r["name"][:34]:<34} rc={rc} heads={heads} err={err[:110]}')

    print("\n== B. ls-remote contra repos PUBLICOS del inventario ==")
    for r in publ:
        url = r["url"].rstrip("/") + ".git"
        rc, out, err = run("git", "ls-remote", "--heads", url, timeout=60)
        heads = len([l for l in out.splitlines() if l.strip()])
        print(f'  PUB  {r["name"][:34]:<34} rc={rc} heads={heads} err={err[:110]}')

    print("\n== C. Comprobacion de los nombres ausentes via API GitHub ==")
    # buscar token en el entorno / git credential helper
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not tok:
        for f in BASE.parent.glob("**/.env*"):
            pass
        # intentar gh cli
        rc, out, err = run("gh", "auth", "token", timeout=30)
        if rc == 0 and out.strip():
            tok = out.strip()
            print("  (token obtenido de gh CLI)")
    if not tok:
        rc, out, err = run("git", "credential", "fill", timeout=20)
        print("  no hay GITHUB_TOKEN/GH_TOKEN en el entorno; gh CLI:",
              "no disponible" if err else err[:80])
    else:
        print("  token presente (longitud oculta)")

    dudosos = ["edu-engine", "william-game", "belentani-neural-icons-hbo-noir",
               "omega-os", "omega-os-v4", "judas-red-front", "desktop", "engine"]
    import urllib.request
    for n in dudosos:
        owner = "roberto7sena-maker" if "neural-icons" in n else "belentani7"
        api = f"https://api.github.com/repos/{owner}/{n}"
        req = urllib.request.Request(api, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "audit",
            **({"Authorization": f"Bearer {tok}"} if tok else {}),
        })
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
                print(f'  {owner}/{n:<34} HTTP {resp.status} existe=True '
                      f'private={data.get("private")} pushed={data.get("pushed_at")}')
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", "?")
            print(f'  {owner}/{n:<34} HTTP {code} existe=False ({type(e).__name__})')


if __name__ == "__main__":
    main()
