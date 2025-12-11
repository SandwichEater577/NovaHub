import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Novahub import NovaScriptRuntime


def test_function_definition_and_call(capsys):
    runtime = NovaScriptRuntime()
    runtime.run_line('func greet(name) {')
    runtime.run_line('  print "Hello " + name')
    runtime.run_line('}')
    runtime.run_line('greet("Test")')
    captured = capsys.readouterr()
    assert 'Hello Test' in captured.out


def test_function_with_return_like_behavior(capsys):
    runtime = NovaScriptRuntime()
    runtime.run_line('func add(a, b) {')
    runtime.run_line('  print a + b')
    runtime.run_line('}')
    runtime.run_line('add(3, 4)')
    captured = capsys.readouterr()
    assert '7' in captured.out
