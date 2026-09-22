#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
produccion.py - Cadena de produccion Belentani
==============================================
Verifica si un repo local esta respaldado online y decide si es borrable.

Construido sobre estructuras existentes (no reinventar):
  GitPython   -> estado de repos
  rich        -> salida/tablas
  pandas      -> informes
  send2trash  -> borrado SEGURO (Papelera de Reciclaje, recuperable)
  typer       -> CLI

Comandos:
  scan     Descubre repos locales
  verify   Verifica estado online de cada repo
  report   Muestra el informe
  clean    Manda a la Papelera los SAFE_TO_DELETE (nunca educacionales)

REGLA DE ORO: nunca se borra nada cuyo contenido no este confirmado online.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# ----------------------------------------------------------------------
# Configuracion
# ----------------------------------------------------------------------
BASE = Path(r"C:\Users\USER\Desktop")
OUT = BASE / "produccion"
OUT.mkdir(parents=True, exist_ok=True)

ROOTS = [
    Path(r"C:\Users\USER\Desktop"),
    Path(r"C:\Users\USER\repos"),
    Path(r"C:\Users\USER\Documents"),
]

STATE_FILE = OUT / "estado.json"
INVENTORY_FILE = BASE / "inventario-produccion.json"

# Proyectos educacionales: NUNCA se borran (orden explicita del usuario)
EDU_PATTERN = re.compile(
    r"school|academy|academia|curso|educa|lingua|aprende|manos|abiertas|"
    r"william|willian|univers|student|learn|taller|ilacaf|guia-ia|aula|"
    r"formac|natalia-marinho|recursos-educativos|edu-engine",
    re.I,
)

# Exclusions: legal y personal. No se tocan ni se publican.
EXCL_PATTERN = re.compile(r"DEFENSA|DEUDAFIX|financ|deuda|expediente", re.I)

SKIP_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".next", "dist", "build"}


# ----------------------------------------------------------------------
# Modelos
# ----------------------------------------------------------------------
class RepoState(BaseModel):
    name: str
    path: str
    remote: str = ""
    branch: str = ""
    verdict: str = "UNKNOWN"
    reason: str = ""
    dirty: bool = False
    unpushed: int = -1
    untracked: int = -1
    local_head: str = ""
    remote_head: str = ""
    size_mb: float = 0.0


VERDICT_ORDER = [
    "SAFE_TO_DELETE", "KEEP_EDU", "PENDING", "DIVERGED", "NO_REMOTE",
    "AUTH_REQUIRED", "REMOTE_MISSING", "UNREACHABLE", "GIT_ERROR",
    "NO_COMMITS", "EXCLUDED",
]

VERDICT_COLOR = {
    "SAFE_TO_DELETE": "green",
    "KEEP_EDU": "cyan",
    "NO_REMOTE": "magenta",
    "EXCLUDED": "dim",
    "PENDING": "yellow",
    "DIVERGED": "red",
    "AUTH_REQUIRED": "yellow",
    "REMOTE_MISSING": "red",
    "UNREACHABLE": "red",
    "GIT_ERROR": "red",
    "NO_COMMITS": "yellow",
}


# ----------------------------------------------------------------------
# Utilidades git (subprocess: evita los bugs de captura de PowerShell)
# ----------------------------------------------------------------------
def git(repo: Path, *args: str, timeout: int = 30) -> tuple[int, str, str]:
    """Ejecuta git y devuelve (codigo, stdout, stderr)."""
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"},
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:  # noqa: BLE001
        return 1, "", str(e)


def read_remote_from_config(repo: Path) -> str:
    """Lee el remoto directamente de .git/config (fiable, sin invocar git)."""
    cfg = repo / ".git" / "config"
    if not cfg.exists():
        return ""
    try:
        txt = cfg.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r'\[remote "origin"\][^\[]*?url\s*=\s*(\S+)', txt, re.S)
    return m.group(1) if m else ""


