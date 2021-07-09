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


test_basic()
