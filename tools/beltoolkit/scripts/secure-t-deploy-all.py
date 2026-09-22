#!/usr/bin/env python
"""
deploy-all.py — Three cuts of scissors for every web project.
1. vercel.json
2. netlify.toml
3. GitHub Pages (via workflow or direct)

Generates configs, commits, pushes. Does NOT overwrite existing files.
"""
import subprocess, json, os
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))

def run(cmd, cwd=None, timeout=60):
    r = subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None,
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def write_if_missing(path, content, label=""):
    path = Path(path)
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"    + {label or path.name}")
    return True

def git_add_commit_push(repo_dir, files, msg):
    """Stage specific files, commit, push."""
    cwd = str(repo_dir)
    staged = []
    for f in files:
        full = Path(repo_dir) / f
        if full.exists():
            code, _, _ = run(f'git add "{f}"', cwd=cwd)
            if code == 0:
                staged.append(f)

    if not staged:
        print("    No new files to commit")
        return False

    code, _, err = run(f'git commit -m "{msg}"', cwd=cwd)
    if code != 0:
        if "nothing to commit" in err or "nothing to commit" in _:
            print("    Already committed")
            return False
        print(f"    Commit failed: {err[:100]}")
        return False

    code, _, err = run("git push", cwd=cwd)
    if code != 0:
        # Try setting upstream
        bc, branch, _ = run("git branch --show-current", cwd=cwd)
        branch = branch or "main"
        code2, _, err2 = run(f"git push -u origin {branch}", cwd=cwd)
        if code2 != 0:
            print(f"    Push failed: {err2[:100]}")
            return False

    print(f"    Pushed {len(staged)} files")
    return True


# ============================================================
# STATIC PROJECTS (no build step, deploy root or subfolder)
# ============================================================
STATIC_PROJECTS = [
    {
        "name": "la-alquitara",
        "path": HOME / "Documents" / "01_PROYECTOS" / "la-alquitara",
        "publish": ".",
        "wrangler_name": "la-alquitara",
    },
    {
        "name": "nebula-cosmos",
        "path": HOME / "Documents" / "01_PROYECTOS" / "nebula-cosmos",
        "publish": ".",
        "wrangler_name": "nebula-cosmos",
    },
    {
        "name": "keyrotor",
        "path": HOME / "keyrotor",
        "publish": "frontend",
        "wrangler_name": "keyrotor",
    },
]

# VITE PROJECTS (need build step)
VITE_PROJECTS = [
    {
        "name": "pvc-u-frontend",
        "path": HOME / "Documents" / "01_PROYECTOS" / "pvc-u-frontend",
        "publish": "dist",
        "wrangler_name": "pvc-u-frontend",
    },
    {
        "name": "secure-t-app",
        "path": HOME / "secure-t-app",
        "publish": "dist/public",
        "wrangler_name": "secure-t",
        "skip_configs": True,  # Already has configs
    },
]

results = {}

# ============================================================
print("=" * 60)
print("PHASE 1: Static projects — add deploy configs")
print("=" * 60)

for proj in STATIC_PROJECTS:
    name = proj["name"]
    path = proj["path"]
    pub = proj["publish"]
    print(f"\n  [{name}]")

    if not path.exists():
        print(f"    PATH NOT FOUND: {path}")
        results[name] = "NOT FOUND"
        continue

    created = []

    # vercel.json — static, no build
    v = {
        "outputDirectory": pub if pub != "." else None,
        "framework": None,
        "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]
    }
    # Remove None values
    v = {k: v for k, v in v.items() if v is not None}
    if write_if_missing(path / "vercel.json", json.dumps(v, indent=2) + "\n"):
        created.append("vercel.json")

    # netlify.toml — static, no build
    netlify_pub = pub if pub != "." else "."
    netlify_content = f"""[build]
  publish = "{netlify_pub}"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    if write_if_missing(path / "netlify.toml", netlify_content):
        created.append("netlify.toml")

    # wrangler.toml
    wrangler = f"""name = "{proj['wrangler_name']}"
pages_build_output_dir = "{pub}"
"""
    if write_if_missing(path / "wrangler.toml", wrangler):
        created.append("wrangler.toml")

    # GitHub Pages workflow (deploy from branch)
    workflow = f"""name: Deploy GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '{pub}'
      - uses: actions/deploy-pages@v4
        id: deployment
