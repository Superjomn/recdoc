# Recdoc

Recdoc is a markdown-like DSL for writing documents that includes some instruction commands (such as bash shell commands and python codes).

## Motivation
In writing a technological tutorial, it is natural to demonstrate a function by writing some instructions such as commands or codes,
readers will follow the instructions and reproduce the result.

Due to the version upgrading, variant setup environments, the tutorial might be unstable. 
e.g. a tutorial might fail after a new version for the document is just a text and can't be tested in a CI system like code.

In the real world, the Jupyter Notebook works well in document reproduction, but it only feet the python world.
For the scenarios such as bash commands and several programming, language mixtures are not supported.

## What is Recdoc, and what it is not?
Recdoc is a DSL -- an extension of markdown syntax, it makes the text document executable so that we can maintain the documentation in a CI system.

Recdoc project itself implements the DSL and uses a pre-process of markdown files, so you can write documentation just like markdown but add several special code snippets.


## Examples


<pre>

Some global settings
```recdoc
bash-path := "xxx/xxx"
python-path := "xxx/xxx"
```

# Head 1

:output: true
:output-length: 500
```python
print('hello')
```

:output: true
:display: true
```sh
echo "hello"
```
</pre>

