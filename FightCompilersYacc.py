# Proyecto compilador Python
# PLY de Fight Compilers 2016
# Parte Yacc
# Hecho por Jaime Neri y Mike Grimaldo

import ply.yacc as yacc
import sys
import pprint
import FightCompilersLex
#import FightCompilersSemantics
from FightCompilersSemantics import Semantics, semantics_cube
from Queue import Queue
from quadruples import add_quadruple, check_operation, relational_operators, logical_operators, ignored_checks, get_count_cuadruplos, rellenar_cuadruplo, get_cuadruplos

tokens = FightCompilersLex.tokens

pp = pprint.PrettyPrinter(indent=4) #Imprime los diccionarios de manera identada

x = Semantics()		#Crea una clase Semantics. Esta guarda diccionarios
ids = Queue()
var_dict = {}
vars_values = []	#Lista de elementos que guarda el valor de variables
vars_types = []		#Lista de elementos que guarda los tipos de variables
var_size = []		#Lista de elementos que guarda el tamano de variables
procs_names = []	#Lista de elementos que guarda el nombre de procedimientos
procs_values = []	#Lista de elementos que guarda el valor de procedimientos
procs_types = []	#Lista de elementos que guarda los tipos de procedimientos
local_bracketlist = [] #Lista que tienen los diccionarios de variables
var_brackList = []  #Lista que tienen los diccionarios de variables

var_brackList2 = {  #Lista que tienen los diccionarios de variables
	'global' : {},
	'local'  : {}
}

PilaO = [] #Pila de operandos '5'
POper = [] #Pila de operadores '+' '-' '*' '/'
PTipos = [] #Pila que guarda los tipos e operandos
PSaltos = [] #Pila que guarda los saltos pendientes para la funcion rellenar_Cuadruplo


# Parsing Rules
def p_juego(p):
	'''Juego : JUEGO ID DOSP JuegoA JuegoB MainProgram'''
	x.current_fid = p[2]
	if x.current_fid in x.procs.keys():
		print ('Procedimiento {0} ya existe en el diccionario'.format(p[2]))
		exit(1)
	else:
		pass
		#var_brackList = [4, 5 ,6]
		#var_brackList[0] = 4
		#len(var_brackList) = 3
		for c in range(len(var_brackList)):
			z = var_brackList.pop()
			if (z == '@'):
				pass
			else:
				var_dict.update(z)
		x.procs.update(x.add_procs_to_dict(p[2],p[1], 'void', var_dict))
		#print len(var_brackList)
		#pp.pprint(x.procs)
		#print(var_brackList.pop())
		#print(var_dict)
		#print(POper)
		#print("Pila de saltos: ")	
		#print(PSaltos)	
		pp.pprint(get_cuadruplos())
		print(PilaO)

def p_juegoa(p):
	'''JuegoA : Vars JuegoA
		      | empty'''

def p_juegob(p):
	'''JuegoB : Funcion JuegoB 
			  | Character JuegoB 
			  | empty'''

def p_vars(p):
	'''Vars : VAR Vars2 PCOMA'''

def p_vars2(p):
	'''Vars2 : ID COR_I Exp COR_D VarSize DOSP Tipo Vars3 '''
	#print(var_brackList.keys())
	if (vars_exists_in_list(p[1])):
	#if p[1] in var_brackList.keys():
		vars_types.pop()
		#vars_values.pop()
		#['4', '@', 5, '@']                                                                                                         
		poptemp = PilaO.pop() 
		if (poptemp != "@") and not PilaO:	#Si existe mas de 1 elemento en la lista de tamano de variables obtiene 2 elementos
			poptemp = PilaO.pop()
		print ('Variable "{0}" ya existe en el diccionario'.format(p[1]))
		exit(1)
	else:
		ids.enqueue(p[1])
		if ids.size() > 0:		#Si encuentra que existe un id, significa que hay que agregarlo a la tabla de variables
			tipo = vars_types.pop()	#obtiene el tipo de la lista de de tipos
			#Aqui empieza la validacion  de VARSIZE
			if (PilaO):		#si la lista no esta vacia
				PilaO.pop()				#siempre hay un @ antes de 1 numero, asi que se saca
				poptemp = PilaO.pop()	#se saca el primer valor despues del @
				sizes2 = poptemp			#se guarda el primer valor como sizes2, por si la lista no esta vacia
				if (PilaO):				#si la lista no esta vacia
					poptemp = PilaO.pop()	#se saca el segundo valor 
					if(poptemp != '@'):		#se analiza el segundo valor, si no es @ se guarda como sizes1
						sizes1 = poptemp
					else:					#si es @ se devuelve a la lista
						sizes1 = sizes2		#sizes1 es igual a sizes2, porque ya sabems que no hay un segundo varsize
						sizes2 = None		#
						PilaO.append('@')  #se agrega un @ para que siempre quede un @ antes de un numero
				else:					#si la lista esta vacia, significa que es el ultimo elemento. 
					sizes1 = sizes2		#sizes1 es igual a sizes2, porque ya sabemos que no hay un segundo varsize
					sizes2 = None
			identificador = ids.dequeue()
			x.var = x.add_vars_to_dict(tipo,sizes1, sizes2)	#Se manda llamar el proceso de agregar variable al dict y lo guarda en el objeto
			#var_dict.update({identificador: x.var})
			var_brackList.append({identificador: x.var})
			local_bracketlist.append({identificador: x.var})
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
	#if p[1] == ',':
		#PilaO.append('@')

