# Proyecto compilador Python
# PLY de Fight Compilers 2016
# Parte Lex
# Hecho por Jaime Neri y Mike Grimaldo


import ply.lex as lex
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Tokens

t_STANDING = r'\.st'
t_CROUCHING = r'\.cr'
t_JUMPING = r'\.j'
t_FORWARD = r'\.f'
t_BACKWARD = r'\.b'
t_QCF = r'\.236'
t_QCB = r'\.214'
t_SRK = r'\.623'
t_BBF = r'\.446'
t_DDU = r'\.228'
t_SPD = r'\.89632147'
t_PUNCH = r'\.P(L|M|H)'
t_KICK = r'\.K(L|M|H)'
t_GRAB = r'\.gPH'

t_OP_PLUS    = r'\+'
t_OP_MIN   = r'-'
t_OP_MULT  = r'\*'
t_OP_DIV  = r'/'
t_EXP_EQ  = r'='
t_PAR_I  = r'\('
t_PAR_D  = r'\)'
t_CTE_I = r'[0-9]+'
t_CTE_F = r'[0-9]+\.[0-9]+'
t_EXP_GT = r'>'
t_EXP_LT = r'<'
t_EXP_GEQ = r'>='
t_EXP_LEQ = r'<='
t_EXP_DEQ = r'=='
t_EXP_NEQ = r'<>'
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_COR_I = r'\['
t_COR_D = r'\]'
t_PCOMA = r';'
t_COMA = r','
t_DOSP = r':'
t_COMILLA = r'"'
t_CTE_STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ignore = ' \t\n\r\f\v' #ignorar espacios

# Palabras reservadas
reservadas = {
    'juego'     : 'JUEGO',
    'function'  : 'FUNCTION',
    'personaje' : 'PERSONAJE',
	'if' 		: 'IF',
    'main'      : 'MAIN',
	'else'      : 'ELSE',
    'while'     : 'WHILE',
    'for'       : 'FOR',
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    'var'       : 'VAR',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'char'      : 'CHAR',
    'void'      : 'VOID',
    'life'      : 'LIFE',
    'stun'      : 'STUN',
    'time'      : 'TIME',
    'type'      : 'TYPE',
    'shoto'     : 'SHOTO',
    'grappler'  : 'GRAPPLER',
    'charge'    : 'CHARGE',
    'comandos'  : 'COMANDOS',
    'input'     : 'INPUT',
    'output'    : 'OUTPUT',
    'return'    : 'RETURN'
}

# Lista de tokens

tokens = [
    'ID',
    'CTE_STRING', 'CTE_I', 'CTE_F', 'COMA', 'PCOMA', 'DOSP','COMILLA',
    'STANDING', 'CROUCHING', 'JUMPING', 'FORWARD', 'BACKWARD', 'QCF', 'QCB', 'SRK', 'BBF', 'DDU', 'SPD', 'PUNCH', 'KICK', 'GRAB',
    'OP_PLUS', 'OP_MIN', 'OP_MULT', 'OP_DIV', 'EXP_EQ', 'EXP_GT', 'EXP_LT', 'EXP_NEQ', 'EXP_GEQ', 'EXP_LEQ', 'EXP_DEQ',
    'LLAVE_I', 'LLAVE_D', 'COR_I', 'COR_D', 'PAR_I', 'PAR_D'] + list(reservadas.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value,'ID')
    return t
        
def t_error(t):
    if(t.value[0] != None):
        print("Caracter ilegal '%s'" % t.value[0])
        t.lexer.skip(1)


#Build lexer
lex.lex()
