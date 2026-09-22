#!/usr/bin/env python3
"""Generate missing deploy configs for all Belentani repos."""

import json
from pathlib import Path

HOME = Path.home()

configs = {
    'belentani-core': {'type': 'nextjs', 'out_dir': '.next', 'needs': ['workflows']},
    'belentani-judas-web': {'type': 'vite', 'out_dir': 'dist/public', 'needs': ['vercel', 'netlify', 'wrangler', 'workflows']},
    'belentani7-profile': {'type': 'vite', 'out_dir': 'dist/public', 'needs': ['vercel', 'netlify', 'wrangler', 'workflows']},
    'lingua-aberta': {'type': 'vite', 'out_dir': 'dist/public', 'needs': ['vercel', 'netlify', 'wrangler', 'workflows']},
    'saas-plasma': {'type': 'nextjs', 'out_dir': '.next', 'needs': ['workflows']},
    'belentani-v2': {'type': 'static', 'out_dir': '.', 'needs': ['workflows']},
    'secure-t-university': {'type': 'static', 'out_dir': '.', 'needs': ['workflows']},
}

for name, cfg in configs.items():
    path = HOME / name
    if not path.exists():
        print(f'{name}: NOT FOUND')
        continue

    # vercel.json
    if 'vercel' in cfg['needs']:
        if cfg['type'] == 'nextjs':
            content = json.dumps({
                'buildCommand': 'pnpm build',
                'installCommand': 'pnpm install --no-frozen-lockfile',
                'framework': 'nextjs'
            }, indent=2)
        elif cfg['type'] == 'vite':
            content = json.dumps({
                'buildCommand': 'pnpm build',
                'installCommand': 'pnpm install --no-frozen-lockfile',
                'outputDirectory': cfg['out_dir'],
                'framework': 'vite'
            }, indent=2)
        elif cfg['type'] == 'static':
            content = json.dumps({
                'outputDirectory': '.',
                'framework': None
            }, indent=2, default=str)
        (path / 'vercel.json').write_text(content)
        print(f'Created: {name}/vercel.json')

    # netlify.toml
    if 'netlify' in cfg['needs']:
        if cfg['type'] in ('vite', 'nextjs'):
            pub = cfg['out_dir'] if cfg['type'] == 'vite' else '.next'
            content = f"""[build]
  command = "pnpm install --no-frozen-lockfile && pnpm run build"
  publish = "{pub}"

[build.environment]
  NODE_VERSION = "24"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        elif cfg['type'] == 'static':
            content = """[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        (path / 'netlify.toml').write_text(content)
        print(f'Created: {name}/netlify.toml')

    # wrangler.toml
    if 'wrangler' in cfg['needs']:
        pub = cfg['out_dir'] if cfg['type'] != 'nextjs' else '.next'
        if cfg['type'] == 'static':
            pub = '.'
        content = f"""name = "{name}"
pages_build_output_dir = "{pub}"
"""
        (path / 'wrangler.toml').write_text(content)
        print(f'Created: {name}/wrangler.toml')

    # .github/workflows
    if 'workflows' in cfg['needs']:
        workflows_dir = path / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Vercel deploy workflow
        vc = f"""name: Deploy Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: {{ node-version: 24, cache: pnpm }}
      - run: pnpm install --no-frozen-lockfile
      - run: pnpm run build
      - uses: amondnet/vercel-action@v25
        if: github.ref == 'refs/heads/main'
        with:
          vercel-token: ${{{{ secrets.VERCEL_TOKEN }}}}
          vercel-org-id: ${{{{ secrets.VERCEL_ORG_ID }}}}
          vercel-project-id: ${{{{ secrets.VERCEL_PROJECT_ID }}}}
          vercel-args: "--prod"
"""
        (workflows_dir / 'deploy-vercel.yml').write_text(vc)
        print(f'Created: {name}/.github/workflows/deploy-vercel.yml')

        # Netlify deploy workflow
        pub_dir = cfg['out_dir'] if cfg['type'] != 'nextjs' else '.next'
        nc = f"""name: Deploy Netlify
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: {{ node-version: 24, cache: pnpm }}
      - run: pnpm install --no-frozen-lockfile
      - run: pnpm run build
      - uses: nwtgck/actions-netlify@v3.0
        if: github.ref == 'refs/heads/main'
        with:
          publish-dir: ./{pub_dir}
          production-branch: main
          github-token: ${{{{ secrets.GITHUB_TOKEN }}}}
          deploy-message: "Deploy from GitHub Actions"
          enable-pull-request-comment: false
          enable-commit-comment: true
          overwrites-pull-request-comment: true
        env:
          NETLIFY_AUTH_TOKEN: ${{{{ secrets.NETLIFY_AUTH_TOKEN }}}}
          NETLIFY_SITE_ID: ${{{{ secrets.NETLIFY_SITE_ID }}}}
"""
        (workflows_dir / 'deploy-netlify.yml').write_text(nc)
        print(f'Created: {name}/.github/workflows/deploy-netlify.yml')

        # GitHub Pages workflow (for static/vite)
        if cfg['type'] in ('vite', 'static'):
            pages_dir = cfg['out_dir'] if cfg['type'] == 'vite' else '.'
            pc = f"""name: Deploy GitHub Pages
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
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: {{ node-version: 24, cache: pnpm }}
      - run: pnpm install --no-frozen-lockfile
      - run: pnpm run build
      - uses: actions/upload-pages-artifact@v3
        with: {{ path: {pages_dir} }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
"""
            (workflows_dir / 'deploy-pages.yml').write_text(pc)
            print(f'Created: {name}/.github/workflows/deploy-pages.yml')

        # Cloudflare Pages workflow
        cf_dir = cfg['out_dir'] if cfg['type'] != 'nextjs' else '.next'
        cc = f"""name: Deploy Cloudflare Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: {{ node-version: 24, cache: pnpm }}
      - run: pnpm install --no-frozen-lockfile
      - run: pnpm run build
      - uses: cloudflare/pages-action@v1
        if: github.ref == 'refs/heads/main'
        with:
          apiToken: ${{{{ secrets.CLOUDFLARE_API_TOKEN }}}}
          accountId: ${{{{ secrets.CLOUDFLARE_ACCOUNT_ID }}}}
          projectName: {name}
          directory: ./{cf_dir}
          branch: main
"""
        (workflows_dir / 'deploy-cloudflare.yml').write_text(cc)
        print(f'Created: {name}/.github/workflows/deploy-cloudflare.yml')

print('Done generating all configs')