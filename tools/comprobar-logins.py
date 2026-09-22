#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comprobar-logins.py - Comprueba el estado de autenticacion de TODOS los CLIs
y plataformas del sistema, uno por uno, sin depender de regex fragiles.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
HOME = Path.home()


def user_env(name: str) -> str:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetEnvironmentVariable('%s','User')" % name],
        capture_output=True, text=True, timeout=20)
    return (p.stdout or "").strip()


def run(exe: str, args: list[str], timeout: int = 60) -> tuple[int, str]:
    """Ejecuta un CLI y devuelve (codigo, salida_combinada)."""
    env = {**os.environ}
    # inyectar GH_TOKEN para que gh funcione
    if "GH_TOKEN" not in env:
        t = user_env("GITHUB_TOKEN")
        if t:
            env["GH_TOKEN"] = t
    try:
        p = subprocess.run([exe, *args], capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace",
                           env=env, cwd=str(HOME))
        return p.returncode, ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
    except subprocess.TimeoutExpired:
        return 124, "(timeout)"
    except FileNotFoundError:
        return 127, "(no encontrado)"
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def clasificar(salida: str, ok_pat: str, ko_pat: str) -> tuple[str, str]:
    """Devuelve (estado, detalle)."""
    low = salida.lower()
    if re.search(ko_pat, low):
        return "NO", salida.splitlines()[0][:70] if salida else ""
    m = re.search(ok_pat, salida, re.I)
    if m:
        return "SI", m.group(0)[:70]
    return "?", (salida.splitlines()[0][:70] if salida else "(sin salida)")