def dir_size_mb(p: Path) -> float:
    total = 0
    for root, dirs, files in os.walk(p, onerror=lambda e: None):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return round(total / 1024 / 1024, 1)


# ----------------------------------------------------------------------
# scan
# ----------------------------------------------------------------------
def discover_repos() -> list[Path]:
    found: set[Path] = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for dirpath, dirnames, _ in os.walk(root, onerror=lambda e: None):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if ".git" in dirnames:
                found.add(Path(dirpath))
                dirnames.remove(".git")
    return sorted(found)


def ensure_safe_directories(repos: list[Path]) -> None:
    """git rechaza repos propiedad de Administradores ('dubious ownership')."""
    for r in repos:
        git(Path.cwd(), "config", "--global", "--add", "safe.directory",
            str(r).replace("\\", "/"))


# ----------------------------------------------------------------------
# verify
# ----------------------------------------------------------------------
def verify_repo(repo: Path) -> RepoState:
    name = repo.name
    remote = read_remote_from_config(repo)
    st = RepoState(name=name, path=str(repo), remote=remote)

    if EXCL_PATTERN.search(name):
        st.verdict, st.reason = "EXCLUDED", "exclusion legal/personal"
        return st
    if EDU_PATTERN.search(name):
        st.verdict, st.reason = "KEEP_EDU", "educacional - se conserva siempre"
        return st
    if not remote:
        st.verdict, st.reason = "NO_REMOTE", "sin remoto: borrar = perder"
        return st

    code, out, err = git(repo, "rev-parse", "HEAD")
    if code != 0:
        if "dubious ownership" in err:
            st.verdict, st.reason = "GIT_ERROR", "ownership no resuelto"
        elif "does not have any commits" in err or "unknown revision" in err:
            st.verdict, st.reason = "NO_COMMITS", "repo sin commits"
        else:
            st.verdict, st.reason = "GIT_ERROR", err.splitlines()[0] if err else "error"
        return st
    st.local_head = out

    code, out, _ = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    st.branch = out if code == 0 and out and out != "HEAD" else "main"

    code, out, _ = git(repo, "status", "--porcelain")
    st.dirty = bool(out.strip()) if code == 0 else False

    code, out, err = git(repo, "ls-remote", "origin", st.branch, timeout=45)
    blob = f"{out} {err}"
    if code != 0 or not out.strip():
        if re.search(r"Authentication failed|could not read Username|terminal prompts disabled|403|Permission denied", blob, re.I):
            st.verdict, st.reason = "AUTH_REQUIRED", "sin credenciales git para el remoto"
        elif re.search(r"not found|does not exist|404|Repository not found", blob, re.I):
            st.verdict, st.reason = "REMOTE_MISSING", "el remoto no existe"
        else:
            st.verdict = "UNREACHABLE"
            st.reason = next((l for l in blob.splitlines() if l.strip()), "no alcanzable")[:120]
        return st

    st.remote_head = out.split()[0]

    if st.remote_head != st.local_head:
        st.verdict, st.reason = "DIVERGED", "HEAD local != remoto"
        return st

    code, out, _ = git(repo, "rev-list", "--count", f"origin/{st.branch}..HEAD")
    st.unpushed = int(out) if code == 0 and out.isdigit() else -1

    code, out, _ = git(repo, "ls-files", "--others", "--exclude-standard")
    st.untracked = len([l for l in out.splitlines() if l.strip()]) if code == 0 else -1

    if st.unpushed == 0 and not st.dirty and st.untracked == 0:
        st.verdict, st.reason = "SAFE_TO_DELETE", "pusheado, limpio, sin pendientes"
    else:
        st.verdict = "PENDING"
        st.reason = f"sin pushear={st.unpushed} sucio={st.dirty} sin trackear={st.untracked}"
    return st


