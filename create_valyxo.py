#!/usr/bin/env python3
"""Create rebrandedValyxo.py from Novahub.py"""

import os
import sys

def rebrand_file():
    src_path = os.path.join(os.path.dirname(__file__), 'src', 'Novahub.py')
    dst_path = os.path.join(os.path.dirname(__file__), 'src', 'Valyxo.py')
    
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}")
        return False
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = [
        # Classes - most specific first
        ('NovaHubShell', 'ValyxoShell'),
        ('NovaFileSystem', 'ValyxoFileSystem'),
        ('NovaScriptRuntime', 'ValyxoScriptRuntime'),
        ('NovaGPTModule', 'ValyxoGPTModule'),
        ('NovaJobsManager', 'ValyxoJobsManager'),
        ('NovaManSystem', 'ValyxoManSystem'),
        
        # Function names
        ('highlight_novascript', 'highlight_valyxoscript'),
        
        # Language names
        ('NovaScript', 'ValyxoScript'),
        ('NovaGPT', 'ValyxoGPT'),
        
        # Directory and app names
        ('NovaHubDocuments', 'ValyxoDocuments'),
        ('NovaHub', 'Valyxo'),
        
        # Command aliases
        ('NScript', 'VScript'),
        ('NGPT', 'VGPT'),
        
        # Version
        ('NovaHub D-Edition v1.1', 'Valyxo v0.31'),
    ]
    
    for old, new in replacements:
        count = content.count(old)
        content = content.replace(old, new)
        if count > 0:
            print(f"  Replaced {count} occurrences of '{old}' → '{new}'")
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    file_size = len(content)
    print(f"\n✓ Created {dst_path}")
    print(f"✓ File size: {file_size:,} bytes")
    return True

if __name__ == '__main__':
    if rebrand_file():
        sys.exit(0)
    else:
        sys.exit(1)
