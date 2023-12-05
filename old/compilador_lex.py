
import ply.lex as lex


states = (

    ('declare', 'exclusive'),
    ('atrib', 'exclusive'),
    ('comment', 'exclusive'),
    ('stdin', 'exclusive'),
    ('stdout', 'exclusive'),
    #('if', 'exclusive'),

)


tokens = ['DECBEGIN', 'XMLEND', 'COMBEGIN', 'COMCONTENT',
          'STDIN', 'STDOUT', 'VAR', 'ATRIBEGIN', 'NUM']

literals = ['(', ')', '+', '-', '*', '/', '=']


# rules for initial state 0


def t_DECBEGIN(t):
    r'<declare'
    t.lexer.push_state('declare')
    return t


def t_ATRIBEGIN(t):
    r'<atrib'
    t.lexer.push_state('atrib')
    return t


def t_STDIN(t):
    r'<stdin'
    t.lexer.push_state('stdin')
    return t


def t_STDOUT(t):
    r'<stdout'
    t.lexer.push_state('stdout')
    return t

# def t_CONTENT(t):
#    r'[a-z][A-Z]'

    #print(t.value, end='')


def t_COMBEGIN(t):
    r'<comentario'
    t.lexer.push_state('comment')
    return t

# Rules for declare state


def t_declare_NUM(t):
    r'\d+'
    return t


def t_declare_XMLEND(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_declare_VAR(t):
    r'[a-zA-Z]\w*'
    return t

# Rules for atrib state

#    "Operacao : ATRIBEGIN VAR '=' EXP XMLEND"


def t_atrib_NUM(t):
    r'\d+'
    return t


def t_atrib_XMLEND(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_atrib_VAR(t):
    r'[a-zA-Z]\w*'
    return t


# Rules for comment state


def t_comment_XMLEND(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_comment_COMCONTENT(t):
    r'[a-zA-Z]+'
    t.lexer.skip(1)
    return t


# Rules for stdin state


def t_stdin_XMLEND(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_stdin_VAR(t):
    r'[a-zA-Z]+'
    t.lexer.skip(1)
    return t


# Rules for stdout state

def t_stdout_XMLEND(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_stdout_VAR(t):
    r'[a-zA-Z]+'
    t.lexer.skip(1)
    return t


t_ANY_ignore = " \t\n"


# Error rule for all states


def t_ANY_error(t):

    print('Caráter ilegal: ', t.value)


# build the lexer


lexer = lex.lex()


# PARA TESTAR O ANALISADOR LEXICO:
"""
import sys
for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(tok)
"""
