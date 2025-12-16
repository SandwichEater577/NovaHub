#!/usr/bin/env python3
import os

project_root = r'c:\Users\MichalStanistalKostk\Documents\NovaHub (Github)\NovaHub'
src_file = os.path.join(project_root, 'src', 'Novahub.py')
dst_file = os.path.join(project_root, 'src', 'Valyxo.py')

# Read the original
with open(src_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Apply all replacements
replacements = [
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
]

count = 0
for old, new in replacements:
    c = content.count(old)
    content = content.replace(old, new)
    count += 1
    if c > 0:
        print(f'Replaced {c}x: {old}')

# Write the complete rebranded file
with open(dst_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✓ Completed: {dst_file}')
print(f'✓ Size: {len(content)} bytes')
