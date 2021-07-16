import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parse import Parser


def test_basic():
    parser = Parser()
    ss = '''
```python
print('hello')
a = 1
b = 2
def func(name):
    print(name)
```
'''
    res = parser.parse(ss)

    print(res)

def test_run():
    parser = Parser()
    ss = '''
```python
print('hello')
a = 1
b = 2
def func(name):
    print(name)
```
'''
    res = parser.run(ss)
    print('**res', '\n'.join(res))


def test_preprocess():
    parser = Parser()
    ss = '''
:display: stdout
:summary_size: 100
```python
print('hello')
a = 1
b = 2
def func(name):
    print(name)
```
'''
    res: str = '\n'.join(parser.preprocess_inlined_redocs(ss))
    print('res', res)
    assert res.strip() == '''
```redoc
display := stdout
summary_size := 100
```
```python
print('hello')
a = 1
b = 2
def func(name):
    print(name)
``` 
    '''.strip()

def test_parse_1():
    file = open('./data/1_basic.md').read()
    parser = Parser()
    lines = parser.run(file)
    print('\n'.join(lines))



