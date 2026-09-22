"""stabilize.py — escanea repos locales, prioriza por dirty count, detecta
remote desactualizado, despliega pendientes en Vercel.

Uso:
  python stabilize.py scan              # escanea y clasifica
  python stabilize.py scan --json       # salida JSON
  python stabilize.py sync              # commit+push los dirty propios (dry-run)
  python stabilize.py sync --apply      # commit+push real
  python stabilize.py deploy            # redeploy Vercel pendientes (dry-run)
  python stabilize.py deploy --apply    # redeploy real

Solo stdlib. httpx opcional para Vercel API.
Tokens solo por env: GH_TOKEN, VERCEL_TOKEN.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

GH_USER = "belentani7"
VERCEL_TEAM = "team_PW8qfFcgLWackpqpCQfifest"

KNOWN_FORKS = {
    "canva-clone", "canva-clone-lidojs", "figma_clone", "IOPaint", "jqgo",
    "kt-paperclip", "ollama", "omarchy", "onlook", "paperclip", "paperclip-app",
    "SongGeneration", "SongGeneration-Studio", "willian-games",
    "Retrieval-based-Voice-Conversion-WebUI", "Meta-voicebox", "hypeframeVideo",
    "react-video-editor", "openreel-video", "natively-cluely-ai-assistant",
    "mattpocock-skills", "thing-cli", "dsh-eval", "deepseek-harness",
}

SEARCH_ROOTS = [
    Path("C:/Users/USER/Desktop"),
    Path("C:/Users/USER/Documents"),
    Path("C:/Users/USER/Videos"),
    Path("C:/Users/USER/repos"),
]


def git(repo_path, *args):
    result = subprocess.run(
        ["git", "-C", str(repo_path)] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=30,
    )
    return result.stdout.strip(), result.returncode


def find_repos(max_depth=3):
    repos = []
    seen = set()
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for current, dirs, _files in os.walk(root):
            depth = len(Path(current).relative_to(root).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            skip = {"node_modules", ".git", "__pycache__", ".next", "dist", ".cache"}
            dirs[:] = [d for d in dirs if d not in skip]
            cp = Path(current)
            if (cp / ".git").exists() and str(cp) not in seen:
                seen.add(str(cp))
                repos.append(cp)
                dirs.clear()
    return repos


def scan_repo(repo_path):
    name = repo_path.name

    branch, _ = git(repo_path, "rev-parse", "--abbrev-ref", "HEAD")
    dirty_out, _ = git(repo_path, "status", "--porcelain")
    dirty_count = len([l for l in dirty_out.splitlines() if l.strip()]) if dirty_out else 0

    remote_url, rc = git(repo_path, "remote", "get-url", "origin")
    has_remote = rc == 0 and bool(remote_url)

    ahead = 0
    behind = 0
    if has_remote and branch:
        ab_out, rc = git(repo_path, "rev-list", "--left-right", "--count",
                         f"{branch}...origin/{branch}")
        if rc == 0 and "\t" in ab_out:
            parts = ab_out.split("\t")
            ahead = int(parts[0])
            behind = int(parts[1])

    is_fork = name in KNOWN_FORKS
    is_own = (not is_fork) and (
        GH_USER in remote_url if has_remote else True
    )

    last_commit_date, _ = git(repo_path, "log", "-1", "--format=%ci")

    return {
        "name": name,
        "path": str(repo_path),
        "branch": branch,
        "dirty": dirty_count,
        "ahead": ahead,
        "behind": behind,
        "has_remote": has_remote,
        "remote_url": remote_url if has_remote else "",
        "is_fork": is_fork,
        "is_own": is_own,
        "last_commit": last_commit_date,
    }


def classify_priority(repo):
    if repo["is_fork"]:
        return "SKIP_FORK"
    if repo["dirty"] == 0 and repo["ahead"] == 0:
        return "CLEAN"
    if repo["dirty"] > 50:
        return "P1_HEAVY"
    if repo["dirty"] > 0:
        return "P2_DIRTY"
    if repo["ahead"] > 0:
        return "P3_AHEAD"
    return "CLEAN"


EDUCATIONAL = {
    "secure-t-university", "aprende-brasil", "open-school", "lingua-aberta",
    "ux-academy-professional-program", "manus-ai-skill-pack", "linguaforge",
    "openlinguaforge", "williamschool", "WILLIAMSCHOOL",
}


def cmd_scan(args):
    repos = find_repos()
    print(f"Encontrados {len(repos)} repos locales.\n")

    scanned = []
    for rp in repos:
        try:
            info = scan_repo(rp)
            info["priority"] = classify_priority(info)
            info["is_edu"] = info["name"] in EDUCATIONAL or info["name"].lower() in {e.lower() for e in EDUCATIONAL}
            scanned.append(info)
        except Exception as exc:
            print(f"  ERROR {rp.name}: {exc}")

    scanned.sort(key=lambda r: (-r["dirty"], -r["ahead"], r["name"]))

    if args.json_out:
        own = [r for r in scanned if not r["is_fork"]]
        print(json.dumps(own, indent=2, ensure_ascii=False))
        return 0

    print(f"{'Repo':<42} {'Dirty':>5} {'Ahead':>5} {'Branch':<12} {'Prio':<12} {'Edu'}")
    print("-" * 95)

    for r in scanned:
        if r["is_fork"]:
            continue
        edu_tag = "EDU" if r["is_edu"] else ""
        print(f"{r['name']:<42} {r['dirty']:>5} {r['ahead']:>5} {r['branch']:<12} {r['priority']:<12} {edu_tag}")

    own = [r for r in scanned if not r["is_fork"]]
    dirty = [r for r in own if r["dirty"] > 0]
    ahead = [r for r in own if r["ahead"] > 0]
    edu = [r for r in own if r["is_edu"]]

    print(f"\n--- Resumen ---")
    print(f"Total propios: {len(own)} (forks ignorados: {len(scanned) - len(own)})")
    print(f"Con cambios locales (dirty): {len(dirty)}")
    print(f"Ahead de remote: {len(ahead)}")
    print(f"Educacionales: {len(edu)}")

    if dirty:
        print(f"\nTop 10 por dirty count (= importancia):")
        for r in dirty[:10]:
            edu_mark = " [EDU]" if r["is_edu"] else ""
            remote_mark = " NO_REMOTE" if not r["has_remote"] else ""
            print(f"  {r['name']:<40} dirty={r['dirty']:<4}{edu_mark}{remote_mark}")

    return 0


def cmd_sync(args):
    repos = find_repos()
    scanned = []
    for rp in repos:
        try:
            info = scan_repo(rp)
            info["priority"] = classify_priority(info)
            if not info["is_fork"] and info["is_own"] and info["dirty"] > 0 and info["has_remote"]:
                scanned.append(info)
        except Exception:
            pass

    scanned.sort(key=lambda r: -r["dirty"])

    if not scanned:
        print("No hay repos propios con cambios pendientes y remote.")
        return 0

    print(f"Repos propios con dirty + remote: {len(scanned)}\n")

    for r in scanned:
        print(f"\n{'='*60}")
        print(f"{r['name']} — dirty={r['dirty']}, branch={r['branch']}")
        print(f"  remote: {r['remote_url']}")

        if not args.apply:
            print("  DRY-RUN: haría git add -A, commit 'chore: sync local changes', push")
            continue

        print("  Fetching...")
        git(Path(r["path"]), "fetch", "origin")

        _, rc = git(Path(r["path"]), "rev-parse", f"origin/{r['branch']}")
        if rc != 0:
            print("  SKIP: remote branch no existe, push manual necesario")
            continue

        print("  Staging...")
        git(Path(r["path"]), "add", "-A")
        print("  Committing...")
        msg = f"chore: sync {r['dirty']} local changes"
        _, rc = git(Path(r["path"]), "commit", "-m", msg)
        if rc != 0:
            print("  SKIP: commit falló (sin cambios staged o conflicto)")
            continue

        print("  Pushing...")
        _, rc = git(Path(r["path"]), "push", "origin", r["branch"])
        if rc == 0:
            print("  OK: pushed")
        else:
            print("  FAIL: push rechazado (archivado o permisos)")

    return 0


def cmd_deploy(args):
    try:
        import httpx
    except ImportError:
        print("httpx no instalado. pip install httpx")
        return 2

    token = os.environ.get("VERCEL_TOKEN", "")
    if not token:
        print("VERCEL_TOKEN no definido en env.")
        return 2

    headers = {"Authorization": f"Bearer {token}"}
    vc_api = "https://api.vercel.com"

    pending = ["keyrotor", "ux-academy-professional", "duckhtml"]

    projects = httpx.get(
        f"{vc_api}/v9/projects?teamId={VERCEL_TEAM}&limit=100",
        headers=headers, timeout=60,
    ).json()
    pmap = {p["name"]: p for p in projects.get("projects", [])}

    for name in pending:
        p = pmap.get(name)
        if not p:
            print(f"{name}: NO encontrado en Vercel")
            continue

        deps = httpx.get(
            f"{vc_api}/v6/deployments?projectId={p['id']}&teamId={VERCEL_TEAM}&limit=1",
            headers=headers, timeout=60,
        ).json().get("deployments", [])

        state = deps[0].get("readyState", "NONE") if deps else "NONE"
        print(f"{name}: ultimo deploy = {state}")

        if state == "READY":
            print(f"  Ya READY, skip.")
            continue

        if not args.apply:
            print(f"  DRY-RUN: haría redeploy")
            continue

        repo_link = p.get("link", {})
        repo_name = repo_link.get("repo")
        if not repo_name:
            print(f"  SKIP: sin repo vinculado")
            continue

        gh_token = os.environ.get("GH_TOKEN", "")
        gh_headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}
        ref_resp = httpx.get(
            f"https://api.github.com/repos/{GH_USER}/{repo_name}/git/ref/heads/main",
            headers=gh_headers, timeout=30,
        )
        if ref_resp.status_code != 200:
            print(f"  SKIP: no pude leer SHA de main ({ref_resp.status_code})")
            continue

        sha = ref_resp.json()["object"]["sha"]
        payload = {
            "name": name,
            "target": "production",
            "gitSource": {
                "type": "github",
                "repo": f"{GH_USER}/{repo_name}",
                "ref": "main",
                "sha": sha,
            },
            "teamId": VERCEL_TEAM,
        }
        deploy_resp = httpx.post(
            f"{vc_api}/v13/deployments?teamId={VERCEL_TEAM}",
            headers=headers, json=payload, timeout=60,
        )
        if deploy_resp.status_code in (200, 201):
            uid = deploy_resp.json().get("id", "?")
            print(f"  DEPLOYED: {uid}")
        else:
            err = deploy_resp.text[:200]
            print(f"  FAIL ({deploy_resp.status_code}): {err}")

    return 0


def main():
    p = argparse.ArgumentParser(prog="stabilize", description="Estabilización repos belentani7")
    sub = p.add_subparsers(dest="cmd", required=True)

    sc = sub.add_parser("scan", help="Escanea repos locales, prioriza por dirty count")
    sc.add_argument("--json", dest="json_out", action="store_true", help="Salida JSON")
    sc.set_defaults(fn=cmd_scan)

    sy = sub.add_parser("sync", help="Commit+push repos propios dirty")
    sy.add_argument("--apply", action="store_true", help="Ejecutar (sin esto: dry-run)")
    sy.set_defaults(fn=cmd_sync)

    dp = sub.add_parser("deploy", help="Redeploy pendientes en Vercel")
    dp.add_argument("--apply", action="store_true", help="Ejecutar (sin esto: dry-run)")
    dp.set_defaults(fn=cmd_deploy)

    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
