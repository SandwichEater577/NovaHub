import os, sys
import io
import tempfile
import platform

# Ensure src directory is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import NovaScriptRuntime, NovaFileSystem


def test_safe_eval_basic():
    runtime = NovaScriptRuntime()
    assert runtime.safe_eval('2 + 3') == 5
    assert runtime.safe_eval('10 - 4') == 6
    assert runtime.safe_eval('2 * 3') == 6
    assert runtime.safe_eval('9 / 3') == 3
    assert runtime.safe_eval('2 ** 3') == 8


def test_set_and_print(capsys):
    runtime = NovaScriptRuntime()
    runtime.run_line('set x = 42')
    assert 'x' in runtime.vars
    runtime.run_line('print x')
    captured = capsys.readouterr()
    assert '42' in captured.out


def test_unknown_variable_raises():
    runtime = NovaScriptRuntime()
    try:
        runtime.safe_eval('y + 1')
        assert False, "Should have raised"
    except RuntimeError:
        assert True