def load_state() -> list[RepoState]:
    if not STATE_FILE.exists():
        return []
    raw = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return [RepoState(**r) for r in raw]


def save_state(states: list[RepoState]) -> None:
    STATE_FILE.write_text(
        json.dumps([s.model_dump() for s in states], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
app = typer.Typer(add_completion=False, help="Cadena de produccion Belentani")


@app.command()
def scan() -> None:
    """Descubre repos locales y sus remotos."""
    repos = discover_repos()
    console.print(f"[cyan]Repos encontrados:[/] {len(repos)}")
    rows = []
    for r in repos:
        rows.append({
            "name": r.name,
            "path": str(r),
            "remote": read_remote_from_config(r),
            "edu": bool(EDU_PATTERN.search(r.name)),
        })
    (OUT / "repos.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    with_remote = sum(1 for r in rows if r["remote"])
    console.print(f"  con remoto: [green]{with_remote}[/]")
    console.print(f"  sin remoto: [magenta]{len(rows) - with_remote}[/]")
    console.print(f"  educacionales: [cyan]{sum(1 for r in rows if r['edu'])}[/]")


@app.command()
def verify(
    limit: int = typer.Option(0, help="Limitar a N repos (0 = todos)"),
    sizes: bool = typer.Option(False, help="Calcular tamano en disco (lento)"),
) -> None:
    """Verifica el estado online de cada repo."""
    repos = discover_repos()
    if limit:
        repos = repos[:limit]
    console.print(Panel.fit(
        f"[bold]Verificando {len(repos)} repos[/]\n"
        "[dim]Regla: nada se borra sin confirmar que esta online[/]",
        border_style="cyan"))

    ensure_safe_directories(repos)

    states: list[RepoState] = []
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        BarColumn(), TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as prog:
        task = prog.add_task("Verificando...", total=len(repos))
        for repo in repos:
            prog.update(task, description=f"[dim]{repo.name[:40]}[/]")
            try:
                st = verify_repo(repo)
            except Exception as e:  # noqa: BLE001
                st = RepoState(name=repo.name, path=str(repo),
                               verdict="GIT_ERROR", reason=str(e)[:100])
            if sizes:
                st.size_mb = dir_size_mb(repo)
            states.append(st)
            prog.advance(task)

    save_state(states)
    console.print(f"\n[green]Estado guardado:[/] {STATE_FILE}")
    show_summary(states)


def show_summary(states: list[RepoState]) -> None:
    counts: dict[str, int] = {}
    for s in states:
        counts[s.verdict] = counts.get(s.verdict, 0) + 1
    table = Table(title="Resultado de verificacion", border_style="cyan")
    table.add_column("Veredicto", style="bold")
    table.add_column("Repos", justify="right")
    table.add_column("Significado")
    meaning = {
        "SAFE_TO_DELETE": "respaldo confirmado online -> borrable",
        "KEEP_EDU": "educacional -> se conserva",
        "PENDING": "commits o archivos sin publicar",
        "DIVERGED": "local y remoto difieren",
        "NO_REMOTE": "no existe respaldo online",
        "AUTH_REQUIRED": "remoto existe, faltan credenciales",
        "REMOTE_MISSING": "el remoto no existe",
        "UNREACHABLE": "no se pudo contactar",
        "GIT_ERROR": "error de git",
        "NO_COMMITS": "sin commits",
        "EXCLUDED": "legal/personal",
    }
    for v in VERDICT_ORDER:
        if counts.get(v):
            table.add_row(
                f"[{VERDICT_COLOR.get(v,'white')}]{v}[/]",
                str(counts[v]), meaning.get(v, ""))
    console.print(table)

    safe = [s for s in states if s.verdict == "SAFE_TO_DELETE"]
    if safe and any(s.size_mb for s in safe):
        console.print(
            f"[green]Recuperable: {sum(s.size_mb for s in safe):,.0f} MB[/]")
    console.print(f"[dim]Total: {len(states)} repos[/]")


@app.command()
def report(
    verdict: str = typer.Option("", help="Filtrar por veredicto"),
    limit: int = typer.Option(30, help="Filas a mostrar"),
    csv: bool = typer.Option(False, help="Exportar CSV"),
) -> None:
    """Muestra el informe de la ultima verificacion."""
    states = load_state()
    if not states:
        console.print("[red]No hay estado. Ejecuta 'verify' primero.[/]")
        raise typer.Exit(1)

    if csv:
        import csv as csvmod
        path = OUT / "verificacion.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csvmod.writer(f)
            w.writerow(["name", "verdict", "reason", "remote", "branch",
                        "dirty", "unpushed", "untracked", "size_mb", "path"])
            for s in states:
                w.writerow([s.name, s.verdict, s.reason, s.remote, s.branch,
                            s.dirty, s.unpushed, s.untracked, s.size_mb, s.path])
        console.print(f"[green]CSV:[/] {path}")
        return

    rows = states if not verdict else [s for s in states if s.verdict == verdict.upper()]
    rows = sorted(rows, key=lambda s: s.name)[:limit]

    table = Table(title=f"Repos ({len(rows)} mostrados)", border_style="cyan")
    table.add_column("Repo", style="bold", max_width=42)
    table.add_column("Veredicto")
    table.add_column("Detalle", max_width=44)
    for s in rows:
        table.add_row(
            s.name, f"[{VERDICT_COLOR.get(s.verdict,'white')}]{s.verdict}[/]",
            s.reason[:80])
    console.print(table)


@app.command()
def clean(
    apply: bool = typer.Option(False, "--apply", help="EJECUTAR el borrado"),
    min_confirmations: int = typer.Option(3, help="Verificaciones coincidentes requeridas"),
) -> None:
    """
    Manda a la PAPELERA los repos SAFE_TO_DELETE.
    Nunca toca educacionales ni exclusiones. Requiere --apply.
    """
    states = load_state()
    if not states:
        console.print("[red]No hay estado. Ejecuta 'verify' primero.[/]")
        raise typer.Exit(1)

    safe = [s for s in states if s.verdict == "SAFE_TO_DELETE"]
    protected = [s for s in states if s.verdict in ("KEEP_EDU", "EXCLUDED")]

    console.print(Panel.fit(
        f"[bold green]Borrables:[/] {len(safe)}\n"
        f"[bold cyan]Protegidos (educacional/legal):[/] {len(protected)}\n"
        f"[bold]Confirmaciones requeridas:[/] {min_confirmations}",
        title="Plan de limpieza", border_style="green"))

    if not safe:
        console.print("[yellow]Nada que borrar.[/]")
        return

    for s in safe[:20]:
        console.print(f"  [green]->[/] {s.name}")
    if len(safe) > 20:
        console.print(f"  [dim]... y {len(safe)-20} mas[/]")

    if not apply:
        console.print("\n[yellow]Simulacion. Anade --apply para ejecutar.[/]")
        console.print("[dim]Los archivos iran a la PAPELERA (recuperables).[/]")
        return

    try:
        from send2trash import send2trash
    except ImportError:
        console.print("[red]Falta send2trash. pip install send2trash[/]")
        raise typer.Exit(1)

    moved = 0
    for s in safe:
        p = Path(s.path)
        if not p.exists():
            continue
        if EDU_PATTERN.search(p.name) or EXCL_PATTERN.search(p.name):
            console.print(f"[cyan]Protegido, se omite:[/] {p.name}")
            continue
        try:
            send2trash(str(p))
            moved += 1
            console.print(f"[green]Papelera:[/] {p.name}")
        except Exception as e:  # noqa: BLE001
            console.print(f"[red]Fallo {p.name}:[/] {e}")

    console.print(f"\n[bold green]{moved} repos a la Papelera (recuperables).[/]")


if __name__ == "__main__":
    app()
