#!/bin/bash
cd "$(dirname "$0")"
python3 << 'PYEOF'
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('src/Novahub.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply all replacements
for old, new in [
    ('NovaHubShell', 'ValyxoShell'),
    ('NovaFileSystem', 'ValyxoFileSystem'),
    ('NovaScriptRuntime', 'ValyxoScriptRuntime'),
    ('NovaGPTModule', 'ValyxoGPTModule'),
    ('NovaJobsManager', 'ValyxoJobsManager'),
    ('NovaManSystem', 'ValyxoManSystem'),
    ('highlight_novascript', 'highlight_valyxoscript'),
    ('NovaScript', 'ValyxoScript'),
    ('NovaGPT', 'ValyxoGPT'),
    ('NovaHubDocuments', 'ValyxoDocuments'),
    ('NovaHub', 'Valyxo'),
    ('NScript', 'VScript'),
    ('NGPT', 'VGPT'),
    ('Valyxo D-Edition v1.1', 'Valyxo v0.31'),
]:
    content = content.replace(old, new)

with open('src/Valyxo.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Rebrand complete: {len(content)} bytes")
PYEOF
