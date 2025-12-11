import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import NovaScriptRuntime
import pytest


def test_for_loop_prints(capsys):
    runtime = NovaScriptRuntime()
    runtime.run_line('set sum = 0')
    runtime.run_line('for i in 1 to 3 {')
    runtime.run_line('  print i')
    runtime.run_line('  set sum = sum + i')
    runtime.run_line('}')
    captured = capsys.readouterr()
    assert '1' in captured.out and '2' in captured.out and '3' in captured.out


def test_while_loop_print(capsys):
    runtime = NovaScriptRuntime()
    runtime.run_line('set i = 1')
    runtime.run_line('while [i <= 3] {')
    runtime.run_line('  print i')
    runtime.run_line('  set i = i + 1')
    runtime.run_line('}')
    captured = capsys.readouterr()
    assert '1' in captured.out and '2' in captured.out and '3' in captured.out


def test_infinite_loop_detection():
    runtime = NovaScriptRuntime()
    runtime.MAX_ITERATIONS = 10
    runtime.run_line('set i = 1')
    with pytest.raises(RuntimeError):
        runtime.run_line('while [True] {')
        runtime.run_line('  set i = i + 1')
        runtime.run_line('}')