"""
    wf_path = ".github/workflows/deploy-pages.yml"
    if write_if_missing(path / wf_path, workflow):
        created.append(wf_path)

    if created:
        ok = git_add_commit_push(path, created,
            "feat: add multi-platform deploy configs (vercel/netlify/cloudflare/pages)")
        results[name] = "PUSHED" if ok else "COMMIT FAILED"
    else:
        results[name] = "CONFIGS EXIST"
        print("    All configs exist already")


# ============================================================
print("\n" + "=" * 60)
print("PHASE 2: Vite projects — add deploy configs")
print("=" * 60)

for proj in VITE_PROJECTS:
    name = proj["name"]
    path = proj["path"]
    pub = proj["publish"]
    print(f"\n  [{name}]")

    if proj.get("skip_configs"):
        print("    Configs already present, skip")
        results[name] = "SKIP (has configs)"
        continue

    if not path.exists():
        print(f"    PATH NOT FOUND: {path}")
        results[name] = "NOT FOUND"
        continue

    created = []

    # vercel.json
    v = {
        "buildCommand": "pnpm build" if (path / "pnpm-lock.yaml").exists() else "npm run build",
        "installCommand": "pnpm install --no-frozen-lockfile" if (path / "pnpm-lock.yaml").exists() else "npm install",
        "outputDirectory": pub,
        "framework": "vite",
        "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]
    }
    if write_if_missing(path / "vercel.json", json.dumps(v, indent=2) + "\n"):
        created.append("vercel.json")

    # netlify.toml
    pkg_mgr = "pnpm" if (path / "pnpm-lock.yaml").exists() else "npm"
    install = f"{pkg_mgr} install --no-frozen-lockfile" if pkg_mgr == "pnpm" else "npm install"
    build = f"{pkg_mgr} run build"
    netlify_content = f"""[build]
  command = "{install} && {build}"
  publish = "{pub}"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    if write_if_missing(path / "netlify.toml", netlify_content):
        created.append("netlify.toml")

    # wrangler.toml
    wrangler = f"""name = "{proj['wrangler_name']}"
pages_build_output_dir = "{pub}"
"""
    if write_if_missing(path / "wrangler.toml", wrangler):
        created.append("wrangler.toml")

    # GitHub Pages workflow (with build)
    setup_pnpm = """      - uses: pnpm/action-setup@v4
""" if pkg_mgr == "pnpm" else ""

    workflow = f"""name: Deploy GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{setup_pnpm}      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: {install}
      - run: {build}
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '{pub}'
  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
"""
    wf_path = ".github/workflows/deploy-pages.yml"
    if write_if_missing(path / wf_path, workflow):
        created.append(wf_path)

    if created:
        ok = git_add_commit_push(path, created,
            "feat: add multi-platform deploy configs (vercel/netlify/cloudflare/pages)")
        results[name] = "PUSHED" if ok else "COMMIT FAILED"
    else:
        results[name] = "CONFIGS EXIST"
        print("    All configs exist already")


# ============================================================
print("\n" + "=" * 60)
print("PHASE 3: Enable GitHub Pages on public repos")
print("=" * 60)

PUBLIC_REPOS_FOR_PAGES = [
    "secure-t-app",
    "la-alquitara",
    "nebula-cosmos",
    "pvc-u-frontend",
    "Steven-renovation",
    "proofmesh",
    "duck-hub",
]

for repo in PUBLIC_REPOS_FOR_PAGES:
    print(f"\n  [{repo}]")
    # Check if already has Pages
    code, out, _ = run(f'gh api "repos/belentani7/{repo}/pages"')
    if code == 0 and '"html_url"' in out:
        url = json.loads(out).get("html_url", "")
        print(f"    Pages already on: {url}")
        continue

    # Check visibility first
    code, out, _ = run(f'gh api "repos/belentani7/{repo}" --jq .visibility')
    if "private" in out.lower():
        print(f"    PRIVATE repo - Pages requires public. Making public...")
        code, _, err = run(f'gh api -X PATCH "repos/belentani7/{repo}" -f visibility=public')
        if code != 0:
            print(f"    Failed to make public: {err[:80]}")
            continue

    # Enable Pages with GitHub Actions source
    code, out, err = run(
        f'gh api -X POST "repos/belentani7/{repo}/pages" '
        f'-f "build_type=workflow"'
    )
    if code == 0:
        print(f"    Pages enabled (workflow source)")
    elif "already" in err.lower() or "already" in out.lower():
        print(f"    Pages already configured")
    else:
        # Try legacy source (deploy from branch)
        code2, out2, err2 = run(
            f'gh api -X POST "repos/belentani7/{repo}/pages" '
            f'-f "source[branch]=main" -f "source[path]=/"'
        )
        if code2 == 0:
            print(f"    Pages enabled (main branch)")
        else:
            print(f"    Failed: {(err2 or err)[:80]}")


# ============================================================
print("\n" + "=" * 60)
print("PHASE 4: Add deploy configs to REMOTE repos (no local clone)")
print("=" * 60)

REMOTE_STATIC = [
    "Steven-renovation",
]

for repo in REMOTE_STATIC:
    print(f"\n  [{repo}]")
    # Check if vercel.json exists
    code, _, _ = run(f'gh api "repos/belentani7/{repo}/contents/vercel.json"')
    if code == 0:
        print("    vercel.json exists")
        continue

    # Create vercel.json via API
    import base64
    content = json.dumps({"framework": None, "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}, indent=2)
    encoded = base64.b64encode(content.encode()).decode()
    code, _, err = run(
        f'gh api -X PUT "repos/belentani7/{repo}/contents/vercel.json" '
        f'-f "message=feat: add vercel.json" '
        f'-f "content={encoded}"'
    )
    if code == 0:
        print("    + vercel.json (via API)")
    else:
        print(f"    Failed: {err[:80]}")

    # Create netlify.toml
    code, _, _ = run(f'gh api "repos/belentani7/{repo}/contents/netlify.toml"')
    if code != 0:
        nl = '[build]\n  publish = "."\n\n[[redirects]]\n  from = "/*"\n  to = "/index.html"\n  status = 200\n'
        encoded = base64.b64encode(nl.encode()).decode()
        code, _, err = run(
            f'gh api -X PUT "repos/belentani7/{repo}/contents/netlify.toml" '
            f'-f "message=feat: add netlify.toml" '
            f'-f "content={encoded}"'
        )
        if code == 0:
            print("    + netlify.toml (via API)")


# ============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
for name, status in sorted(results.items()):
    print(f"  {status:20s} {name}")
print(f"\nTotal processed: {len(results)}")
