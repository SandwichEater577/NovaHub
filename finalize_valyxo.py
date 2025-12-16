#!/usr/bin/env python3
"""Copy remaining Novahub.py content to Valyxo.py with proper rebrand"""

import os

with open('src/Novahub.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where our edits end in the original - use line 235
lines = content.split('\n')
# Find line 235 (0-indexed, so 234)
marker_idx = -1
for i, line in enumerate(lines):
    if 'Unknown language. Supported:' in line:
        marker_idx = i
        break

if marker_idx >= 0:
    # Get everything after line 235
    rest_lines = lines[marker_idx + 1:]
    rest = '\n'.join(rest_lines)
    
    # Apply replacements
    replacements = [
        ('NovaGPTModule', 'ValyxoGPTModule'),
        ('NovaJobsManager', 'ValyxoJobsManager'),
        ('NovaManSystem', 'ValyxoManSystem'),
        ('NovaScriptRuntime', 'ValyxoScriptRuntime'),
        ('NovaHubShell', 'ValyxoShell'),
        ('NovaGPT', 'ValyxoGPT'),
        ('NovaScript', 'ValyxoScript'),
        ('NovaHub', 'Valyxo'),
        ('nova_logo', 'valyxo_logo'),
        ('NScript', 'VScript'),
        ('NGPT', 'VGPT'),
    ]
    
    for old, new in replacements:
        rest = rest.replace(old, new)
    
    # Append to Valyxo.py
    with open('src/Valyxo.py', 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write(rest)
    
    print("✓ Finalized Valyxo.py")
else:
    print("✗ Marker not found - using fallback")
