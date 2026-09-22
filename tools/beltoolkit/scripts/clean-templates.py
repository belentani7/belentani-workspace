#!/usr/bin/env python3
"""Clean Manus from template.json files."""

import json
from pathlib import Path

HOME = Path.home()

for name in ['belentani7-profile', 'lingua-aberta']:
    path = HOME / name / 'template.json'
    if path.exists():
        content = path.read_text(encoding='utf-8')
        content = content.replace('"vite-plugin-manus-runtime": "0.0.59",', '')
        content = content.replace('"@builder.io/vite-plugin-jsx-loc": "^0.1.1",', '')
        content = content.replace('"vite-plugin-manus-runtime": "^0.0.58",', '')
        path.write_text(content, encoding='utf-8')
        print(f'Cleaned: {name}/template.json')

path = HOME / 'Downloads' / 'secure-t-check' / 'template.json'
if path.exists():
    content = path.read_text(encoding='utf-8')
    content = content.replace('"vite-plugin-manus-runtime": "^0.0.58",', '')
    content = content.replace('"@builder.io/vite-plugin-jsx-loc": "^0.1.1",', '')
    path.write_text(content, encoding='utf-8')
    print(f'Cleaned: secure-t-check/template.json')

print('Done cleaning template.json files')