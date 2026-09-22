#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
api-check-ausentes.py - Confirma via API REST de GitHub si existen los repos
con remoto belentani7/roberto7sena-maker que git reporta como "not found".
Solo lectura.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request

BASE = r"C:\Users\USER\Desktop\produccion"


def token():
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(k):
            return os.environ[k], f"env:{k}"
    try:
        p = subprocess.run(["gh", "auth", "token"], capture_output=True,
                           text=True, timeout=25, encoding="utf-8",
                           errors="replace")
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip(), "gh CLI"
    except Exception:  # noqa: BLE001
        pass
    return "", "sin token"


def main():
    tok, src = token()
    print(f"Token: {'presente' if tok else 'AUSENTE'} ({src})\n")

    candidatos = [
        ("belentani7", "edu-engine"),
        ("belentani7", "william-game"),
        ("belentani7", "omega-os"),
        ("belentani7", "omega-os-v4"),
        ("belentani7", "judas-red-front"),
        ("belentani7", "desktop"),
        ("belentani7", "engine"),
        ("roberto7sena-maker", "belentani-neural-icons-hbo-noir"),
        # control: un repo que SI esta en el inventario
        ("belentani7", "belentani-platform"),
        ("belentani7", "hbo-noir-icons"),
    ]
    for owner, name in candidatos:
        url = f"https://api.github.com/repos/{owner}/{name}"
        hdrs = {"Accept": "application/vnd.github+json", "User-Agent": "audit"}
        if tok:
            hdrs["Authorization"] = f"Bearer {tok}"
        req = urllib.request.Request(url, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
                print(f'  {owner}/{name:<38} HTTP {r.status} EXISTE '
                      f'private={d.get("private")} pushed={d.get("pushed_at")} '
                      f'default={d.get("default_branch")}')
        except urllib.error.HTTPError as e:
            print(f'  {owner}/{name:<38} HTTP {e.code} NO-EXISTE/NO-ACCESO')
        except Exception as e:  # noqa: BLE001
            print(f'  {owner}/{name:<38} ERROR {type(e).__name__}: {e}')


if __name__ == "__main__":
    main()
