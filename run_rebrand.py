#!/usr/bin/env python3
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

src_path = 'src/Novahub.py'
dst_path = 'src/Valyxo.py'

print(f"Reading {src_path}...")
with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Content size: {len(content)} bytes")

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
    ('NovaHub D-Edition v1.1', 'Valyxo v0.31'),
]

for old, new in replacements:
    count = content.count(old)
    content = content.replace(old, new)
    if count > 0:
        print(f"Replaced {count}x: {old} -> {new}")

print(f"\nWriting {dst_path}...")
with open(dst_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Created {dst_path} ({len(content)} bytes)")
