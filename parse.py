import sys
from typing import Dict, List, Tuple, Any
from backends.py import CodeExecutor as PythonCodeExecutor
from backends.py import StdoutManager
from backends.py import origin_sys_stdout, origin_sys_stderr
import logging
from dsl import RedocParser
import re


class CodeBlockConfig:
    class Repr:
        ''' The string representation of all the attributes. '''
        display = 'display'
        display_code = 'display_code'
        context = 'context'

    def __init__(self):
        self.display: str = 'stdout'
        self.display_code: bool = True
        self.context: str = ''


class Parser(object):

    def __init__(self):
        self.code_block: List[str] = []
        self.code_block_lang: str = ''
        self.py_code_executor: PythonCodeExecutor = PythonCodeExecutor()

    def run(self, text) -> List[str]:
        lines = self.preprocess_inlined_redocs(text)
        lines = self.parse('\n'.join(lines))
        return lines

    def eval_python(self, code: str):
        self.py_code_executor.eval(code, self.cur_code_block_config.context)

    def preprocess_inlined_redocs(self, text: str) -> List[str]:
        '''
        replace the

        :attr:value
        :attr:value

        to redocs syntax

        ```redocs
        attr := value
        attr := value
        ```
        '''
        lines = []
        attr_ref = re.compile(r"\:([a-zA-Z_]+)\:[^\S]*([\S]+)")

        redoc_start = False
        redoc_lines = []
        for line in text.split('\n'):
            res = attr_ref.match(line)
            if res:
                redoc_start = True
                var = res.group(1)
                val = res.group(2)
                redoc_lines.append("{var} := {val}".format(var=var, val=val))
            else:
                if redoc_start:
                    lines.append('```redoc')
                    lines += redoc_lines
                    redoc_lines = []
                    lines.append('```')
                    redoc_start = False

                lines.append(line)

        return lines

    def parse(self, text: str):
        logging.warning('parse input:\n%s' % text)
        lines = []
        self.cur_code_block_config: CodeBlockConfig = CodeBlockConfig()

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
                    symbols = self.execute_redoc_code('\n'.join(self.code_block))
                    self.cur_code_block_config = self.create_code_block_config_from_redoc_symbols(symbols)
                elif self.code_block_lang == 'python':
                    out, err = self.execute_python_code('\n'.join(self.code_block))
                    if self.cur_code_block_config.display_code:
                        self.display_python_code(lines)
                    if out: self.display_log(out, lines)
                    if err: self.display_log(err, lines)
                self.code_block_lang = ''
                self.code_block.clear()

            elif self.code_block_lang:
                logging.warning('add line to code block')
                self.code_block.append(line)
            else:
                lines.append(line)
        return lines

    def create_code_block_config_from_redoc_symbols(self, symbols: Dict[str, Any]) -> CodeBlockConfig:
        config = CodeBlockConfig()
        reprs = CodeBlockConfig.Repr
        logging.info('redoc result: %s' % symbols)
        if reprs.display in symbols:
            config.display = symbols[reprs.display]
        if reprs.context in symbols:
            config.context = symbols[reprs.context]
        return config

    def execute_redoc_code(self, code: str) -> Dict[str, Any]:
        executor = RedocParser()
        for line in code.split('\n'):
            executor.parse(line)
        return executor.symbols

    def display_python_code(self, lines: List[str]) -> None:
        '''
        Display the python code to final output.
        '''
        lines.append('```python')
        lines += self.code_block
        lines.append('```')

    def execute_python_code(self, code: str) -> Tuple[str, str]:
        '''
        Execute python code and get the stdout and stderr as output
        '''

        precode = '''
StdoutManager.clear_stdout()
StdoutManager.clear_stderr()
StdoutManager.record_stdout()
StdoutManager.record_stderr()
        '''
        self.py_code_executor.eval(precode + "\n" + code, context=self.cur_code_block_config.context)

        out, err = StdoutManager.my_stdout.getvalue(), StdoutManager.my_stderr.getvalue()

        out = out.strip()
        err = err.strip()

        logging.info('python stdout:\n"%s"' % out)
        logging.info('python stderr:\n"%s"' % err)
        return out, err

    def display_log(self, log: str, lines: List[str], title: str = "Log:") -> None:
        lines.append(title)
        lines.append('```')
        lines.append(log)
        lines.append('```')


if __name__ == '__main__':
    parser = Parser()
    lines = parser.run(sys.stdin.read())
    print('\n'.join(lines))
