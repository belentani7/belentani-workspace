#!/usr/bin/env python3
"""
Belentani Escuelas Audit & Fix
Scans all repos, checks canonical compliance, generates missing configs.
"""

import json
import os
import re
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))

REPOS = {
    "belentani-core": HOME / "belentani-core",
    "belentani-v2": HOME / "belentani-v2",
    "belentani-unified": HOME / "belentani-unified",
    "belentani-judas-web": HOME / "belentani-judas-web",
    "belentani7-profile": HOME / "belentani7-profile",
    "lingua-aberta": HOME / "lingua-aberta",
    "secure-t-university": HOME / "secure-t-university",
    "belentani-campaign-repo": HOME / "belentani-campaign-repo",
    "belentani-forge": HOME / "belentani-forge",
    "belentani-cv-work": HOME / "belentani-cv-work",
    "saas-plasma": HOME / "saas-plasma",
    "AI-Fashion-app": HOME / "AI-Fashion-app",
    "DuckOS": HOME / "DuckOS",
    "BELENTANI_OS": HOME / "Documents" / "BELENTANI_OS",
    "Belentani-Agency-AI-Omega": HOME / "Documents" / "Belentani-Agency-AI-Omega",
    "secure-t-check": HOME / "Downloads" / "secure-t-check",
    "bportal": HOME / "Downloads" / "bportal",
}

MANUS_PLUGINS = [
    "vite-plugin-manus-runtime",
    "@builder.io/vite-plugin-jsx-loc",
    "vitePluginManusRuntime",
    "vitePluginManusDebugCollector",
    "jsxLocPlugin",
    ".manus-logs",
    "manuspre.computer",
    "manus.computer",
    "manus-asia.computer",
    "manuscomputer.ai",
    "manusvm.computer",
]

def detect_project_type(repo_path):
    pkg = repo_path / "package.json"
    if not pkg.exists():
        if (repo_path / "index.html").exists():
            return "static"
        return "no-package"

    data = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

    if "next" in deps:
        return "nextjs"
    if "vite" in deps or any("vite" in d for d in deps):
        return "vite"
    if (repo_path / "vite.config.ts").exists() or (repo_path / "vite.config.js").exists():
        return "vite"
    if (repo_path / "index.html").exists():
        return "static"
    return "unknown"


def check_manus_contamination(repo_path):
    issues = []
    for f in repo_path.rglob("*"):
        if "node_modules" in str(f) or ".next" in str(f) or ".git" in str(f):
            continue
        if not f.is_file():
            continue
        try:
            if f.suffix in (".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml"):
                content = f.read_text(encoding="utf-8", errors="ignore")
                for marker in MANUS_PLUGINS:
                    if marker in content:
                        issues.append(f"  MANUS: {f.relative_to(repo_path)} contains '{marker}'")
        except Exception:
            pass
    return issues


def check_vite_config(repo_path):
    issues = []
    vite_conf = None
    for name in ("vite.config.ts", "vite.config.js", "vite.config.mjs"):
        p = repo_path / name
        if p.exists():
            vite_conf = p
            break

    if not vite_conf:
        return issues, None

    content = vite_conf.read_text(encoding="utf-8", errors="ignore")

    out_dir = None
    if "outDir" in content:
        m = re.search(r'outDir.*?["\']([^"\']+)["\']', content)
        if m:
            out_dir = m.group(1)
        elif "dist/public" in content:
            out_dir = "dist/public"

    if 'base:' not in content and 'base :' not in content:
        issues.append("  VITE: missing `base: './'` (rutas relativas)")
    elif '"./"' not in content and "'./'>" not in content and '"./"`' not in content:
        pass  # may have base but different value

    if "root:" not in content and "root :" not in content:
        issues.append("  VITE: missing explicit `root` (should be 'client' or '.')")

    if not out_dir:
        issues.append("  VITE: missing explicit `outDir` (should be 'dist/public')")

    return issues, out_dir


def check_deploy_configs(repo_path, project_type, out_dir):
    issues = []
    missing = []

    has_vercel = (repo_path / "vercel.json").exists()
    has_netlify = (repo_path / "netlify.toml").exists()
    has_wrangler = (repo_path / "wrangler.toml").exists()
    has_workflows = (repo_path / ".github" / "workflows").exists()

    if not has_vercel:
        missing.append("vercel.json")
    if not has_netlify:
        missing.append("netlify.toml")
    if not has_wrangler:
        missing.append("wrangler.toml")
    if not has_workflows:
        missing.append(".github/workflows/")

    if missing:
        issues.append(f"  DEPLOY: missing {', '.join(missing)}")

    return issues


def generate_vercel_json(project_type, out_dir, repo_name):
    if project_type == "nextjs":
        return json.dumps({
            "buildCommand": "pnpm build",
            "installCommand": "pnpm install --no-frozen-lockfile",
            "framework": "nextjs"
        }, indent=2)
    elif project_type == "vite":
        return json.dumps({
            "buildCommand": "pnpm build",
            "installCommand": "pnpm install --no-frozen-lockfile",
            "outputDirectory": out_dir or "dist/public",
            "framework": "vite"
        }, indent=2)
    elif project_type == "static":
        return json.dumps({
            "outputDirectory": ".",
            "framework": None
        }, indent=2, default=str)
    return None


