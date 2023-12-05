import ply.yacc as yacc
from compiladorfixe_lex import tokens
import sys
import re

stack_position = 0
if_counter = 0
if_stack = []
while_stack = []
while_counter = 0
repeat_stack = []
repeat_counter = 0
for_stack = []
for_counter = 0


def getSignedNum(x):
    res = re.fullmatch(r'\(([+\-]?\d+)\)', x)
    return res.group(1)


def push(list, element):
    list.append(element)


def pop(list):
    return list.pop()


def top(list):
    return list[len(list) - 1]


def p_Programa_Operacoes(p):
    "Programa : Operacoes"
    p[0] = p[1]


def p_Operacoes(p):
    "Operacoes : Operacoes Operacao"
    p[0] = p[1] + p[2]


def p_Operacoes_empty(p):
    "Operacoes : "
    p[0] = ''


def p_Operacao_BeginDeclares(p):
    "Operacao : BEGINDECLARES"
    p[0] = ''


def p_Operacao_EndDeclares(p):
    "Operacao : ENDDECLARES"
    p[0] = 'START\n'


def p_Operacao_Read(p):
    "Operacao : READ VAR"
    global variables
    atributes = parser.variables[p[2]]
    p[0] = '   read\n' + '   atoi\n' + \
        '   storeg ' + str(atributes[1]) + '\n'


def p_Operacao_ReadToArray(p):
    "Operacao : READ VAR '[' EXP ']'"
    atributes = parser.variables[p[2]]
    p[0] = '   pushgp\n' + '   pushi ' + \
        str(atributes[1]) + '\n' + '   padd\n' + p[4] + \
        '   read\n' + '   atoi\n' + '   storen\n'


def p_Operacao_ReadToBiArray(p):
    "Operacao : READ VAR '[' EXP ']' '[' EXP ']'"
    atributes = parser.variables[p[2]]
    p[0] = '   pushgp\n' + '   pushi ' + str(atributes[1]) + '\n' + '   padd\n' + p[4] + str(
        atributes[3]) + '  mul\n' + str(atributes[3]) + '  add\n' + '   read\n' + '   atoi\n' + '   storen\n'


def p_Operacao_BeginIF(p):
    "Operacao : IF '(' CONDICOES ')'"
    global if_counter, if_stack
    push(if_stack, if_counter)
    p[0] = p[3]+'   jz ' + 'else' + str(if_counter) + '\n'
    if_counter += 1



def p_CONDICOES(p):
    "CONDICOES : CONDICAO"
    p[0] = p[1]


def p_CONDICOES_NOT(p):
    "CONDICOES : NOT CONDICOES"
    p[0] = p[2] + '   not\n'


def p_CONDICOES_GROUP(p):
    "CONDICOES : '(' CONDICOES ')'"
    p[0] = p[2]


def p_CONDICOES_AND(p):
    "CONDICOES : CONDICOES AND CONDICOES"
    p[0] = p[1] + p[3] + '   mul\n'


def p_CONDICOES_OR(p):
    "CONDICOES : CONDICOES OR CONDICOES"
    p[0] = p[1] + p[3] + '   add\n'


def p_Operacao_Repeat(p):
    "Operacao : REPEAT"
    global repeat_counter
    global repeat_stack
    push(repeat_stack, repeat_counter)
    p[0] = 'repeat' + str(repeat_counter) + ':\n'
    repeat_counter += 1


def p_Operacao_Until(p):
    "Operacao : UNTIL '(' CONDICOES ')'"
    global repeat_stack
    global repeat_counter
    counter = pop(repeat_stack)
    p[0] = p[3] + '   jz ' + 'repeat' + \
        str(counter) + '\n' + 'endrepeat' + str(counter) + ':\n'


def p_Operacao_For(p):
    "Operacao : FOR1 FOR3"
    p[0] = p[1] + p[2]


tmp = ""


def p_FOR3(p):
    "FOR3 : FOR2 Operacao ')' DO"
    global tmp
    tmp = str(p[2])
    p[0] = p[1]


def p_FOR2(p):
    "FOR2 : CONDICOES ';'"
    global for_counter
    p[0] = p[1] + '   jz endfordo' + str(for_counter) + '\n'
    for_counter = for_counter + 1


