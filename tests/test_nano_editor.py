import os, sys
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import NovaFileSystem, NovaHubShell, path_within_root


def test_nano_create_and_insert(tmp_path):
    # Monkeypatch root dirs to use a temporary path
    import Novahub as nh
    nh.ROOT_DIR = str(tmp_path)
    nh.PROJECTS_DIR = os.path.join(str(tmp_path), 'Projects')
    nh.MAIN_PROJECT = os.path.join(nh.PROJECTS_DIR, 'Main')
    shell = NovaHubShell()
    shell.fs.ensure_dirs()
    p = shell.fs.create_file(shell.fs.cwd or nh.MAIN_PROJECT, 'testfile.ns', ask_lang=False)
    assert os.path.exists(p)
    # Write some content and verify
    with open(p, 'w', encoding='utf-8') as f:
        f.write('print "Hello Test"\n')
    # Use path_within_root
    assert path_within_root(p) is not None

