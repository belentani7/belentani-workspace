#!/usr/bin/env python3
"""
Push all repos with pending changes to GitHub.
Create repos where missing.
"""

import subprocess
import sys
import os
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))

def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def git_status(repo):
    code, out, _ = run("git status --porcelain", cwd=repo)
    return out.splitlines() if code == 0 else []

def git_push_configs(name, repo, msg="feat: add multi-platform deploy configs (vercel/netlify/cloudflare)"):
    print(f"\n{'='*60}")
    print(f"PUSHING: {name}")
    print(f"{'='*60}")

    dirty = git_status(repo)
    if not dirty:
        print(f"  Clean, nothing to push")
        return True

    print(f"  {len(dirty)} dirty files:")
    for f in dirty[:10]:
        print(f"    {f}")

    # Stage deploy configs and vite changes
    targets = []
    for line in dirty:
        fname = line[3:].strip().strip('"')
        if any(fname.endswith(ext) for ext in [
            "vercel.json", "netlify.toml", "wrangler.toml",
            "vite.config.ts", "vite.config.js"
        ]):
            targets.append(fname)

    if not targets:
        print(f"  No deploy config changes found, skip")
        return False

    for t in targets:
        code, _, err = run(f'git add "{t}"', cwd=repo)
        if code != 0:
            print(f"  ERROR adding {t}: {err}")
            return False
        print(f"  Staged: {t}")

    code, _, err = run(f'git commit -m "{msg}"', cwd=repo)
    if code != 0:
        print(f"  Commit failed: {err}")
        return False
    print(f"  Committed")

    code, out, err = run("git push", cwd=repo)
    if code != 0:
        print(f"  Push failed: {err}")
        # Try setting upstream
        branch_code, branch, _ = run("git branch --show-current", cwd=repo)
        branch = branch or "main"
        code2, _, err2 = run(f"git push -u origin {branch}", cwd=repo)
        if code2 != 0:
            print(f"  Push with upstream failed: {err2}")
            return False
        print(f"  Pushed with upstream set")
    else:
        print(f"  Pushed OK")
    return True


def ensure_repo_exists(name, visibility="public"):
    """Check if repo exists on GitHub, create if not."""
    code, _, _ = run(f"gh repo view belentani7/{name} --json name")
    if code == 0:
        return True  # exists

    print(f"  Creating repo belentani7/{name} ({visibility})...")
    code, out, err = run(f"gh repo create belentani7/{name} --{visibility} --confirm")
    if code != 0:
        # Try alternative syntax
        code, out, err = run(f"gh repo create {name} --{visibility}")
        if code != 0:
            print(f"  Create failed: {err}")
            return False
    print(f"  Created: belentani7/{name}")
    return True


def init_and_push(name, local_path, visibility="public"):
    """Init git, create repo, push."""
    print(f"\n{'='*60}")
    print(f"NEW REPO: {name} from {local_path}")
    print(f"{'='*60}")

    if not Path(local_path).exists():
        print(f"  Path not found!")
        return False

    has_git = (Path(local_path) / ".git").exists()

    if not has_git:
        run("git init", cwd=local_path)
        run("git branch -M main", cwd=local_path)

    # Check if remote exists
    code, remote, _ = run("git remote get-url origin", cwd=local_path)
    if code != 0:
        # Need to create repo and add remote
        if not ensure_repo_exists(name, visibility):
            return False
        run(f"git remote add origin https://github.com/belentani7/{name}.git", cwd=local_path)

    # Add gitignore if missing
    gitignore = Path(local_path) / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("node_modules/\ndist/\n.next/\n.env\n.env.local\n*.log\n.DS_Store\n", encoding="utf-8")

    # Stage all
    run("git add -A", cwd=local_path)

    status = git_status(local_path)
    if not status:
        # Check if there are commits
        code, _, _ = run("git rev-parse HEAD", cwd=local_path)
        if code != 0:
            print("  No files to commit and no history")
            return False
        print("  Already committed and clean")
    else:
        code, _, err = run('git commit -m "feat: initial deploy with multi-platform configs"', cwd=local_path)
        if code != 0:
            print(f"  Commit failed: {err}")
            return False

    code, _, err = run("git push -u origin main", cwd=local_path)
    if code != 0:
        # Force push if remote has different history
        code2, _, err2 = run("git push -u origin main --force-with-lease", cwd=local_path)
        if code2 != 0:
            print(f"  Push failed: {err2}")
            return False
        print(f"  Pushed (force-with-lease)")
    else:
        print(f"  Pushed OK")
    return True


# ============================================================
# PHASE 1: Push configs on existing repos
# ============================================================
print("\n" + "=" * 60)
print("PHASE 1: Push deploy configs to existing repos")
print("=" * 60)

EXISTING = {
    "belentani-core": HOME / "belentani-core",
    "belentani-v2": HOME / "belentani-v2",
    "belentani-judas-web": HOME / "belentani-judas-web",
    "lingua-aberta": HOME / "lingua-aberta",
    "secure-t-university": HOME / "secure-t-university",
    "belentani7-profile": HOME / "belentani7-profile",
    "saas-plasma": HOME / "saas-plasma",
}

results_phase1 = {}
for name, path in sorted(EXISTING.items()):
    ok = git_push_configs(name, str(path))
    results_phase1[name] = ok

# ============================================================
# PHASE 2: Push standalone projects from Documents
# ============================================================
print("\n" + "=" * 60)
print("PHASE 2: Standalone projects from Documents")
print("=" * 60)

STANDALONE = {
    "pvc-u-frontend": HOME / "Documents" / "01_PROYECTOS" / "pvc-u-frontend",
    "la-alquitara": HOME / "Documents" / "01_PROYECTOS" / "la-alquitara",
    "nebula-cosmos": HOME / "Documents" / "01_PROYECTOS" / "nebula-cosmos",
}

results_phase2 = {}
for name, path in sorted(STANDALONE.items()):
    ok = init_and_push(name, str(path))
    results_phase2[name] = ok

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
for phase_name, results in [("Phase 1 (configs)", results_phase1), ("Phase 2 (standalone)", results_phase2)]:
    print(f"\n{phase_name}:")
    for name, ok in sorted(results.items()):
        print(f"  {'OK' if ok else 'FAIL'}: {name}")

total_ok = sum(1 for r in {**results_phase1, **results_phase2}.values() if r)
total = len(results_phase1) + len(results_phase2)
print(f"\nTotal: {total_ok}/{total} successful")