def p_varsize(p):
	'''VarSize : COR_I Exp COR_D
				| empty empty empty'''
	pass
	#if p[3] == ']':
	PilaO.append('@')

def p_tipo(p):
	'''Tipo : INT
			| FLOAT
			| CHAR
			| VOID'''
	pass
	vars_types.append(p[1])
	#print(vars_types)
	
def p_tipo2(p):
	'''Tipo2 : INT
			| FLOAT
			| CHAR
			| VOID'''
	pass
	procs_types.append(p[1])
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
				| LlamadaPersonaje PCOMA EstatutoA
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
	'''Asignacion : ID EXP_EQ Expresion '''
	#print("Variable: ")
	#print(p[1])
	#print("Var_brackelist actual: ")
	#print()
	if (vars_exists_in_list(p[1])):
		if(PilaO):
			operandoTEMPORAL = PilaO.pop()
			resultado_quadruple = add_quadruple(p[2], p[1], -1, operandoTEMPORAL, -1, 0) #se genera cuadruplos de asignacion
			PilaO.append(resultado_quadruple)
	else:
		print ('Variable "{0}" no se encuentra previamente definida'.format(p[1]))
		exit(1)			

def p_expresion(p):
	'''Expresion : Exp ExpresionA '''

def p_expresiona(p):
	'''ExpresionA : ExpresionB add_Exp
				  | empty'''

def p_expresionb(p):
	'''ExpresionB : EXP_GT Exp 
				  | EXP_LT Exp
				  | EXP_GEQ Exp
				  | EXP_LEQ Exp
			  	  | EXP_DEQ Exp
			  	  | EXP_NEQ Exp'''
	POper.append(p[1])

def p_add_Exp(p):
	'''add_Exp : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR in relational_operators): # Si el operador es relational_operators, se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un relational_operators


def p_exp(p):
	'''Exp : Termino Exp2 add_Term'''
	
def p_exp2(p):
	'''Exp2 : OP_PLUS Exp
			| OP_MIN Exp
			| empty empty '''
	if (p[1] == '+' or p[1] == '-'):
		POper.append(p[1]) #Se agrega el operador  suma/resta a la pila de operadores
		#print(POper)

def p_addTerm(p):
	'''add_Term : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR == '+' or tempOPERADOR == '-' ): # Si eloperador es "+" o "-", se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un "+" o "-"

def p_termino(p):
	'''Termino : Factor Termino2 add_Factor'''

