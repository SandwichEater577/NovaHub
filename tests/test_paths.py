import os, sys
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import path_within_root


def test_path_within_root(tmp_path, monkeypatch):
    import Novahub as nh
    monkeypatch.setattr(nh, 'ROOT_DIR', str(tmp_path))
    inside = os.path.join(str(tmp_path), 'foo')
    os.makedirs(inside, exist_ok=True)
    assert path_within_root(inside) == os.path.abspath(inside)
    outside = os.path.abspath(os.path.join(str(tmp_path), '..', 'outside'))
    if os.path.exists(outside):
        pass
    # outside should not be within root
    assert path_within_root(outside) is None
