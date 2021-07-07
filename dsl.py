import ply
import ply.lex as lex
import logging
import ply.yacc as yacc
from typing import Dict, Any

log = logging.getLogger('ply')


class RecdocLexer(object):
    tokens = (
        'NAME',
        'NUMBER',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN',
        'RPAREN',
        'STRING',
    )

    # tokens
    t_EQUALS = r':='

    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    states = (
        ('string', 'exclusive'),)

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_STRING(self, t):
        r'"'
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.begin('string')

    def t_string_quote(self, t):
        r'"'
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos - 1]
        t.type = "STRING"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        return t

    def t_string_any(self, t):
        r'[^\n]'
        pass

    def t_string_error(self, t):
        print("illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        t_string_ignore = ' \t'

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


class MyParser(object):
    # Parsing rules
    precedence = (
        ('left', 'EQUALS'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    tokens = RecdocLexer.tokens

    def __init__(self):
        # dictionary of names
        self.names: Dict[str, Any] = {}
        self.parser = yacc.yacc(module=self, errorlog=log)

    def p_statement_assign(self, t):
        'statement : NAME EQUALS expression'
        self.names[t[1]] = t[3]

    def p_statement_expr(self, t):
        'statement : expression'
        print(t[1])

    def p_expression_binop(self, t):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression'''
        print('a:', t[0])
        print('a:', t[3])
        if t[2] == '+':
            t[0] = t[1] + t[3]
        elif t[2] == '-':
            t[0] = t[1] - t[3]
        elif t[2] == '*':
            t[0] = t[1] * t[3]
        elif t[2] == '/':
            t[0] = t[1] / t[3]

    def p_expression_uminus(self, t):
        'expression : MINUS expression %prec UMINUS'
        t[0] = -t[2]

    def p_expression_group(self, t):
        'expression : LPAREN expression RPAREN'
        t[0] = t[2]

    def p_expression_number(self, t):
        'expression : NUMBER'
        t[0] = t[1]

    def p_expression_string(self, t):
        'expression : STRING'
        t[0] = t[1]

    def p_expression_name(self, t):
        'expression : NAME'
        try:
            t[0] = self.names[t[1]]
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)


if __name__ == '__main__':
    # Build the lexer
    m = RecdocLexer()
    m.build()
    lexer = lex.lex(object=m)

    parser = MyParser()

    while True:
        try:
            s = input('calc > ')  # Use raw_input on Python 2
        except EOFError:
            break
        parser.parser.parse(s, lexer=m.lexer)
        print(parser.names)
