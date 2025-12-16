import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import Valyxo as vx
from Valyxo import ValyxoShell, path_within_root


def test_nano_create_and_insert(tmp_path):
    # Monkeypatch root dirs to use a temporary path
    vx.ROOT_DIR = str(tmp_path)
    vx.PROJECTS_DIR = os.path.join(str(tmp_path), 'Projects')
    vx.MAIN_PROJECT = os.path.join(vx.PROJECTS_DIR, 'Main')
    shell = ValyxoShell()
    shell.fs.ensure_dirs()
    p = shell.fs.create_file(shell.fs.cwd or vx.MAIN_PROJECT, 'testfile.vs', ask_lang=False)
    assert os.path.exists(p)
    # Write some content and verify
    with open(p, 'w', encoding='utf-8') as f:
        f.write('print "Hello Test"\n')
    # Use path_within_root
    assert path_within_root(p) is not None

