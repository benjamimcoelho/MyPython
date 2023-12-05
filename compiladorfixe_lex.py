import ply.lex as lex

reserved = {
    'int': 'INT',
    'print': 'PRINT',
    'read': 'READ',
    'arrayInt': 'ARRAYINT',
    'atr': 'ATR',
    'if': 'IF',
    'else': 'ELSE',
    'endif': 'ENDIF',
    'while': 'WHILE',
    'do': 'DO',
    'endwhile': 'ENDWHILE',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'for': 'FOR',
    'endfor': 'ENDFOR',
    'begindeclares': 'BEGINDECLARES',
    'enddeclares': 'ENDDECLARES',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'prints': 'PRINTS',

}

tokens = ['VAR', 'NUM', 'STRING', 'SIGNEDNUM'] + list(reserved.values())

literals = ['(', ')', '+', '-', '*', '/', '=',
            ';', '[', ']', '<', '>', '!']


def t_VAR(t):
    r'[a-zA-Z]\w*'
    t.type = reserved.get(t.value, 'VAR')    # Check for reserved words
    return t


t_STRING = r'\"(\"|[^"])*\"'


t_NUM = r'\d+'

t_SIGNEDNUM = r'\([+\-]?\d+\)'

t_ignore = " \t\n"


def t_error(t):
    print("Carater ilegal: ", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