def p_Operacao_EndFor(p):
    "Operacao : ENDFOR"
    global for_counter, tmp, for_stack
    counter = pop(for_stack)
    p[0] = tmp + '\n' + '   jump fordo' + \
        str(counter) + '\n' + 'endfordo' + str(counter) + ':\n'


def p_Operacao_While(p):
    "Operacao : WHILEI '(' CONDICOES ')' DO"
    global while_counter
    global while_stack
    push(while_stack, while_counter)
    p[0] = p[1] + p[3] + '   jz endwhile' + str(while_counter) + '\n'
    while_counter = while_counter + 1


def p_WHILEI(p):
    "WHILEI : WHILE"
    global while_counter
    global while_stack
    p[0] = 'whiledo' + str(while_counter) + ':\n'


def p_FOR1_FOR(p):
    "FOR1 : FOR '(' Operacao ';'"
    global for_counter
    global for_stack
    push(for_stack, for_counter)
    p[0] = p[3] + 'fordo' + str(for_counter) + ':\n'


def p_Operacao_EndWhile(p):
    "Operacao : ENDWHILE"
    global while_stack
    global while_counter
    counter = pop(while_stack)
    p[0] = '   jump whiledo' + \
        str(counter) + '\n' + 'endwhile' + str(counter) + ':\n'


def p_CONDICAO_Igual(p):
    "CONDICAO : EXP '=' '=' EXP"
    p[0] = p[1] + p[4] + '   equal\n'


def p_CONDICAO_Diferente(p):
    "CONDICAO : EXP '!' '=' EXP"
    p[0] = p[1] + p[4] + '   sub\n'


def p_CONDICAO_Menor(p):
    "CONDICAO : EXP '<' EXP"
    p[0] = p[1] + p[3] + '   inf\n'


def p_CONDICAO_Maior(p):
    "CONDICAO : EXP '>' EXP"
    p[0] = p[1] + p[3] + '   sup\n'


def p_CONDICAO_MenorIgual(p):
    "CONDICAO : EXP '<' '=' EXP"
    p[0] = p[1] + p[4] + '   infeq\n'


def p_CONDICAO_MaiorIgual(p):
    "CONDICAO : EXP '>' '=' EXP"
    p[0] = p[1] + p[4] + '   supeq\n'


def p_Operacao_else(p):
    "Operacao : ELSE Operacoes"
    global if_stack
    counter = top(if_stack)
    p[0] = '   jump ' + 'endIf' + \
        str(counter) + '\n' + 'else' + str(counter) + ':\n' + p[2]


def p_Operacao_EndIF(p):
    "Operacao : ENDIF"
    global if_stack
    counter = pop(if_stack)
    p[0] = 'endIf' + str(counter) + ':\n'


def p_Operacao_int_zero(p):
    "Operacao : INT VAR"
    p[0] = '   pushi 0\n'
    global stack_position
    parser.variables.update({p[2]: ['int', stack_position]})
    stack_position = stack_position + 1


def p_Operacao_int(p):
    "Operacao : INT VAR '=' EXP"
    p[0] = p[4]
    global stack_position
    parser.variables.update({p[2]: ['int', stack_position]})
    stack_position = stack_position + 1


def p_Operacao_arrayInt(p):
    "Operacao : ARRAYINT VAR '[' NUM ']'"

    global stack_position
    parser.variables.update({p[2]: ['arrayInt', stack_position, p[4]]})
    stack_position = stack_position + int(p[4])
    p[0] = '   pushn ' + p[4] + '\n'


def p_Operacao_BiArrayInt(p):
    "Operacao : ARRAYINT VAR '[' NUM ']' '[' NUM ']'"
    global stack_position
    aux = int(p[4]) * int(p[7])
    parser.variables.update(
        {p[2]: ['arrayInt', stack_position, str(aux), p[4]]})
    stack_position = stack_position + aux
    p[0] = '   pushn ' + str(aux) + '\n'


def p_Operacao_Print_EXP(p):
    "Operacao : PRINT EXP"
    p[0] = p[2] + '   writei\n'


def p_Operacao_Atribuir(p):
    "Operacao : ATR VAR '=' EXP"
    atributes = parser.variables[p[2]]
    p[0] = p[4] + '   storeg ' + str(atributes[1]) + '\n'


