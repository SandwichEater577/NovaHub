#!/usr/bin/env python3
"""Script to rebrand NovaHub to Valyxo"""

import os

# Read the original Novahub.py file
src_path = r'src\Novahub.py'
output_path = r'src\Valyxo.py'

with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Apply replacements in the right order (most specific first)
replacements = [
    ('NovaHubShell', 'ValyxoShell'),
    ('NovaHubDocuments', 'ValyxoDocuments'),
    ('NovaFileSystem', 'ValyxoFileSystem'),
    ('NovaScriptRuntime', 'ValyxoScriptRuntime'),
    ('NovaGPTModule', 'ValyxoGPTModule'),
    ('NovaJobsManager', 'ValyxoJobsManager'),
    ('NovaManSystem', 'ValyxoManSystem'),
    ('highlight_novascript', 'highlight_valyxoscript'),
    ('NovaScript', 'ValyxoScript'),
    ('NovaGPT', 'ValyxoGPT'),
    ('nova_logo', 'valyxo_logo'),
    ('NovaHub', 'Valyxo'),
    ('NScript', 'VScript'),
    ('NGPT', 'VGPT'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Update version to 0.31
content = content.replace(
    'VERSION = "Valyxo D-Edition v1.1 (Zencoder Integrated)"',
    'VERSION = "Valyxo v0.31 (Zencoder Integrated)"'
)

# Write to new Valyxo.py
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Created {output_path}")
print(f"✓ File size: {len(content)} bytes")
