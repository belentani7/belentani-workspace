#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vercel-device-login.py - Autentica Vercel por device flow (sin navegador del CLI).

Flujo:
  1. Descubre los endpoints OIDC de vercel.com
  2. Pide un device_code + user_code
  3. Muestra la URL y el codigo al usuario
  4. Sondea el token_endpoint hasta que el usuario autorice
  5. Guarda el token en auth.json y en VERCEL_TOKEN

Uso:
  python vercel-device-login.py --start   # solo pide codigo y lo muestra
  python vercel-device-login.py --poll    # sondea hasta obtener token
  python vercel-device-login.py           # start + poll (bloqueante)
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import httpx
from rich.console import Console

console = Console()

CLIENT_ID = "cl_HYyOPBNtFMfHhaUn9L4QPfTZz6TP47bp"
ISSUER = "https://vercel.com"
AUTH = Path.home() / "AppData/Roaming/com.vercel.cli/Data/auth.json"
STATE = Path(r"C:\Users\USER\Desktop\produccion\vercel-device.json")
UA = "vercel-cli/59.16.0 node-v26"


def descubrir() -> dict:
    url = f"{ISSUER}/.well-known/openid-configuration"
    r = httpx.get(url, headers={"user-agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()


def start():
    as_meta = descubrir()
    console.print(f"[dim]token_endpoint: {as_meta.get('token_endpoint')}[/]")
    r = httpx.post(as_meta["device_authorization_endpoint"],
                   data={"client_id": CLIENT_ID, "scope": "openid offline_access"},
                   headers={"Content-Type": "application/x-www-form-urlencoded",
                            "user-agent": UA},
                   timeout=30)
    if r.status_code != 200:
        console.print(f"[red]HTTP {r.status_code}: {r.text[:200]}[/]")
        return None
    d = r.json()
    STATE.write_text(json.dumps({**d, "token_endpoint": as_meta["token_endpoint"],
                                 "creado": time.time()}, indent=2), encoding="utf-8")

    console.print()
    console.print("[bold green]" + "=" * 66 + "[/]")
    console.print("[bold green]  AUTORIZA VERCEL EN TU NAVEGADOR[/]")
    console.print("[bold green]" + "=" * 66 + "[/]")
    console.print()
    console.print(f"  1. Abre:   [bold cyan]{d.get('verification_uri_complete') or d.get('verification_uri')}[/]")
    console.print(f"  2. Codigo: [bold yellow]{d.get('user_code')}[/]")
    console.print()
    console.print(f"  Caduca en {d.get('expires_in', 300)} s. Sondeo cada {d.get('interval', 5)} s.")
    console.print("[bold green]" + "=" * 66 + "[/]")
    return d


def poll(max_seconds: int = 600):
    if not STATE.exists():
        console.print("[red]Ejecuta primero --start[/]")
        return None
    st = json.loads(STATE.read_text(encoding="utf-8"))
    token_endpoint = st["token_endpoint"]
    device_code = st["device_code"]
    interval = int(st.get("interval", 5))
    inicio = time.time()

    console.print(f"\n[dim]Sondeando {token_endpoint} ...[/]")
    while time.time() - inicio < max_seconds:
        try:
            r = httpx.post(token_endpoint,
                           data={"client_id": CLIENT_ID,
                                 "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                                 "device_code": device_code},
                           headers={"Content-Type": "application/x-www-form-urlencoded",
                                    "user-agent": UA},
                           timeout=30)
            if r.status_code == 200:
                return r.json()
            j = {}
            try:
                j = r.json()
            except Exception:
                pass
            err = j.get("error", "")
            if err in ("authorization_pending", "slow_down"):
                if err == "slow_down":
                    interval += 2
                time.sleep(interval)
                continue
            console.print(f"  [red]{err or r.status_code}: {j.get('error_description','')[:120]}[/]")
            return None
        except Exception as e:  # noqa: BLE001
            console.print(f"  [yellow]error de red, reintentando: {str(e)[:60]}[/]")
            time.sleep(interval)
    console.print("[red]Tiempo agotado esperando autorizacion.[/]")
    return None


def guardar(tok: dict):
    access = tok.get("access_token")
    if not access:
        console.print("[red]Sin access_token en la respuesta[/]")
        return
    console.print(f"\n[green]TOKEN OBTENIDO[/] ({access[:10]}...)")

    if AUTH.exists():
        ts = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy(AUTH, AUTH.with_suffix(f".json.bak-{ts}"))
    d = {}
    if AUTH.exists():
        try:
            d = json.loads(AUTH.read_text(encoding="utf-8"))
        except Exception:
            d = {}
    d["token"] = access
    if tok.get("refresh_token"):
        d["refreshToken"] = tok["refresh_token"]
    if tok.get("expires_in"):
        d["expiresAt"] = int(time.time()) + int(tok["expires_in"])
    d.setdefault("userId", d.get("userId", ""))
    AUTH.parent.mkdir(parents=True, exist_ok=True)
    AUTH.write_text(json.dumps(d, indent=2), encoding="utf-8")
    console.print(f"[green]auth.json actualizado[/]")

    # Verificar que funciona
    try:
        r = httpx.get("https://api.vercel.com/v2/user",
                      headers={"Authorization": f"Bearer {access}"}, timeout=25)
        if r.status_code == 200:
            u = r.json().get("user", {})
            console.print(f"[green]VERIFICADO[/] usuario={u.get('username') or u.get('email')}")
    except Exception as e:  # noqa: BLE001
        console.print(f"[yellow]no se pudo verificar: {str(e)[:60]}[/]")

    # Guardar tambien como variable de usuario
    import subprocess
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    "[Environment]::SetEnvironmentVariable('VERCEL_TOKEN','%s','User')" % access],
                   capture_output=True, text=True)
    console.print("[green]VERCEL_TOKEN guardado a nivel de usuario[/]")


if __name__ == "__main__":
    if "--start" in sys.argv:
        start()
    elif "--poll" in sys.argv:
        t = poll()
        if t:
            guardar(t)
    elif "--status" in sys.argv:
        if AUTH.exists():
            d = json.loads(AUTH.read_text(encoding="utf-8"))
            exp = d.get("expiresAt")
            console.print(f"token: {str(d.get('token'))[:12]}...")
            if exp:
                import datetime
                dt = datetime.datetime.fromtimestamp(int(exp))
                console.print(f"expira: {dt:%Y-%m-%d %H:%M} "
                              f"({'CADUCADO' if dt < datetime.datetime.now() else 'vigente'})")
    else:
        d = start()
        if d:
            t = poll()
            if t:
                guardar(t)
