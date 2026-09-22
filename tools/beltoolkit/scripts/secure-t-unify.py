#!/usr/bin/env python
"""
secure-t-unify.py
Merge best unique content from all secure-t copies into secure-t-app.
Does NOT overwrite existing files - only adds missing pieces.
"""
import shutil, json, os
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))
DST = HOME / "secure-t-app"
CHECK = HOME / "Downloads" / "secure-t-check"
STATIC = HOME / "secure-t-university"

copied = []
skipped = []

def safe_copy(src, dst, label=""):
    """Copy file only if destination doesn't exist."""
    dst = Path(dst)
    src = Path(src)
    if not src.exists():
        skipped.append(f"NOT FOUND: {src}")
        return False
    if dst.exists():
        skipped.append(f"EXISTS: {dst.name}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(label or dst.name)
    return True

def safe_copy_dir(src, dst, label=""):
    """Copy directory only if destination doesn't exist."""
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        skipped.append(f"DIR NOT FOUND: {src}")
        return False
    if dst.exists():
        skipped.append(f"DIR EXISTS: {dst.name}")
        return False
    shutil.copytree(src, dst)
    count = sum(1 for _ in dst.rglob("*") if _.is_file())
    copied.append(f"{label or dst.name}/ ({count} files)")
    return True

# ============================================================
print("UNIFYING BEST OF ALL SECURE-T COPIES")
print("=" * 60)

# --- From Downloads/secure-t-check ---
print("\n[Downloads/secure-t-check]")

# 1. Dockerfile
safe_copy(CHECK / "Dockerfile", DST / "Dockerfile", "Dockerfile")

# 2. DEPLOY.md
safe_copy(CHECK / "DEPLOY.md", DST / "DEPLOY.md", "DEPLOY.md")

# 3. railway.json
safe_copy(CHECK / "railway.json", DST / "railway.json", "railway.json")

# 4. NOTICE-ATRIBUCIONES.md (legal attributions)
safe_copy(CHECK / "NOTICE-ATRIBUCIONES.md", DST / "NOTICE-ATRIBUCIONES.md", "NOTICE-ATRIBUCIONES.md")

# 5. components.json (shadcn config)
safe_copy(CHECK / "components.json", DST / "components.json", "components.json")

# 6. sql/seed.sql (database seed - critical)
safe_copy(CHECK / "sql" / "seed.sql", DST / "sql" / "seed.sql", "sql/seed.sql")

# 7. education/ directory (knowledge core, video catalog)
safe_copy_dir(CHECK / "education", DST / "education", "education")

# 8. patches/ (wouter patch)
safe_copy_dir(CHECK / "patches", DST / "patches", "patches")

# --- From secure-t-university (static) ---
print("\n[secure-t-university]")

# 9. Course content markdown (real labs and exercises)
courses_dst = DST / "education" / "courses"
courses_dst.mkdir(parents=True, exist_ok=True)
for md in (STATIC / "courses").glob("*.md"):
    safe_copy(md, courses_dst / md.name, f"courses/{md.name}")

# 10. Public files (security.txt, robots.txt, sitemap.xml)
# These go into client/public/ for the Vite build
pub_dst = DST / "client" / "public"
for fname in ["robots.txt", "sitemap.xml"]:
    src = STATIC / "public" / fname
    safe_copy(src, pub_dst / fname, f"public/{fname}")

# security.txt -> .well-known/security.txt (RFC 9116 standard)
wellknown = pub_dst / ".well-known"
wellknown.mkdir(parents=True, exist_ok=True)
sec_src = STATIC / "public" / "security.txt"
if sec_src.exists() and not (wellknown / "security.txt").exists():
    content = sec_src.read_text(encoding="utf-8")
    # Update placeholder URLs to match our project
    content = content.replace("secure-t-university.example.com", "secure-t-app.vercel.app")
    (wellknown / "security.txt").write_text(content, encoding="utf-8")
    copied.append("public/.well-known/security.txt (updated URLs)")

# --- Fix DEPLOY.md to reference new repo name ---
print("\n[Fixes]")
deploy_path = DST / "DEPLOY.md"
if deploy_path.exists():
    content = deploy_path.read_text(encoding="utf-8")
    if "belentani7/secure-t" in content and "belentani7/secure-t-app" not in content:
        content = content.replace("belentani7/secure-t`", "belentani7/secure-t-app`")
        content = content.replace("belentani7/secure-t\"", "belentani7/secure-t-app\"")
        deploy_path.write_text(content, encoding="utf-8")
        print("  DEPLOY.md: repo reference updated to secure-t-app")

# --- Fix Dockerfile to use --no-frozen-lockfile ---
docker_path = DST / "Dockerfile"
if docker_path.exists():
    content = docker_path.read_text(encoding="utf-8")
    if "--frozen-lockfile" in content:
        content = content.replace("--frozen-lockfile", "--no-frozen-lockfile")
        docker_path.write_text(content, encoding="utf-8")
        print("  Dockerfile: --frozen-lockfile -> --no-frozen-lockfile")

# ============================================================
print("\n" + "=" * 60)
print("UNIFICATION COMPLETE")
print("=" * 60)
print(f"\nCopied ({len(copied)}):")
for c in copied:
    print(f"  + {c}")
if skipped:
    print(f"\nSkipped ({len(skipped)}):")
    for s in skipped:
        print(f"  - {s}")
print(f"\nTotal new files added to secure-t-app")