def p_addFactor(p):
	'''add_Factor : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR == '*' or tempOPERADOR == '/' ): # Si eloperador es "*" o "/", se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un "*" o "/" 


def p_termino2(p):
	'''Termino2 : OP_MULT Termino
				| OP_DIV Termino
				| empty '''
	if (p[1] == '*' or p[1] == '/'):
		POper.append(p[1])	#Se agrega el operador multiplicacion/division a la pila de operadores
		#print(POper)

def p_factor(p):
	'''Factor : PAR_I Expresion PAR_D Factor3
			  | Factor2 VarCte
			  | Llamada empty
			  | ID Add_ID_TYPE '''
			  
def p_Add_ID_TYPE(p):
	'''Add_ID_TYPE :  empty'''
	#if (vars_exists_in_list(p[-1])):

	#else:
	#	print ('Procedimiento {0} ya existe en el diccionario'.format(p[2]))
	#	exit(1)
	tipo = vars_return_type(p[-1])
	PTipos.append(tipo)		

def p_factor2(p):
	'''Factor2 : OP_PLUS
			   | OP_MIN
			   | empty '''

def p_factor3(p):
	''' Factor3 : '''
	#quitar fondo falso
#	PilaO.pop()

def p_varcte(p): #truena en ID; por que?!
	'''VarCte : CTE_STRING Add_STRING_TYPE
			  |  CTE_I Add_INT_TYPE
			  |  CTE_F Add_FLOAT_TYPE
		  	  |  TRUE Add_BOOLT_TYPE
		  	  |  FALSE  Add_BOOLF_TYPE'''
	pass
	PilaO.append(p[1])
#	if  PTipos:
#		print (PTipos)
	

def p_Add_STRING_TYPE(p):
	'''Add_STRING_TYPE :  empty'''
	PTipos.append("string")

def p_addinttype(p):
	'''Add_INT_TYPE : '''
	PTipos.append("int")

def p_addfloattype(p):
	'''Add_FLOAT_TYPE : '''
	PTipos.append("float")

def p_addboolttype(p):
	'''Add_BOOLT_TYPE : '''
	PTipos.append("true")

def p_addboolftype(p):
	'''Add_BOOLF_TYPE : '''
	PTipos.append("false")

def p_condicion(p):
	'''Condicion : IF PAR_I Expresion PAR_D add_IF_1 Bloque CondicionA add_IF_3'''

def p_add_If_1(p):
	'''add_IF_1 : empty '''
	if(PTipos):
		tempTIPOS = PTipos.pop() #Se obtiene el tipo del tope de la lista de tipos
		if (tempTIPOS == 'bool' ): # Si el tipo es es booleano, se continua
			tempOPERAND1 = PilaO.pop()
			resultado_quadruple = add_quadruple('GOTOF', tempOPERAND1, -1, -1, -1, 0) #se genera cuadruplos
			PSaltos.append(resultado_quadruple -1) #se devuelve el operando a la pila de operadores
		else:
			print ('No se puede hacer la operacion con los tipos: {0} y {1}'.format(tempTIPOS, 'bool'))
			exit(1)

def p_condiciona(p):
	'''CondicionA : ELSE add_IF_2 Bloque
				  | empty '''

def p_add_if_2(p):
	'''add_IF_2 : empty '''
	if (PSaltos):
		resultado_quadruple = add_quadruple('GOTO', -1, -1, -1, -1, 0) #se genera cuadruplos GOTO, no tiene operandos nulos y una casilla vacia
		rellenar_cuadruplo(PSaltos.pop())
		PSaltos.append(resultado_quadruple -1)  # metemos el contador -1 a la pila de psaltos

def p_add_if_3(p):
	'''add_IF_3 : empty '''
	if (PSaltos):
		rellenar_cuadruplo(PSaltos.pop())  # Sesaca el fin de PSaltos y luego se rellena con cont

def p_escritura(p):
	'''Escritura : OUTPUT PAR_I Escritura2 '''

def p_escritura2(p):
	'''Escritura2 :  ID add_Escritura Escritura3
				  |  CTE_STRING add_Escritura Escritura3'''

def p_escritura3(p):
	'''Escritura3 : PAR_D
				  | COMA Escritura2'''

def p_add_Escritura(p):
	'''add_Escritura : empty'''
	PilaO.append(p[-1])				# Se otiene el ID directamente y se manda a la pila
	operandoTEMPORAL = PilaO.pop()  # Se obtiene operando y se genera el cuadruplo
	#print(operandoTEMPORAL)
	add_quadruple('OUTPUT', operandoTEMPORAL, -1, -1, -1, 0) #se genera cuadruplos OUTPUT

def p_lectura(p):
	'''Lectura : INPUT PAR_I LecturaA PAR_D '''

def p_lecturaa(p):
	'''LecturaA : ID add_Lectura1 LecturaA
				| empty '''

def p_add_Lectura1(p):
	'''add_Lectura1 :  empty'''
	PilaO.append(p[-1])				# Se otiene el ID directamente y se manda a la pila
	operandoTEMPORAL = PilaO.pop()  # Se obtiene operando y se genera el cuadruplo
	#print(operandoTEMPORAL)
	add_quadruple('INPUT', operandoTEMPORAL, -1, -1, -1, 0) #se genera cuadruplos INPUT

def p_funcion(p):
	'''Funcion : FUNCTION Tipo2 ID FuncionA'''
	pass
	local_bracketlist = []
	x.current_fid = p[3]
	if x.current_fid in x.procs.keys():
		print ('Procedimiento "{0}" esta duplicdo y ya existe en el diccionario.'.format(p[3]))
		exit(1)
	else:
		#p.pprint(x.procs)
		tipo = procs_types.pop()	#Se saca el tipo de procedimiento de la lista de tipos
		#var_dict = var_brackList.pop()
		var_dict = {}
		#for c in range(len(var_brackList)):
		#	var_dict.update(var_brackList.pop())
		var_dummyBrackList = var_brackList
		for c in var_dummyBrackList:
			z = var_brackList.pop()
			if z == '@':
				break
			else:
				var_dict.update(z)
		x.procs.update(x.add_procs_to_dict(p[3],tipo, 'void', var_dict)) #se actualiza el diccionario de procedimientos
		var_dict = {}
		#print(var_dict)
		#pp.pprint(var_dict)
		#pp.pprint(x.procs)

	
def p_funciona(p):
	'''FuncionA : PAR_I Params3 Params PAR_D  Bloque'''
	#print(var_brackList)
	
def p_params3(p):
	'''Params3 : empty '''
	var_brackList.append('@') # Se anade un delimitador al principio de cada funcion, para saber que parametros
	
def p_params(p):
	'''Params : Tipo ID Params2
			   | empty empty empty '''
	if(p[2] != None):
		if (vars_exists_in_list(p[2])):
		#if p[1] in var_brackList.keys():
			vars_types.pop()
			print ('Variable "{0}" ya existe en el diccionario'.format(p[2]))
			exit(1)
		else:
			ids.enqueue(p[2])
			#print(var_types)
			if ids.size() > 0:	#Si encuentra que existe un id, significa que hay que agregarlo a la tabla de variables
				#print(vars_types)
				tipo = vars_types.pop()	#obtiene el tipo de la lista de de tipos
				identificador = ids.dequeue()
				x.var = x.add_vars_to_dict(tipo,None, None)	#Se manda llamar el proceso de agregar variable al dict y lo guarda en el objeto
				#print(identificador)
				#var_dict.update({p[2]: x.var})
				var_brackList.append({p[2]: x.var})

def p_params2(p):
	'''Params2 : COMA Params
			   | empty empty '''

def p_llamada(p):
	'''Llamada : ID PAR_I Llamada2 PAR_D  '''

def p_llamada2(p):
	'''Llamada2 : Expresion Llamada3
				| empty '''

def p_llamada3(p):
	'''Llamada3 : COMA Expresion Llamada3
			 	| empty '''

def p_character(p):
	''' Character : PERSONAJE ID LLAVE_I CharacterA Archetype Estatuto2 LLAVE_D '''

def p_charactera(p):
	''' CharacterA : FVarsAsignacion 
			| empty '''

def p_llamadaPersonaje(p):
	'''LlamadaPersonaje : ID PAR_I LlamadaPersonaje2 PAR_D  '''

def p_llamadaPersonaje2(p):
	'''LlamadaPersonaje2 : Expresion LlamadaPersonaje3
				| empty '''

def p_llamadaPersonaje3(p):
	'''LlamadaPersonaje3 : COMA Expresion LlamadaPersonaje3
			 	| empty '''

def p_regresa(p):
	''' Regresa : RETURN Regresa2 add_Regresa'''

def p_regresa2(p):
	''' Regresa2 : Expresion empty
				 | ID add_ID '''

def p_add_ID(p):
	''' add_ID : empty'''
	PilaO.append(p[-1])

def p_add_Regresa(p):
	''' add_Regresa : empty '''
	if(PilaO):
		tipoTEMPORAL = PTipos.pop()
		operandoTEMPORAL = PilaO.pop()
		#print(operandoTEMPORAL)
		add_quadruple('RETURN', operandoTEMPORAL, -1, -1, -1, 0) #se genera cuadruplos REGRESA

def p_loopwhile(p):
	''' LoopWhile : WHILE add_While_1 PAR_I Expresion PAR_D add_While_2 Bloque add_While_3 '''
	
def p_add_While_1(p):
	'''add_While_1 : empty '''
	PSaltos.append(get_count_cuadruplos())  # meter cont en PSaltos
	
def p_add_While_2(p):
	'''add_While_2 : empty '''
	aux = PTipos.pop()
	if aux == 'true' or aux == 'false' or aux == 'bool':
		tempOPERAND = PilaO.pop()
		resultado_quadruple = add_quadruple('GOTOF', tempOPERAND, -1, -1, -1, 0) #se genera cuadruplos
		PSaltos.append(resultado_quadruple - 1)
	else:
		#tronarlo
		print ('No se puede hacer la operacion con los tipos: {0} y {1}'.format(aux, 'bool'))
		exit(1)

def p_add_While_3(p):
	'''add_While_3 : empty '''
	if (PSaltos):
		falso = PSaltos.pop()
		retorno = PSaltos.pop()
		add_quadruple('GOTO', retorno, -1, -1, -1, 0) #se genera cuadruplos GOTO, no tiene operandos nulos y una casilla vacia
		rellenar_cuadruplo(falso)
	#PSaltos.append(get_count_cuadruplos)  # meter cont en PSaltos

			
#def p_loopfor(p):
#	''' LoopFor : FOR PAR_I Asignacion PCOMA Expresion add_For_1 PCOMA Expresion add_For_2 PAR_D Bloque add_For_3 '''
def p_loopfor(p):
#	''' LoopFor : FOR PAR_I Asignacion PCOMA Expresion PCOMA Expresion PAR_D Bloque '''
	''' LoopFor : FOR ID add_For_1 EXP_EQ Expresion add_For_2 TO Expresion add_For_3 DO Bloque add_For_4 '''
	
	

def p_add_For_1(p):
	'''add_For_1 : empty '''
	#PilaO.append(p[-1])  # Guardar el identificador (direccion) en pila de Operandos (PilaO), verificar semantica

def p_add_For_2(p):
	'''add_For_2 : empty '''

def p_add_For_3(p):
	'''add_For_3 : empty '''

def p_add_For_4(p):
	'''add_For_4 : empty '''


def p_fvarasignacion(p):
	''' FVarsAsignacion : LIFE EXP_EQ Exp FVarsAsignacionA
						| STUN EXP_EQ Exp FVarsAsignacionA
						| TIME EXP_EQ Exp FVarsAsignacionA '''

def p_fvarasignaciona(p):
	''' FVarsAsignacionA : FVarsAsignacion 
						 | empty'''

def p_archetype(p):
	''' Archetype : TYPE EXP_EQ ArchetypeA '''

def p_archetypea(p):
	''' ArchetypeA : SHOTO COMANDOS EXP_EQ Scomando
			   	   | GRAPPLER COMANDOS EXP_EQ Gcomando
				   | CHARGE COMANDOS EXP_EQ Ccomando '''

def p_scomando(p):
	''' Scomando : STANDING ScomandoA '''

def p_scomandoa(p):
	''' ScomandoA : Estado ScomandoA
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

