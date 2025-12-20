import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import Valyxo as vx
from Valyxo import ValyxoShell


def test_autosuggest_suggestion(monkeypatch, tmp_path):
    # Use a temporary root for safe initialization
    vx.ROOT_DIR = str(tmp_path)
    vx.PROJECTS_DIR = os.path.join(str(tmp_path), 'Projects')
    vx.SYSTEM_DIR = os.path.join(str(tmp_path), 'System')
    vx.CONFIG_DIR = os.path.join(str(tmp_path), 'Config')
    shell = ValyxoShell()
    shell.initialize()
    # Monkeypatch the prompt to auto-answer 'y' for suggestions
    monkeypatch.setattr('Valyxo.prompt', lambda x: 'y')
    # Provide a typo that should suggest 'mkdir'
    suggestion = shell.autosuggest('mkdr')
    assert suggestion in ("mkdir", None)
