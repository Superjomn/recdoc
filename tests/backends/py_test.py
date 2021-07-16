import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backends.py import eval_code, StdoutManager


def test_basic():
    a = '''
a = "hello world"
    '''
    g = {}
    l = {}
    eval_code(a, g, l)
    assert "a" in l
    assert l["a"] == "hello world"


def test_function_def():
    a = '''
def inc(x):
    return x + 1
    '''
    g = {}
    l = {}
    eval_code(a, g, l)
    b = '''
a = 1
a = inc(a)
    '''
    eval_code(b, g, l)
    assert l['a'] == 2


def test_stdout():
    StdoutManager.record_stdout()
    print("hello world")
    out = StdoutManager.my_stdout.getvalue()
    assert out == "hello world\n"
    StdoutManager.restore_stdout()
    StdoutManager.clear_stdout()
    print("hello world")
    res = StdoutManager.my_stdout.getvalue()
    assert res == ""


def test_redirect_stdout():
    a = '''
import sys
StdoutManager.clear_stdout()
StdoutManager.record_stdout()

print('1234')
a = StdoutManager.my_stdout.getvalue()
StdoutManager.clear_stdout()
StdoutManager.record_stdout()

print('hello world')
StdoutManager.restore_stdout()
    '''
    g = {
        'StdoutManager': StdoutManager,
    }
    l = {}
    eval_code(a, g, l)
    StdoutManager.restore_stdout()
    print('aaaaaaaaa')
    print('l', l['a'])
    assert l['a'] == "1234\n"
    res = StdoutManager.my_stdout.getvalue()

    print('stdout', res)
    assert res == "hello world\n"