def main():
    resultados = []

    # ---------- GITHUB ----------
    code, out = run("gh", ["auth", "status"])
    estado, det = clasificar(out, r"Logged in to \S+ account \S+", r"not logged into any")
    resultados.append(("GitHub CLI (gh)", estado, det))

    # GitHub API con token
    tok = user_env("GITHUB_TOKEN")
    if tok:
        try:
            r = httpx.get("https://api.github.com/user",
                          headers={"Authorization": f"Bearer {tok}",
                                   "User-Agent": "dsh"}, timeout=25)
            if r.status_code == 200:
                d = r.json()
                resultados.append(("GitHub API (token)", "SI",
                                   f"user={d['login']} pub={d['public_repos']} priv={d['total_private_repos']}"))
            else:
                resultados.append(("GitHub API (token)", "NO", f"HTTP {r.status_code}"))
        except Exception as e:  # noqa: BLE001
            resultados.append(("GitHub API (token)", "NO", str(e)[:50]))
    else:
        resultados.append(("GitHub API (token)", "NO", "sin GITHUB_TOKEN"))

    # git credential helper
    p = subprocess.run(["git", "config", "--global", "--get-all",
                        "credential.https://github.com.helper"],
                       capture_output=True, text=True, timeout=20)
    helper = (p.stdout or "").strip()
    if "gh.exe" in helper:
        resultados.append(("git credenciales", "NO", "helper apunta a gh (sin login)"))
    elif helper:
        resultados.append(("git credenciales", "SI", "helper con token"))
    else:
        resultados.append(("git credenciales", "?", "sin helper configurado"))

    # ---------- PLATAFORMAS DE DEPLOY ----------
    code, out = run(r"C:\Users\USER\AppData\Roaming\npm\vercel.cmd", ["whoami"])
    if "logged out" in out.lower():
        # el token existe pero caduco: comprobar expiresAt
        auth = HOME / "AppData/Roaming/com.vercel.cli/Data/auth.json"
        extra = "token caducado"
        if auth.exists():
            try:
                d = json.loads(auth.read_text(encoding="utf-8"))
                exp = d.get("expiresAt")
                if exp:
                    import datetime
                    dt = datetime.datetime.fromtimestamp(int(exp))
                    dias = (datetime.datetime.now() - dt).days
                    extra = f"caduco hace {dias} dia(s) ({dt:%Y-%m-%d})"
            except Exception:
                pass
        resultados.append(("Vercel", "NO", extra))
    else:
        estado, det = clasificar(out, r"^[a-z0-9\-_]+$", r"logged out|not logged")
        resultados.append(("Vercel", estado, det))

    code, out = run(r"C:\Users\USER\AppData\Roaming\npm\netlify.cmd", ["status"])
    if "Netlify User" in out or "Email:" in out:
        m = re.search(r"Email:\s*(\S+)", out)
        resultados.append(("Netlify", "SI", m.group(1) if m else "autenticado"))
    else:
        estado, det = clasificar(out, r"logged in", r"not logged|error")
        resultados.append(("Netlify", estado, det))

    code, out = run(r"C:\Users\USER\AppData\Roaming\npm\wrangler.cmd", ["whoami"])
    if "logged in" in out.lower():
        m = re.search(r"associated with the email (\S+)", out)
        resultados.append(("Cloudflare (wrangler)", "SI", m.group(1) if m else "autenticado"))
    else:
        estado, det = clasificar(out, r"logged in", r"not authenticated|not logged")
        resultados.append(("Cloudflare (wrangler)", estado, det))

    # ---------- PUBLICACION ----------
    code, out = run("node", [r"C:\Users\USER\AppData\Roaming\npm\node_modules\@unravel-tech\thing\src\index.js",
                             "accounts", "--json"])
    if '"accounts":[]' in out.replace(" ", ""):
        resultados.append(("thing (usething.ai)", "NO", "sin cuenta"))
    elif '"accounts"' in out:
        try:
            d = json.loads(out[out.find("{"):])
            n = len(d.get("accounts") or [])
            resultados.append(("thing (usething.ai)", "SI" if n else "NO", f"{n} cuenta(s)"))
        except Exception:
            resultados.append(("thing (usething.ai)", "?", out[:50]))
    else:
        resultados.append(("thing (usething.ai)", "?", out[:50]))

    # ---------- AGENTES ----------
    code, out = run(r"C:\Users\USER\AppData\Roaming\npm\claude.cmd", ["auth", "status"])
    # claude devuelve JSON: {"loggedIn":true,"authMethod":"oauth_token",...}
    m = re.search(r"\{.*\}", out, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            if d.get("loggedIn"):
                resultados.append(("Claude Code", "SI",
                                   f"{d.get('authMethod')} / {d.get('apiProvider')}"))
            else:
                resultados.append(("Claude Code", "NO", "loggedIn=false"))
        except Exception:
            resultados.append(("Claude Code", "?", out[:60]))
    else:
        estado, det = clasificar(out, r"logged in|authenticated", r"not logged|no auth")
        resultados.append(("Claude Code", estado, det))

    code, out = run(r"C:\Users\USER\AppData\Roaming\npm\gemini.cmd", ["--version"])
    oauth = HOME / ".gemini" / "oauth_creds.json"
    if oauth.exists():
        try:
            d = json.loads(oauth.read_text(encoding="utf-8"))
            exp = d.get("expiry_date") or d.get("expiry")
            resultados.append(("Gemini CLI", "SI", f"oauth_creds.json (exp: {exp})"))
        except Exception:
            resultados.append(("Gemini CLI", "?", "oauth_creds.json ilegible"))
    else:
        resultados.append(("Gemini CLI", "NO", "sin oauth_creds.json"))

    # opencode: auth.json
    oc = HOME / ".local" / "share" / "opencode" / "auth.json"
    if oc.exists():
        try:
            d = json.loads(oc.read_text(encoding="utf-8"))
            provs = list(d.keys())
            resultados.append(("OpenCode", "SI" if provs else "NO",
                               f"{len(provs)} proveedores: {', '.join(provs[:6])}"))
        except Exception:
            resultados.append(("OpenCode", "?", "auth.json ilegible"))
    else:
        resultados.append(("OpenCode", "?", "sin auth.json"))

    # codex: config con env_key
    codex = HOME / ".codex" / "config.toml"
    if codex.exists():
        txt = codex.read_text(encoding="utf-8", errors="replace")
        plain = "experimental_bearer_token" in txt
        resultados.append(("Codex", "SI", "config OK" + (" (clave en texto plano!)" if plain else "")))

    # aider: config
    aid = HOME / ".aider" / "config.yml"
    if aid.exists():
        resultados.append(("Aider", "SI", "config.yml presente"))

    # ---------- OTROS ----------
    code, out = run("docker", ["version"])
    resultados.append(("Docker", "NO" if "no encontrado" in out or code == 127 else "SI",
                       "no instalado" if code == 127 else out.splitlines()[0][:60]))

    # navegadores/servicios ya comprobados antes
    for nombre, ruta in [("Google Drive", Path(r"C:\Program Files\Google\Drive File Stream")),
                         ("OneDrive", HOME / "OneDrive")]:
        resultados.append((nombre, "SI" if ruta.exists() else "NO",
                           "instalado" if ruta.exists() else "no encontrado"))

    # ---------- TABLA ----------
    t = Table(title="ESTADO DE TODOS LOS LOGINS", border_style="cyan")
    t.add_column("Servicio", style="bold", max_width=24)
    t.add_column("Login")
    t.add_column("Detalle", max_width=54)
    color = {"SI": "green", "NO": "red", "?": "yellow"}
    for nombre, estado, det in resultados:
        t.add_row(nombre, f"[{color.get(estado,'white')}]{estado}[/]", det)
    console.print(t)

    ok = sum(1 for _, e, _ in resultados if e == "SI")
    no = sum(1 for _, e, _ in resultados if e == "NO")
    dud = sum(1 for _, e, _ in resultados if e == "?")
    console.print(f"\n[green]OK: {ok}[/]   [red]Faltan: {no}[/]   [yellow]Dudosos: {dud}[/]")

    faltan = [(n, d) for n, e, d in resultados if e == "NO"]
    if faltan:
        console.print("\n[red bold]PENDIENTES DE LOGIN:[/]")
        for n, d in faltan:
            console.print(f"   {n:<24} {d}")


if __name__ == "__main__":
    main()