def vars_exists_in_list(v_id):
	#print (v_id)
	#print(var_brackList) for key in var_bracklist[v_id]
	for y in var_brackList:
		#if y == v_id:
		if v_id in y:
			#print(y)
			return True

def vars_return_type(v_id):
	#print("si imprimio")
	#print (v_id)
	for y in var_brackList:
		#print (y [ v_id ][ 'Tipo' ])
		#if y == v_id:
		#print (y)
		if v_id in y:
			return y[v_id]['Tipo']

def operacion_cuadruplos(tempOPERADOR): 
    tempTIPO2 = PTipos.pop()
    tempTIPO1 = PTipos.pop()
    if tempOPERADOR in relational_operators:
    	tempOPERADOR = 'comp'
    elif tempOPERADOR in logical_operators:
    	tempOPERADOR = 'log'
    resultadoTIPO = check_operation(tempTIPO1,tempOPERADOR,tempTIPO2) # Se manda llamar el cubo semantico
    if (resultadoTIPO != 'error'): 
        tempOPERAND2 = PilaO.pop()
        tempOPERAND1 =  PilaO.pop()
        resultado_quadruple = add_quadruple(tempOPERADOR, tempOPERAND1, tempTIPO1, tempOPERAND2, tempTIPO2, 0) #se genera cuadruplos
        PilaO.append(resultado_quadruple)	#se devuelve el operando a la pila de operadores
        PTipos.append(resultadoTIPO)		#se devuelve el tipo a la pila de tipos
    else:
        #tronarlo
        print ('No se puede hacer la operacion con los tipos: {0}, {1}, {2}'.format(tempTIPO1, tempOPERADOR, tempTIPO2))
        exit(1)


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