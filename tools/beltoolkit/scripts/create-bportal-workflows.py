#!/usr/bin/env python3
"""Create bportal workflows."""

from pathlib import Path

path = Path.home() / 'Downloads' / 'bportal' / '.github' / 'workflows'
path.mkdir(parents=True, exist_ok=True)

vc = """name: Deploy Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24 }
      - run: npm install
      - uses: amondnet/vercel-action@v25
        if: github.ref == "refs/heads/main"
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
"""
(path / 'deploy-vercel.yml').write_text(vc)

nc = """name: Deploy Netlify
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24 }
      - run: npm install
      - uses: nwtgck/actions-netlify@v3.0
        if: github.ref == "refs/heads/main"
        with:
          publish-dir: .
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
          enable-pull-request-comment: false
          enable-commit-comment: true
          overwrites-pull-request-comment: true
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
"""
(path / 'deploy-netlify.yml').write_text(nc)

pc = """name: Deploy GitHub Pages
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
      - uses: actions/setup-node@v4
        with: { node-version: 24 }
      - run: npm install
      - uses: actions/upload-pages-artifact@v3
        with: { path: . }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
"""
(path / 'deploy-pages.yml').write_text(pc)

cc = """name: Deploy Cloudflare Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24 }
      - run: npm install
      - uses: cloudflare/pages-action@v1
        if: github.ref == "refs/heads/main"
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: bportal
          directory: .
          branch: main
"""
(path / 'deploy-cloudflare.yml').write_text(cc)

print('Created bportal workflows')