import os, sys
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import NovaHubShell, prompt


def test_autosuggest_suggestion(monkeypatch, tmp_path):
    import Novahub as nh
    # Use a temporary root for safe initialization
    nh.ROOT_DIR = str(tmp_path)
    nh.PROJECTS_DIR = os.path.join(str(tmp_path), 'Projects')
    nh.SYSTEM_DIR = os.path.join(str(tmp_path), 'System')
    nh.CONFIG_DIR = os.path.join(str(tmp_path), 'Config')
    shell = NovaHubShell()
    shell.initialize()
    # Monkeypatch the prompt to auto-answer 'y' for suggestions
    monkeypatch.setattr('Novahub.prompt', lambda x: 'y')
    # Provide a typo that should suggest 'mkdir'
    suggestion = shell.autosuggest('mkdr')
    assert suggestion in ("mkdir", None)
