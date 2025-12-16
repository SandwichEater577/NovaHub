#!/usr/bin/env python3
import sys
import os

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_path, "src"))

print("=" * 60)
print("Testing Valyxo Modular Structure")
print("=" * 60)

try:
    from valyxo.core.colors import Colors, color, DEFAULT_THEMES
    print("[OK] valyxo.core.colors")
except Exception as e:
    print(f"[FAIL] valyxo.core.colors: {e}")

try:
    from valyxo.core.constants import APP_NAME, VERSION, COMMANDS
    print(f"[OK] valyxo.core.constants (APP_NAME={APP_NAME})")
except Exception as e:
    print(f"[FAIL] valyxo.core.constants: {e}")

try:
    from valyxo.core.utils import prompt, path_within_root, normalize_virtual_path
    print("[OK] valyxo.core.utils")
except Exception as e:
    print(f"[FAIL] valyxo.core.utils: {e}")

try:
    from valyxo.core.filesystem import ValyxoFileSystem
    print("[OK] valyxo.core.filesystem")
except Exception as e:
    print(f"[FAIL] valyxo.core.filesystem: {e}")

try:
    from valyxo.core.gpt import ValyxoGPTModule
    print("[OK] valyxo.core.gpt")
except Exception as e:
    print(f"[FAIL] valyxo.core.gpt: {e}")

try:
    from valyxo.core.jobs import ValyxoJobsManager
    print("[OK] valyxo.core.jobs")
except Exception as e:
    print(f"[FAIL] valyxo.core.jobs: {e}")

try:
    from valyxo.core.man import ValyxoManSystem
    print("[OK] valyxo.core.man")
except Exception as e:
    print(f"[FAIL] valyxo.core.man: {e}")

try:
    from valyxo.core import (
        Colors, color, DEFAULT_THEMES,
        APP_NAME, VERSION, COMMANDS, LANG_MAP,
        prompt, path_within_root, normalize_virtual_path,
        ValyxoFileSystem, ValyxoGPTModule, ValyxoJobsManager, ValyxoManSystem,
    )
    print("[OK] valyxo.core (complete)")
except Exception as e:
    print(f"[FAIL] valyxo.core (complete): {e}")

try:
    from Valyxo import ValyxoShell
    print("[OK] Valyxo.ValyxoShell")
except Exception as e:
    print(f"[FAIL] Valyxo.ValyxoShell: {e}")

print("=" * 60)
print("All imports completed!")
print("=" * 60)
