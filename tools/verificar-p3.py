#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verificar-p3.py - Confirma que las ramas rescate-detached estan publicadas."""
import os
import subprocess

E = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def buscar(nombre):
    for base in (r"C:\Users\USER\Desktop", r"C:\Users\USER\Documents", r"C:\Users\USER\repos"):
        if not os.path.isdir(base):
            continue
        for root, dirs, _ in os.walk(base, onerror=lambda e: None):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            if os.path.basename(root) == nombre and os.path.isdir(os.path.join(root, ".git")):
                return root
    return None


for n in ("agentbox", "nexus-data"):
    d = buscar(n)
    if not d:
        print(f"  {n}: no encontrado")
        continue
    r = subprocess.run(["git", "-C", d, "ls-remote", "--heads", "origin"],
                       capture_output=True, text=True, env=E, timeout=90)
    ramas = [l.split("refs/heads/")[-1] for l in r.stdout.splitlines() if "refs/heads/" in l]
    tiene = "rescate-detached" in ramas
    print(f"  {n}: {'PUBLICADA' if tiene else 'NO publicada'}  -> remoto tiene: {ramas}")
