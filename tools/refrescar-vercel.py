#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
refrescar-vercel.py - Intenta renovar el token de Vercel usando el refreshToken
guardado, sin necesidad de login por navegador.
"""
from __future__ import annotations

import json
import shutil
import time
from datetime import datetime
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

console = Console()
AUTH = Path.home() / "AppData/Roaming/com.vercel.cli/Data/auth.json"


def mask(v: str) -> str:
    v = str(v)
    return v[:8] + "*" * max(0, len(v) - 12) + v[-4:] if len(v) > 14 else "*" * len(v)


def main():
    if not AUTH.exists():
        console.print("[red]No existe auth.json[/]")
        return

    d = json.loads(AUTH.read_text(encoding="utf-8"))
    console.print("[bold]Contenido de auth.json[/]")
    for k, v in d.items():
        if k.startswith("//"):
            continue
        console.print(f"  {k:<14} = {mask(v)}")

    exp = d.get("expiresAt")
    if exp:
        try:
            dt = datetime.fromtimestamp(int(exp))
            console.print(f"\n  expiresAt -> {dt:%Y-%m-%d %H:%M} "
                          f"({'CADUCADO' if dt < datetime.now() else 'vigente'})")
        except Exception:
            pass

    token = d.get("token")
    refresh = d.get("refreshToken")
    if not refresh:
        console.print("[yellow]No hay refreshToken: no se puede renovar sin login.[/]")
        return

    console.print(f"\n[bold]Intentando renovar con refreshToken...[/]")

    # Vercel CLI usa este endpoint OAuth
    intentos = [
        ("https://api.vercel.com/login/oauth/token",
         {"grant_type": "refresh_token", "refresh_token": refresh},
         "form"),
        ("https://api.vercel.com/v2/oauth/access_token",
         {"grant_type": "refresh_token", "refresh_token": refresh},
         "form"),
    ]

    nuevo = None
    for url, data, modo in intentos:
        try:
            r = httpx.post(url, data=data, timeout=30,
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
            console.print(f"  {url} -> HTTP {r.status_code}")
            if r.status_code == 200:
                j = r.json()
                if j.get("access_token"):
                    nuevo = j
                    console.print(f"  [green]TOKEN RENOVADO[/]")
                    break
            else:
                console.print(f"     {(r.text or '')[:120]}")
        except Exception as e:  # noqa: BLE001
            console.print(f"  {url} -> error: {str(e)[:70]}")

    if nuevo:
        # backup y escritura
        ts = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy(AUTH, AUTH.with_suffix(f".json.bak-{ts}"))
        d["token"] = nuevo["access_token"]
        if nuevo.get("refresh_token"):
            d["refreshToken"] = nuevo["refresh_token"]
        if nuevo.get("expires_in"):
            d["expiresAt"] = int(time.time()) + int(nuevo["expires_in"])
        AUTH.write_text(json.dumps(d, indent=2), encoding="utf-8")
        console.print(f"[green]auth.json actualizado (backup .bak-{ts})[/]")
    else:
        console.print("\n[yellow]No se pudo renovar automaticamente.[/]")
        console.print("  El refreshToken de Vercel CLI puede requerir el flujo de dispositivo.")
        console.print("  Alternativa: crear un token en https://vercel.com/account/tokens")
        console.print("  y guardarlo como variable VERCEL_TOKEN.")

    # Comprobar si hay VERCEL_TOKEN en el entorno
    console.print("\n[bold]Buscando alternativas de token[/]")
    import subprocess
    for var in ("VERCEL_TOKEN", "VERCEL_API_TOKEN"):
        p = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "[Environment]::GetEnvironmentVariable('%s','User')" % var],
            capture_output=True, text=True, timeout=20)
        v = (p.stdout or "").strip()
        if v:
            console.print(f"  {var}: presente ({mask(v)})")
            try:
                r = httpx.get("https://api.vercel.com/v2/user",
                              headers={"Authorization": f"Bearer {v}"}, timeout=25)
                if r.status_code == 200:
                    u = r.json().get("user", {})
                    console.print(f"     [green]VALIDA[/] user={u.get('username') or u.get('email')}")
                else:
                    console.print(f"     [red]HTTP {r.status_code}[/]")
            except Exception as e:  # noqa: BLE001
                console.print(f"     error: {str(e)[:50]}")
        else:
            console.print(f"  {var}: ausente")


if __name__ == "__main__":
    main()
