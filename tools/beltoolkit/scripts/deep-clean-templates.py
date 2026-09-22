#!/usr/bin/env python3
"""Deep clean template.json - parse and clean embedded package.json."""

import json
from pathlib import Path

HOME = Path.home()

def clean_embedded_pkg(pkg_str):
    """Clean Manus deps from embedded package.json string."""
    try:
        pkg = json.loads(pkg_str)
        # Clean devDependencies
        if 'devDependencies' in pkg:
            deps = pkg['devDependencies']
            if 'vite-plugin-manus-runtime' in deps:
                del deps['vite-plugin-manus-runtime']
            if '@builder.io/vite-plugin-jsx-loc' in deps:
                del deps['@builder.io/vite-plugin-jsx-loc']
        return json.dumps(pkg, indent=2)
    except Exception as e:
        print(f"Error parsing embedded pkg: {e}")
        return pkg_str

for name in ['belentani7-profile', 'lingua-aberta']:
    path = HOME / name / 'template.json'
    if path.exists():
        content = path.read_text(encoding='utf-8')
        data = json.loads(content)
        if 'files' in data and 'package.json' in data['files']:
            data['files']['package.json'] = clean_embedded_pkg(data['files']['package.json'])
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'Deep cleaned: {name}/template.json')

# secure-t-check
path = HOME / 'Downloads' / 'secure-t-check' / 'template.json'
if path.exists():
    content = path.read_text(encoding='utf-8')
    data = json.loads(content)
    if 'files' in data and 'package.json' in data['files']:
        data['files']['package.json'] = clean_embedded_pkg(data['files']['package.json'])
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Deep cleaned: secure-t-check/template.json')

print('Done deep cleaning template.json files')