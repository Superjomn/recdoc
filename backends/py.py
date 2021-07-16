'''
This file defines the python backend, which helps to execute python code and manage the context.
'''
from io import StringIO
import logging
from typing import Dict, Tuple, Any
import sys
from copy import deepcopy


def eval_code(code: str, __globals=globals(), __locals=locals()):
    exec(code, __globals, __locals)


origin_sys_stdout = sys.stdout
origin_sys_stderr = sys.stderr


class StdoutManager:
    stdout = origin_sys_stdout
    stderr = origin_sys_stderr

    my_stdout = StringIO()
    my_stderr = StringIO()

    @staticmethod
    def get_my_stdout_content():
        return StdoutManager.my_stdout.getvalue()

    @staticmethod
    def get_my_stdout_content():
        return StdoutManager.my_stderr.getvalue()

    @staticmethod
    def record_stdout():
        sys.stdout = StdoutManager.my_stdout

    @staticmethod
    def record_stderr():
        sys.stderr = StdoutManager.my_stderr

    @staticmethod
    def clear_stdout():
        StdoutManager.my_stdout = StringIO()

    @staticmethod
    def clear_stderr():
        StdoutManager.my_stdout = StringIO()

    @staticmethod
    def restore_stdout():
        sys.stdout = origin_sys_stdout

    @staticmethod
    def restore_stderr():
        sys.stderr = origin_sys_stderr


class Scope(object):
    '''
    Make the context inheriable.
    '''

    def __init__(self, name: str, parent: "Scope" = None):
        '''
        context: the parent scope.
        '''
        self.name = name
        self.parent = parent
        self.data: Dict[str, Any] = deepcopy(parent.data) if parent else {}


class CodeExecutor(object):
    ''' Execute a python code snippet. '''

    def __init__(self):
        self.__globals = {'StdoutManager': StdoutManager, }
        self.__locals = {}
        self.scopes : [str, Scope] = {}

    def create_scope(self, name:str):
        if name not in self.scopes:
            logging.info("create context [%s]" % name)
            self.scopes[name] = Scope(name)
        return self.scopes[name]

    def eval(self, code: str, context: str = ""):
        if context:
            logging.info("eval in context: %s" % context)
            scope = self.create_scope(context)
            eval_code(code, self.__globals, scope.data)
            logging.info("result: %s" % scope.data)
        else:
            eval_code(code, self.__globals, {})
