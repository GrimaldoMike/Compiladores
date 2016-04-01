# Proyecto compilador Python
# PLY de Fight Compilers 2016
# Parte Yacc
# Hecho por Jaime Neri y Mike Grimaldo

import ply.yacc as yacc
import sys
import pprint
import FightCompilersLex
#import FightCompilersSemantics
from FightCompilersSemantics import Semantics
from Queue import Queue

tokens = FightCompilersLex.tokens

pp = pprint.PrettyPrinter(indent=4) #Imprime los diccionarios de manera identada

x = Semantics()		#Crea una clase Semantics. Esta guarda diccionarios
ids = Queue()
var_dict = {}
vars_values = []	#Lista de elementos que guarda el valor de variables
vars_types = []		#Lista de elementos que guarda los tipos de variables
vars_size = []		#Lista de elementos que guarda el tamano de variables
procs_values = []	#Lista de elementos que guarda el valor de procedimientos
procs_types = []	#Lista de elementos que guarda los tipos de procedimientos


# Parsing Rules
def p_juego(p):
	'''Juego : JUEGO ID DOSP JuegoA JuegoB MainProgram'''
	x.current_fid = p[2]
	pass
	x.procs = x.add_procs_to_dict(p[2],p[1], 'void', var_dict)
	pp.pprint(x.procs)


	'''JuegoA : Vars J
	'''JuegoA : Vars JuegoA
		      | empty'''

def p_juegob(p):
	'''JuegoB : Funcion JuegoB 
			  | empty'''

def p_vars(p):
	'''Vars : VAR Vars2 PCOMA'''

def p_vars2(p):
	'''Vars2 : ID COR_I Exp COR_D VarSize DOSP Tipo Vars3 '''
	pass
	print(vars_size)
	if (ids.vars_exists_in_list((p[1]))):
		vars_types.pop()
		vars_values.pop()
		if len(vars_size) > 1:	#Si existe mas de 1 elemento en la lista de tamano de variables obtiene 2 elementos
			vars_size.pop()
			vars_size.pop()
		else:					#Si no, solo obtiene 1 elemento
			vars_size.pop()		
	else:
		ids.enqueue(p[1])
		if ids.size() > 0:		#Si encuentra que existe un id, significa que hay que agregarlo a la tabla de variables
			#valor = p[2]
			tipo = vars_types.pop()	#obtiene el tipo de la lista de de tipos
			#vars_types.append(tipo)
			sizes1 = None
			sizes2 = None
			if len(vars_size) > 1:	#Si existe mas de 1 elemento en la lista de tamano de variables obtiene 2 elementos
				sizes2 = vars_size.pop()
				sizes1 = vars_size.pop()
			else:					#Si no, solo obtiene 1 elemento
				sizes1 = vars_size.pop()
			identificador =ids.dequeue()
			x.var = x.add_vars_to_dict(tipo,sizes1, sizes2)	#Se manda llamar el proceso de agregar variable al dict y lo guarda en el objeto
			var_dict.update({identificador: x.var})

	#print(p[5])
	#c = 0
	#for i in p:
	#	print (p[c])
	#	c = c+1
	#print(p[2])	

def p_vars3(p):
	'''Vars3 : COMA Vars2
			| empty'''
	pass
	

def p_varsize(p):
	'''VarSize : COR_I Exp COR_D
				| empty'''
	pass

def p_tipo(p):
	'''Tipo : INT
			| FLOAT
			| CHAR
			| VOID'''
	pass
	vars_types.append(p[1])
	#print(vars_types)

def p_mainprogram(p):
	'''MainProgram : MAIN PAR_I PAR_D Bloque'''
 
def p_bloque(p):
	'''Bloque ::= LLAVE_I Estatuto LLAVE_D'''

def p_estatuto(p):
	'''Estatuto : Asignacion PCOMA EstatutoA
				| Condicion PCOMA EstatutoA
				| Lectura PCOMA EstatutoA
				| Escritura PCOMA EstatutoA
				| Llamada PCOMA EstatutoA
				| Character PCOMA EstatutoA
				| Regresa PCOMA EstatutoA
				| LoopWhile PCOMA EstatutoA
				| LoopFor PCOMA EstatutoA'''

def p_estatutoa(p):
	'''EstatutoA : Estatuto 
				 | empty'''

def p_estatuto2(p): 
	'''Estatuto2 : Estatuto2A 
				 | empty '''

def p_estatuto2a(p):
	'''Estatuto2A : Asignacion PCOMA Estatuto2
				 | Condicion PCOMA Estatuto2
				 | Lectura PCOMA Estatuto2
				 | Escritura PCOMA Estatuto2
				 | Llamada PCOMA Estatuto2
				 | Regresa PCOMA Estatuto2
				 | LoopWhile PCOMA Estatuto2
				 | LoopFor PCOMA Estatuto2'''
				
def p_asignacion(p):
	'''Asignacion : ID EXP_EQ Expresion'''

def p_expresion(p):
	'''Expresion : Exp ExpresionA '''

def p_expresiona(p):
	'''ExpresionA : ExpresionB
				  | empty'''

def p_expresionb(p):
	'''ExpresionB : EXP_GT Exp
				  | EXP_LT Exp
				  | EXP_GEQ Exp
				  | EXP_LEQ Exp
			  	  | EXP_DEQ Exp
			  	  | EXP_NEQ Exp'''

def p_exp(p):
	'''Exp : Termino Exp2'''

def p_exp2(p):
	'''Exp2 : OP_PLUS Exp
			| OP_MIN Exp
			| empty '''

def p_termino(p):
	'''Termino : Factor Termino2'''

def p_termino2(p):
	'''Termino2 : OP_MULT Termino
				| OP_DIV Termino
				| empty '''

def p_factor(p):
	'''Factor : PAR_I Expresion PAR_D 
			  | Factor2 VarCte
			  | Llamada'''

def p_factor2(p):
	'''Factor2 : OP_PLUS
			   | OP_MIN
			   | empty '''

def p_varcte(p):
	'''VarCte : ID
			  | CTE_I
			  | CTE_F
		  	  | TRUE
		  	  | FALSE'''
	pass
	vars_size.append(p[1])
	#print(vars_size)


def p_condicion(p):
	'''Condicion : IF PAR_I Expresion PAR_D Bloque CondicionA'''

def p_condiciona(p):
	'''CondicionA : ELSE Bloque
				  | empty '''

def p_escritura(p):
	'''Escritura : OUTPUT PAR_I Escritura2'''

def p_escritura2(p):
	'''Escritura2 :  Expresion Escritura3
				  |  COMILLA Escritura4'''

def p_escritura3(p):
	'''Escritura3 : PAR_D
				  | COMA Escritura2'''


def p_escritura4(p):
	'''Escritura4 : ID Escritura4 
				  | COMILLA Escritura3'''
				  

def p_lectura(p):
	'''Lectura : INPUT PAR_I ID LecturaA PAR_D '''

def p_lecturaa(p):
	'''LecturaA : ID LecturaA
				| empty '''

def p_funcion(p):
	'''Funcion : FUNCTION Tipo ID FuncionA'''
	pass
	#tipo = procs_types.pop()
	#x.procs = x.add_procs_to_dict(p[3],tipo, 'void', {})
	
def p_funciona(p):
	'''FuncionA : PAR_I Params PAR_D Bloque'''

def p_params(p):
	'''Params : Tipo ID Params
			   | empty '''
	#pass
	#x1 = vars_types.pop()
	#id1 = p[2]
	#ids.enqueue(p[2])
	#if ids.size() > 0:		#Si encuentra que existe un id, significa que hay que agregarlo a la tabla de variables	
	


def p_llamada(p):
	'''Llamada : ID PAR_I Llamada2 PAR_D  '''

def p_llamada2(p):
	'''Llamada2 : Expresion Llamada3
				| empty '''

def p_llamada3(p):
	'''Llamada3 : COMA Expresion Llamada3
			 	| empty '''

def p_character(p):
	''' Character : PERSONAJE ID LLAVE_I CharacterB Archetype Estatuto2 LLAVE_D CharacterA '''

def p_charactera(p):
	''' CharacterA :  PERSONAJE ID LLAVE_I CharacterB Archetype Estatuto2 LLAVE_D CharacterA 
			| empty '''

def p_characterb(p):
	''' CharacterB : FVarsAsignacion 
			| empty '''

def p_regresa(p):
	''' Regresa : RETURN Expresion '''

def p_loopwhile(p):
	''' LoopWhile : WHILE LLAVE_D Expresion LLAVE_I  Bloque '''

def p_loopfor(p):
	''' LoopFor : FOR LLAVE_D Asignacion PCOMA Expresion PCOMA Expresion LLAVE_I Bloque '''

def p_fvarasignacion(p):
	''' FVarsAsignacion :     LIFE EXP_EQ Exp FVarsAsignacionA
				| STUN EXP_EQ Exp FVarsAsignacionA
				| TIME EXP_EQ Exp FVarsAsignacionA '''

def p_fvarasignaciona(p):
	''' FVarsAsignacionA :    FVarsAsignacion 
				| empty'''

def p_archetype(p):
	''' Archetype : TYPE EXP_EQ ArchetypeA '''

def p_archetypea(p):
	''' ArchetypeA :  SHOTO EXP_EQ Scomando
			| GRAPPLER EXP_EQ Gcomando
			| CHARGE COMANDOS EXP_EQ Ccomando '''

def p_scomando(p):
	''' Scomando : STANDING ScomandoA '''

def p_scomandoa(p):
	''' ScomandoA :   Estado ScomandoA
			| Attack ScomandoA
			| Sespecial ScomandoA
			| empty '''

def p_gcomando(p):
	''' Gcomando : STANDING GcomandoA '''

def p_gcomandoa(p):
 	''' GcomandoA :   Estado GcomandoA
			| Attack GcomandoA
			| Gespecial GcomandoA
			| empty '''

def p_ccomando(p):
	''' Ccomando : STANDING CcomandoA '''

def p_ccomandoa(p):
 	''' CcomandoA :   Estado CcomandoA
			| Attack CcomandoA
			| Cespecial CcomandoA
			| empty '''

def p_estado(p):
	''' Estado : STANDING 
		   | CROUCHING 
		   | JUMPING 
		   | FORWARD 
		   | BACKWARD '''

def p_sespecial(p):
 	''' Sespecial :   QuarterCF 
			| QuarterCB 
			| ForwardDDF '''

def p_gespecial(p):
	''' Gespecial :   SpinningPD 
			| Lariat '''

def p_cespecial(p):
	''' Cespecial :   BackBackForward 
			| DownDownUp '''

def p_quartercf(p):
	''' QuarterCF : QCF Golpe '''

def p_quartercb(p):
	''' QuarterCB : QCB Patada '''

def p_forwarddf(p):
	''' ForwardDDF : SRK Golpe '''

def p_spinningpd(p):
	''' SpinningPD : SPD Golpe '''

def p_lariat(p):
	''' Lariat : Golpe Golpe Golpe 
		  | Patada Patada Patada '''

def p_backbackforward(p):
	''' BackBackForward : BBF Golpe '''

def p_downdownup(p):
	''' DownDownUp : DDU Patada '''

def p_attack(p):
	''' Attack : Golpe 
		   | Patada 
		   | Agarre '''

def p_golpe(p):
	''' Golpe : PUNCH '''

def p_patada(p):
	''' Patada : KICK '''

def p_agarre(p):
	''' Agarre : GRAB '''

def p_empty(p):
	''' empty : '''

def p_error(p):
	print ("<---Syntax error--->")
	print ("En el input: '{0}'\nEn el caracter: '{1}'\nEn la linea: '{2}'".format(p.type,  p.lexpos, p.lineno))
	print ("En el valor: '{0}'".format(p.value))
	print ("<------------------>")

parser = yacc.yacc()

if(len(sys.argv) > 1):
    if sys.argv[1] == "-f":
        f = open(sys.argv[2], "r")
        s = f.readlines()
    string = ""
    for line in s:
        string += line
    print (string)
    result = parser.parse(string)
else:
    print ("Error")

#def p_expression_plus(p):
 #   'scomando : scomando PLUS ataque'
  #  p[0] = p[1] + p[3]