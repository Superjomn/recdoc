# Title 0

This is the basic usage, execute the python code and output the `stdout`.

:display: "both"
:context: "context0"
```python
print('hello world')

for i in range(10):
    print(i)
```

# The context management
:display: "both"
:context: "c0"
```python
a = 1
b = 2
```

:display: "both"
:context: "c0"
```python
print('a', a)
print('b', b)

a = a + 1
```
:display: "both"
:context: "c0"
```python
print('a should be 2', a)
```
