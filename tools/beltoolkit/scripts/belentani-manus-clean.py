#!/usr/bin/env python3
"""
Clean Manus platform plugins from vite configs.
Rewrite to canonical Belentani format.
"""

import re
from pathlib import Path
import os

HOME = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))

CANONICAL_VITE_WITH_CLIENT = '''import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
    },
  },
  root: path.resolve(import.meta.dirname, "client"),
  publicDir: path.resolve(import.meta.dirname, "client", "public"),
  base: "./",
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true,
  },
});
'''

CANONICAL_VITE_SIMPLE = '''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: "./",
  build: {
    outDir: "dist/public",
    emptyOutDir: true,
  },
});
'''


def has_client_dir(repo_path):
    return (repo_path / "client").exists() and (repo_path / "client" / "src").exists()


def clean_repo(name, repo_path):
    vite = repo_path / "vite.config.ts"
    if not vite.exists():
        print(f"  {name}: no vite.config.ts, skip")
        return

    content = vite.read_text(encoding="utf-8")
    has_manus = "manus" in content.lower() or "jsxLocPlugin" in content

    if has_manus:
        if has_client_dir(repo_path):
            vite.write_text(CANONICAL_VITE_WITH_CLIENT, encoding="utf-8")
            print(f"  {name}: vite.config.ts REWRITTEN (canonical with client/)")
        else:
            vite.write_text(CANONICAL_VITE_SIMPLE, encoding="utf-8")
            print(f"  {name}: vite.config.ts REWRITTEN (canonical simple)")
    else:
        # Just needs base/root/outDir fixes
        changes = []
        if 'base:' not in content and 'base :' not in content:
            content = content.replace(
                "export default defineConfig({",
                'export default defineConfig({\n  base: "./",'
            )
            changes.append("added base")

        if changes:
            vite.write_text(content, encoding="utf-8")
            print(f"  {name}: vite.config.ts PATCHED ({', '.join(changes)})")
        else:
            print(f"  {name}: vite.config.ts OK")


TARGETS = {
    "belentani7-profile": HOME / "belentani7-profile",
    "lingua-aberta": HOME / "lingua-aberta",
    "secure-t-check": HOME / "Downloads" / "secure-t-check",
    "belentani-judas-web": HOME / "belentani-judas-web",
}

print("MANUS CLEANUP + VITE CANONICAL FIX")
print("=" * 50)
for name, path in sorted(TARGETS.items()):
    clean_repo(name, path)

print("\nDone.")
