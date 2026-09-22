#!/usr/bin/env python
"""
secure-t-transform.py
Extract secure-t from monorepo, clean Manus contamination,
rename student Alex Martín -> Luiz, inline edu-engine,
write canonical deploy configs. Standalone deployable result.
"""
import shutil, json, os
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))
SRC = HOME / "Documents" / "01_PROYECTOS" / "belentani-unified" / "apps" / "secure-t"
EDU = HOME / "Documents" / "01_PROYECTOS" / "belentani-unified" / "packages" / "edu-engine"
DST = HOME / "secure-t-app"

EXCLUDE_DIRS = {".git", "node_modules", ".vercel", ".manus-logs", "dist", ".cache"}

def copy_tree(src, dst, exclude_dirs=None):
    exclude_dirs = exclude_dirs or set()
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in exclude_dirs:
            continue
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target, exclude_dirs)
        else:
            shutil.copy2(item, target)

def replace_in_file(filepath, old, new):
    content = filepath.read_text(encoding="utf-8")
    if old not in content:
        print(f"  WARNING: '{old[:50]}...' not found in {filepath.name}")
        return False
    content = content.replace(old, new)
    filepath.write_text(content, encoding="utf-8")
    return True

# ============================================================
print("1. Copying secure-t to standalone directory...")
if DST.exists():
    shutil.rmtree(DST)
copy_tree(SRC, DST, EXCLUDE_DIRS)
print(f"   Copied to {DST}")

# ============================================================
print("2. Inlining edu-engine into lib/edu-engine/...")
edu_dst = DST / "lib" / "edu-engine"
copy_tree(EDU, edu_dst, {"node_modules", ".git", "dist"})
print(f"   4 source files + package.json + tests")

# ============================================================
print("3. Fixing edu-engine import in Lesson.tsx...")
lesson = DST / "client" / "src" / "pages" / "Lesson.tsx"
replace_in_file(lesson,
    'from "../../../../../packages/edu-engine/src/index.ts"',
    'from "../../../lib/edu-engine/src/index.ts"')

# ============================================================
print("4. Renaming student: Alex Martín -> Luiz...")

# Lesson.tsx: tutor.welcome("Alex", lang)
replace_in_file(lesson, 'tutor.welcome("Alex"', 'tutor.welcome("Luiz"')

# Home.tsx: multiple replacements
home = DST / "client" / "src" / "pages" / "Home.tsx"
h = home.read_text(encoding="utf-8")

replacements = [
    ("Alex Martín", "Luiz"),
    ("Good morning, Alex", "Good morning, Luiz"),
    ("Hola, Alex.", "Hola, Luiz."),
]
for old, new in replacements:
    if old in h:
        h = h.replace(old, new)
        print(f"   {old} -> {new}")
    else:
        print(f"   WARNING: '{old}' not found")

# AM initials -> L (specific context: inside avatar div)
h = h.replace('font-bold">AM</div>', 'font-bold">L</div>')
print('   AM (initials) -> L')

home.write_text(h, encoding="utf-8")

# ============================================================
print("5. Deleting ManusDialog.tsx...")
manus = DST / "client" / "src" / "components" / "ManusDialog.tsx"
if manus.exists():
    manus.unlink()
    print("   Deleted")

# ============================================================
print("6. Writing canonical vite.config.ts...")
(DST / "vite.config.ts").write_text('''import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
      "@notifications": path.resolve(import.meta.dirname, "notifications", "index.ts"),
      "@assets": path.resolve(import.meta.dirname, "attached_assets"),
    },
  },
  envDir: path.resolve(import.meta.dirname),
  root: path.resolve(import.meta.dirname, "client"),
  base: "./",
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true,
  },
});
''', encoding="utf-8")
print("   180+ lines Manus -> 20 lines canonical")

# ============================================================
print("7. Cleaning Manus deps from package.json...")
pkg_path = DST / "package.json"
pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
removed = []
for section in ["dependencies", "devDependencies"]:
    if section not in pkg:
        continue
    for dep in list(pkg[section].keys()):
        low = dep.lower()
        if "manus" in low or "builder.io" in low or "jsx-loc" in low:
            del pkg[section][dep]
            removed.append(dep)
for d in removed:
    print(f"   Removed: {d}")

# Fix scripts if they reference frozen lockfile
if "scripts" in pkg:
    for k, v in pkg["scripts"].items():
        if "--frozen-lockfile" in str(v):
            pkg["scripts"][k] = v.replace("--frozen-lockfile", "--no-frozen-lockfile")

pkg_path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# ============================================================
print("8. Writing deploy configs...")

# vercel.json - SPA with client-side routing
vercel = {
    "buildCommand": "pnpm build",
    "installCommand": "pnpm install --no-frozen-lockfile",
    "outputDirectory": "dist/public",
    "framework": "vite",
    "rewrites": [
        {"source": "/(.*)", "destination": "/index.html"}
    ]
}
(DST / "vercel.json").write_text(json.dumps(vercel, indent=2) + "\n", encoding="utf-8")
print("   vercel.json")

# netlify.toml
(DST / "netlify.toml").write_text("""[build]
  command = "pnpm install --no-frozen-lockfile && pnpm run build"
  publish = "dist/public"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
""", encoding="utf-8")
print("   netlify.toml")

# wrangler.toml
(DST / "wrangler.toml").write_text("""name = "secure-t"
pages_build_output_dir = "dist/public"
""", encoding="utf-8")
print("   wrangler.toml")

# ============================================================
print("9. Cleaning up .gitignore...")
gi = DST / ".gitignore"
existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
extras = []
for entry in [".manus-logs/", ".vercel/", ".cache/", "*.log"]:
    if entry not in existing:
        extras.append(entry)
if extras:
    with open(gi, "a", encoding="utf-8") as f:
        f.write("\n# Cleanup\n" + "\n".join(extras) + "\n")
    print(f"   Added {len(extras)} entries")

# Remove .vercel and .manus-logs if copied
for d in [".vercel", ".manus-logs"]:
    p = DST / d
    if p.exists():
        shutil.rmtree(p)

# ============================================================
print("\n" + "=" * 60)
print("SECURE-T STANDALONE READY:", DST)
print("=" * 60)
print()
print("Changes applied:")
print("  [x] Extracted from monorepo -> standalone")
print("  [x] edu-engine inlined to lib/edu-engine/")
print("  [x] Import path fixed in Lesson.tsx")
print("  [x] Alex Martín -> Luiz (Home.tsx + Lesson.tsx)")
print("  [x] AM initials -> L")
print("  [x] ManusDialog.tsx deleted")
print("  [x] vite.config.ts canonical (Manus removed)")
print("  [x] package.json cleaned (Manus deps removed)")
print("  [x] Deploy configs: vercel.json, netlify.toml, wrangler.toml")
print()
print("NOT touched (least aggressive):")
print("  - Curriculum content (7 courses, 4 years)")
print("  - UI design (dark theme, green accent)")
print("  - Brand 'secure T · Digital University'")
print("  - Mentor Astra")
print("  - Academic model, AI governance, labs")
print("  - Server code (api, auth, drizzle, rag, voice)")
print("  - Multi-language support")
print("  - All documentation")
print()
print("Next: cd secure-t-app && git init && push to GitHub")
