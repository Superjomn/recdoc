import sys
from typing import Dict, List
from backends.py import CodeExecutor as PythonCodeExecutor
import logging


class Parser(object):
    def __init__(self):
        self.code_block: List[str] = []
        self.code_block_lang: str = ''
        self.py_code_executor: PythonCodeExecutor = PythonCodeExecutor()

    def eval_python(self, code: str):
        self.py_code_executor.eval(code)

    def parse(self, text: str):
        lines = []
        for line in text.split('\n'):
            line: str = line.rstrip()

            logging.info('line %s [%s]' % (line, self.code_block_lang))
            if line.strip() == '```redoc':
                logging.warning('redoc begin')
                self.code_block_lang = 'redoc'
            elif line.strip() == '```python':
                logging.warning('python begin')
                self.code_block_lang = 'python'
            elif line.strip() == '```':
                logging.warning("lang %s ends" % self.code_block_lang)
                if self.code_block_lang == 'redoc':
                    self.code_block_lang = ''
                    print('redoc', self.code_block)
                elif self.code_block_lang == 'python':
                    self.code_block_lang = ''
                    print('code block:', self.code_block)
                    self.py_code_executor.eval('\n'.join(self.code_block))

            elif self.code_block_lang:
                logging.warning('add line to code block')
                self.code_block.append(line)
            else:
                lines.append(line)
        return lines
