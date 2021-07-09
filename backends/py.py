'''
This file defines the python backend, which helps to execute python code and manage the context.
'''
from io import StringIO
import sys


def eval_code(code: str, __globals=globals(), __locals=locals()):
    exec(code, __globals, __locals)


class StdoutManager:
    stdout = sys.stdout
    stderr = sys.stderr

    my_stdout = StringIO()
    my_stderr = StringIO()

    @staticmethod
    def record_stdout():
        sys.stdout = StdoutManager.my_stdout

    @staticmethod
    def record_stderr():
        sys.stderr = StdoutManager.my_stderr

    @staticmethod
    def clear_stdout():
        StdoutManager.my_stdout.truncate(0)

    @staticmethod
    def clear_stderr():
        StdoutManager.my_stderr.truncate(0)

    @staticmethod
    def restore_stdout():
        sys.stdout = StdoutManager.stdout

    @staticmethod
    def restore_stdout():
        sys.stderr = StdoutManager.stderr


class CodeExecutor(object):
    ''' Execute a python code snippet. '''

    def __init__(self):
        self.__globals = {'StdoutManager': StdoutManager}
        self.__locals = {}

    def eval(self, code: str):
        eval_code(code, self.__globals, self.__locals)