def generate_netlify_toml(project_type, out_dir):
    if project_type in ("vite", "nextjs"):
        pub = out_dir or "dist/public"
        if project_type == "nextjs":
            pub = ".next"
        return f"""[build]
  command = "pnpm install --no-frozen-lockfile && pnpm run build"
  publish = "{pub}"

[build.environment]
  NODE_VERSION = "24"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    elif project_type == "static":
        return """[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    return None


def generate_wrangler_toml(repo_name, project_type, out_dir):
    pub = out_dir or "dist/public"
    if project_type == "static":
        pub = "."
    return f"""name = "{repo_name}"
pages_build_output_dir = "{pub}"
"""


def audit_repo(name, repo_path):
    result = {"name": name, "path": str(repo_path), "issues": [], "type": "unknown", "status": "OK"}

    if not repo_path.exists():
        result["status"] = "NOT_FOUND"
        return result

    project_type = detect_project_type(repo_path)
    result["type"] = project_type

    # Manus contamination
    manus = check_manus_contamination(repo_path)
    result["issues"].extend(manus)

    # Vite config
    vite_issues, out_dir = check_vite_config(repo_path)
    result["issues"].extend(vite_issues)
    result["out_dir"] = out_dir

    # Deploy configs
    deploy_issues = check_deploy_configs(repo_path, project_type, out_dir)
    result["issues"].extend(deploy_issues)

    # Package.json checks
    pkg = repo_path / "package.json"
    if pkg.exists():
        data = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
        scripts = data.get("scripts", {})
        if "build" not in scripts:
            result["issues"].append("  PKG: missing 'build' script")
        if "dev" not in scripts:
            result["issues"].append("  PKG: missing 'dev' script")

    if result["issues"]:
        result["status"] = "NEEDS_FIX"

    return result


def main():
    print("=" * 70)
    print("BELENTANI ESCUELAS — AUDIT & COMPATIBILITY REPORT")
    print(f"Date: 2026-09-08")
    print("=" * 70)

    results = []
    fix_plan = []

    for name, path in sorted(REPOS.items()):
        r = audit_repo(name, path)
        results.append(r)

        print(f"\n{'[OK]' if r['status'] == 'OK' else '[!!]' if r['status'] == 'NEEDS_FIX' else '[??]'} {name} ({r['type']})")
        if r["status"] == "NOT_FOUND":
            print("  Path not found")
            continue
        for issue in r["issues"]:
            print(issue)

        # Generate fix plan
        if r["status"] == "NEEDS_FIX" and r["type"] in ("vite", "nextjs", "static"):
            out_dir = r.get("out_dir")
            repo_path = Path(r["path"])

            if not (repo_path / "vercel.json").exists():
                content = generate_vercel_json(r["type"], out_dir, name)
                if content:
                    fix_plan.append(("CREATE", repo_path / "vercel.json", content))

            if not (repo_path / "netlify.toml").exists():
                content = generate_netlify_toml(r["type"], out_dir)
                if content:
                    fix_plan.append(("CREATE", repo_path / "netlify.toml", content))

            if not (repo_path / "wrangler.toml").exists():
                content = generate_wrangler_toml(name, r["type"], out_dir)
                if content:
                    fix_plan.append(("CREATE", repo_path / "wrangler.toml", content))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    ok = sum(1 for r in results if r["status"] == "OK")
    fix = sum(1 for r in results if r["status"] == "NEEDS_FIX")
    nf = sum(1 for r in results if r["status"] == "NOT_FOUND")
    manus_count = sum(1 for r in results if any("MANUS" in i for i in r["issues"]))

    print(f"  OK: {ok} | NEEDS_FIX: {fix} | NOT_FOUND: {nf}")
    print(f"  Manus contaminated: {manus_count}")
    print(f"  Fix plan: {len(fix_plan)} files to generate")

    # Write fix plan
    if fix_plan:
        print("\n" + "=" * 70)
        print("FIX PLAN — Files to create:")
        print("=" * 70)
        for action, filepath, content in fix_plan:
            print(f"  {action}: {filepath}")

    # Save report
    report_path = HOME / "Documents" / "belentani-audit-report.json"
    report = {
        "date": "2026-09-08",
        "results": [{**r, "path": str(r["path"])} for r in results],
        "fix_plan": [(a, str(f), c) for a, f, c in fix_plan] if fix_plan else [],
        "summary": {"ok": ok, "needs_fix": fix, "not_found": nf, "manus_contaminated": manus_count}
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport saved: {report_path}")

    # Ask user before applying
    print("\n" + "=" * 70)
    print("APPLY FIXES? Run with --apply to create missing files")
    print("=" * 70)

    import sys
    if "--apply" in sys.argv:
        print("\nApplying fixes...")
        for action, filepath, content in fix_plan:
            filepath = Path(filepath) if not isinstance(filepath, Path) else filepath
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding="utf-8")
            print(f"  Created: {filepath}")
        print(f"\nDone. {len(fix_plan)} files created.")


if __name__ == "__main__":
    main()
