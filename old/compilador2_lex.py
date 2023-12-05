
import ply.lex as lex


tokens = ['DECBEGIN', 'XMLEND', 'DEC', 'COMBEGIN', 'COMCONTENT',
          'STDIN', 'STDOUT', 'IFBEGIN', 'VAR']

t_DECBEGIN = r'<declare'
#t_STDIN = r'<stdin'
#t_STDOUT = r'<stdout'
t_XMLEND = r'/>'
t_COMBEGIN = r'<comentario'
t_DEC = r'[a-zA-Z]+'
#t_IFBEGIN = r'<if'
#t_VAR = r'[a-zA-Z]+'
#t_COMCONTENT = r'[^\]+'


t_ignore = " \t\n"


def t_error(t):
    t.lexer.skip(1)
    return t


lexer = lex.lex()


# PARA TESTAR O ANALISADOR LEXICO:

#import sys
#for linha in sys.stdin:
#    lexer.input(linha)
 #   for tok in lexer:
 #       print(tok)
