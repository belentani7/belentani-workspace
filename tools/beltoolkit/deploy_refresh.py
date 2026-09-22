"""deploy_refresh.py — Trigger Vercel redeployments via GitHub push.

Since Vercel auto-deploys on push, we create an empty commit and push
to trigger a fresh build. Python stdlib only.

Usage:
  python deploy_refresh.py status              # Check git status all edu
  python deploy_refresh.py trigger <repo>      # Trigger redeploy for one repo
  python deploy_refresh.py trigger-all         # Trigger redeploy for all edu
  python deploy_refresh.py verify              # Verify URLs respond (stdlib)

No VERCEL_TOKEN needed — uses GitHub integration.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import ssl
from pathlib import Path

REPOS_BASE = Path("C:/Users/USER/repos")
GH_USER = "belentani7"

EDU_REPOS = [
    "aprende-brasil",
    "lingua-aberta",
    "linguaforge",
    "WILLIAMSCHOOL",
    "open-school",
    "manus-ai-skill-pack",
    "secure-t-university",
    "ux-academy-professional-program",
]

VERCEL_URLS = {
    "aprende-brasil": "https://aprende-brasil.vercel.app",
    "lingua-aberta": "https://lingua-aberta.vercel.app",
    "linguaforge": "https://linguaforge.vercel.app",
    "WILLIAMSCHOOL": "https://williamschool.vercel.app",
    "open-school": "https://open-school-gamma.vercel.app",
    "manus-ai-skill-pack": "https://manus-ai-skill-pack.vercel.app",
    "secure-t-university": "https://secure-t-university.vercel.app",
    "ux-academy-professional-program": "https://ux-academy-professional.vercel.app",
}


def git(repo_path, *args):
    result = subprocess.run(
        ["git", "-C", str(repo_path)] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=30,
    )
    return result.stdout.strip(), result.returncode


def cmd_status(args):
    print(f"{'Repo':<42} {'Branch':<10} {'Dirty':>5} {'Ahead':>5} {'Hash':<8}")
    print("-" * 80)
    for name in EDU_REPOS:
        repo = REPOS_BASE / name
        if not (repo / ".git").exists():
            print(f"  {name:<40} NOT FOUND")
            continue
        branch, _ = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        dirty_out, _ = git(repo, "status", "--porcelain")
        dirty = len([l for l in dirty_out.splitlines() if l.strip()]) if dirty_out else 0
        hashval, _ = git(repo, "rev-parse", "--short", "HEAD")
        ahead = 0
        ab, rc = git(repo, "rev-list", "--left-right", "--count", f"{branch}...origin/{branch}")
        if rc == 0 and "\t" in ab:
            ahead = int(ab.split("\t")[0])
        mark = "+" if dirty == 0 and ahead == 0 else "!"
        print(f"  {mark} {name:<40} {branch:<10} {dirty:>5} {ahead:>5} {hashval:<8}")
    return 0


def cmd_trigger(args):
    name = args.repo
    if name not in EDU_REPOS:
        print(f"Unknown repo: {name}. Valid: {', '.join(EDU_REPOS)}")
        return 1

    repo = REPOS_BASE / name
    branch, _ = git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    print(f"Triggering redeploy for {name} ({branch})...")
    git(repo, "commit", "--allow-empty", "-m", "chore: trigger Vercel redeploy")
    out, rc = git(repo, "push", "origin", branch)
    if rc == 0:
        print(f"  Pushed. Vercel will auto-deploy.")
    else:
        print(f"  Push failed: {out}")
    return rc


def cmd_trigger_all(args):
    for name in EDU_REPOS:
        repo = REPOS_BASE / name
        if not (repo / ".git").exists():
            print(f"  SKIP {name}: not found")
            continue
        branch, _ = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        print(f"  {name} ({branch})... ", end="", flush=True)
        git(repo, "commit", "--allow-empty", "-m", "chore: trigger Vercel redeploy")
        _, rc = git(repo, "push", "origin", branch)
        print("OK" if rc == 0 else "FAIL")
    return 0


def cmd_verify(args):
    ctx = ssl.create_default_context()
    print(f"{'Repo':<42} {'Status':>6} {'Title'}")
    print("-" * 80)
    for name, url in VERCEL_URLS.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "belentani-deploy-check/1.0"})
            resp = urllib.request.urlopen(req, context=ctx, timeout=15)
            code = resp.status
            html = resp.read(2000).decode("utf-8", errors="replace")
            title = ""
            if "<title>" in html:
                title = html.split("<title>")[1].split("</title>")[0][:50]
            print(f"  {name:<40} {code:>6} {title}")
        except Exception as e:
            print(f"  {name:<40} {'ERR':>6} {e}")
    return 0


def main():
    p = argparse.ArgumentParser(prog="deploy_refresh", description="Vercel redeploy via GitHub push")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Git status of all edu repos")

    t = sub.add_parser("trigger", help="Trigger redeploy for one repo")
    t.add_argument("repo", help="Repo name")

    sub.add_parser("trigger-all", help="Trigger redeploy for all edu repos")
    sub.add_parser("verify", help="Verify Vercel URLs respond")

    args = p.parse_args()
    commands = {
        "status": cmd_status,
        "trigger": cmd_trigger,
        "trigger-all": cmd_trigger_all,
        "verify": cmd_verify,
    }
    sys.exit(commands[args.cmd](args))


if __name__ == "__main__":
    main()