def p_Operacao_Atribuir_Array(p):
    "Operacao : ATR VAR '[' EXP ']' '=' EXP"
    atributes = parser.variables[p[2]]
    p[0] = '   pushgp\n' + '   pushi ' + \
        str(atributes[1]) + '\n' + '   padd\n' + p[4] + p[7] + '   storen\n'


def p_Operacao_Atribuir_BiArray(p):
    "Operacao : ATR VAR '[' EXP ']' '[' EXP ']' '=' EXP"
    atributes = parser.variables[p[2]]
    p[0] = '   pushgp\n' + '   pushi ' + str(atributes[1]) + '\n' + '   padd\n' + p[4] + \
        '   pushi ' + atributes[3] + '\n' + '   mul\n' + \
        p[7] + '   add\n' + p[10] + '   storen\n'


def p_Operacao_PRINTS(p):
    "Operacao : PRINTS STRING "
    p[0] = '   pushs ' + p[2] + '\n   writes\n'


def p_EXP(p):
    "EXP : EXP '+' TERMO"
    p[0] = p[1] + p[3] + '   add\n'


def p_EXP_sub(p):
    "EXP : EXP '-' TERMO"
    p[0] = p[1] + p[3] + '   sub\n'


def p_TERMO(p):
    "EXP : TERMO"
    p[0] = p[1]


def p_TERMO_mul(p):
    "TERMO : TERMO '*' FACTOR"
    p[0] = p[1] + p[3] + '   mul\n'


def p_TERMO_div(p):
    "TERMO : TERMO '/' FACTOR"
    p[0] = p[1] + p[3] + '   div\n'


def p_FACTOR(p):
    "TERMO : FACTOR"
    p[0] = p[1]


def p_FACTOR_group(p):
    "FACTOR : '(' EXP ')'"
    p[0] = p[2]


def p_FACTOR_NUM(p):
    "FACTOR : NUM"
    p[0] = '   pushi ' + p[1] + '\n'


def p_FACTOR_SIGNEDNUM(p):
    "FACTOR : SIGNEDNUM"
    p[0] = '   pushi ' + getSignedNum(p[1]) + '\n'


def p_FACTOR_VAR(p):
    "FACTOR : VAR"
    atributes = parser.variables[p[1]]
    p[0] = '   pushg ' + str(atributes[1]) + '\n'


def p_FACTOR_ArrayInt(p):
    "FACTOR : VAR '[' EXP ']'"
    atributes = parser.variables[p[1]]
    p[0] = '   pushgp\n' + '   pushi ' + \
        str(atributes[1]) + '\n' + '   padd\n' + p[3] + '\n' + '   loadn\n'


def p_FACTOR_BiArrayInt(p):
    "FACTOR : VAR '[' EXP ']' '[' EXP ']'"
    atributes = parser.variables[p[1]]
    p[0] = '   pushgp\n' + '   pushi ' + \
        str(atributes[1]) + '\n' + '   padd\n' + p[3] + \
        '   pushi ' + atributes[3] + '\n' + '   mul\n' + \
        p[6] + '   add\n' + '   loadn\n'


def p_error(p):
    print("Syntax error in input: ", p)


parser = yacc.yacc()

parser.variables = {}


def getName(input):
    res = re.match(r'(\w+)\.vm', input)
    return res.group(1)


def printHelpMenu():
    print('''\n\nPara utilizar o compilador: python   .\\compilador_yacc.py input.vm \n \nOnde input.vm é o ficheiro input.\nO código assembly para a máquina VM será criado
no ficheiro input_out.vm no diretório vms/\n\n
Opções adicionais: \n\n -s para o compilador não gerar output\n\n''')


silent = 0

if (sys.argv[1] == '-help'):
    printHelpMenu()
else:
    if len(sys.argv) > 2:
        if sys.argv[2] == '-s':
            silent = 1
    f = open('vms/' + getName(sys.argv[1]) + '_out.vm', 'w')
    with open(sys.argv[1]) as input:
        for linha in input:
            if linha != '\n':
                result = parser.parse(linha)
                f.write(result)
                if result and silent == 0:
                    print('Frase valida: \n\n' + result)
    if silent == 0:
        print(parser.variables)

    f.write('STOP\n')

    f.close()
