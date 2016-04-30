# Proyecto compilador Python
# PLY de Fight Compilers 2016
# Parte Yacc
# Hecho por Jaime Neri y Mike Grimaldo
#!env/bin/python

import ply.yacc as yacc
import sys
import pprint
import FightCompilersLex
#import FightCompilersSemantics
from FightCompilersSemantics import Semantics, semantics_cube
from Queue import Queue
from quadruples import add_quadruple, check_operation, relational_operators, logical_operators, ignored_checks, get_count_cuadruplos, rellenar_cuadruplo, get_cuadruplos
from MemoryBlock import MemoryBlock

# memory allocation (just variable counters representing: constants and local/global vars)
mem_local        = MemoryBlock(0, 1000, 2000, 3000, 4000, 5000)
mem_global       = MemoryBlock(5000, 6000, 7000, 8000, 9000, 10000)
mem_constants    = MemoryBlock(10000, 11000, 12000, 13000, 14000, 15000)
mem_temps        = MemoryBlock(15000, 16000, 17000, 18000, 19000, 20000)
mem_global_temps = MemoryBlock(20000, 21000, 22000, 23000, 24000, 25000)

#bools, ints, floats, chars, strings, limit
memory_dict = {
        'local':       [0, 		1000, 2000,   3000,  4000,  5000],
        'global':      [5000, 	6000, 7000,   8000,  9000, 10000],
        'constants':   [10000, 11000, 12000, 13000, 14000, 15000],
        'temp':        [15000, 16000, 17000, 18000, 19000, 20000],
        'temp_global': [20000, 21000, 22000, 23000, 24000, 25000]
}

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

funcion_id = []
var_brackList = []  #Lista que tienen los diccionarios de variables
proc_brackList = []  #Lista que tienen los diccionarios de procedimientos

contador_parametros = [0] #contador que guarda el numero de parametros por funcion
contador_varsGlobales = [0] #contador que guarda el numero de variables globales
contador_k = [1]


directorio_Activo = {  #Lista que tienen los diccionarios de variables
	'global' : {},
	'local'  : {}
}

PilaO = [] #Pila de operandos '5'
POper = [] #Pila de operadores '+' '-' '*' '/'
PTipos = [] #Pila que guarda los tipos e operandos
PSaltos = [] #Pila que guarda los saltos pendientes para la funcion rellenar_Cuadruplo

# Parsing Rules
def p_juego(p):
	'''Juego : JUEGO ID add_Juego_1 DOSP JuegoA add_Juego_2 JuegoB MainProgram'''
	#pp.pprint(get_cuadruplos())

def p_add_Juego_1(p):
	'''add_Juego_1 : empty'''
	if p[-1] in x.procs.keys():  #se verifica la semantica
		print ('<---[REPEATED_FUNC_DECLARATION][Juego]; Procedimiento "{0}" ya existe en el diccionario--->'.format(p[2]))
		exit(1)
	else:
		proc_brackList.append(p[-1])
		
		x.procs.update(x.add_procs_to_dict(p[-1],p[-2], 0, 10000, {})) #Se da de alta el nombre del procedimiento
		count = contador_varsGlobales.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
		contador_varsGlobales.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
		x.procs.update(x.add_procs_to_dict(p[-1],p[-2], count, 10000, var_dict))
		directorio_Activo['global'] = x.procs
		#print(diectorio_Activo['global'])
		
		#pp.pprint(get_cuadruplos())

def p_juegoa(p):
	'''JuegoA : Vars JuegoA
		      | empty'''

def p_juegob(p):
	'''JuegoB : Funcion JuegoB 
			  | Character JuegoB 
			  | empty'''

def p_add_Juego_2(p):
	'''add_Juego_2 : empty'''
	resultado_quadruple = add_quadruple('GOTO', -1, -1, -1, -1, 0) #se genera cuadruplos GOTO, no tiene operandos nulos y una casilla vacia
	PSaltos.append(resultado_quadruple -1)  # metemos el contador -1 a la pila de psaltos
	count = contador_varsGlobales.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
	contador_varsGlobales.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
	var = proc_brackList.pop()
	#print(var_brackList)
	#proc_brackList.append(var)
	directorio_Activo['global'][var]['#Params'] = count	#Se actualiza la funcion con su numero de parametros
	directorio_Activo['global'][var]['Var_Table'].update(var_brackList.pop())	#Se actualiza la funcion con su numero de parametros
	pp.pprint(x.procs)


def p_add_Vars2_1(p):
	'''add_Vars2_1 : empty'''
	if (vars_exists_in_list(p[-1])):
		print ('<---[REPEATED_DECLARATION][Vars]; Variable "{0}" ya existe en el diccionario--->'.format(p[1]))
		exit(1)	
	else:
		PilaO.append(p[-1])
		x.var = x.add_vars_to_dict(p[-1],0, 0)	#Se manda llamar el proceso de agregar variable al dict y lo guarda en el objeto
		

def p_add_Vars2_2(p):
	'''add_Vars2_2 : empty'''
	if (PilaO):
		#print(PilaO)
		size1 = PilaO.pop()
		var_id = PilaO.pop()
		PilaO.append(var_id)
		temp = directorio_Activo['global'].values().pop()
		temp['Var_Table'] = {var_id : {'Size_1': size1, 'Size_2': 0, 'Tipo': 0}}
		#print(temp) 	#Se actualiza la funcion con su numero de parametros
		#print(x.procs) 	#Se actualiza la funcion con su numero de parametros
			print(PilaO)

def p_vars(p):
	'''Vars : VAR Vars2 PCOMA'''

def p_vars2(p):
	'''Vars2 : ID add_Vars2_1 COR_I Exp add_Vars2_2 COR_D VarSize DOSP Tipo Vars3 '''
	#print(var_brackList.keys())
	if (vars_exists_in_list(p[1])):
	#if p[1] in var_brackList.keys():
		vars_types.pop()
		#vars_values.pop()
		#['4', '@', 5, '@']                                                                                                         
		poptemp = PilaO.pop() 
		if (poptemp != "@") and not PilaO:	#Si existe mas de 1 elemento en la lista de tamano de variables obtiene 2 elementos
			poptemp = PilaO.pop()
		print ('<---[REPEATED_DECLARATION][Vars]; Variable "{0}" ya existe en el diccionario--->'.format(p[1]))
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
			count = contador_varsGlobales.pop()  #se obtiene el contador actual de la lista
			contador_varsGlobales.append(count +1)	# se suma 1 ya que se agrego una variable
			var_brackList.append({identificador: x.var})
			#print("estoy en vars")
			#print(var_brackList)


def p_vars3(p):
	'''Vars3 : COMA Vars2
			| empty'''
	pass
	#if p[1] == ',':
		#PilaO.append('@')

def p_varsize(p):
	'''VarSize : COR_I Exp add_Vars2_3 COR_D
				| empty'''
	pass
	#if p[3] == ']':
	PilaO.append('@')

def p_add_Vars2_3(p):
	'''add_Vars2_3 : empty'''
	print(PilaO)
	if (PilaO):
		print(PilaO)
		size2 = PilaO.pop()
		temp = directorio_Activo['global'].values().pop()
		#temp['Var_Table'] = {var_id : {'Size_2': size2}}
		#print(temp) 	#Se actualiza la funcion con su numero de parametros
		#print(x.procs) 	#Se actualiza la funcion con su numero de parametros

def p_tipo(p):
	'''Tipo : INT
			| FLOAT
			| CHAR
			| BOOL'''
	pass
	vars_types.append(p[1])
	#print(vars_types)
	
def p_tipo2(p):
	'''Tipo2 : INT
			| FLOAT
			| CHAR
			| BOOL
			| VOID'''
	pass
	procs_types.append(p[1])
	#print(vars_types)

def p_mainprogram(p):
	'''MainProgram : MAIN PAR_I PAR_D add_Main_1 Bloque add_Main_2'''

def p_add_Main_1(p):		#funcion que se encarga de rellenar el primer GOTO de los cuadruplos. Se salta las funciones.
	'''add_Main_1 : empty'''
	if(PSaltos):
		retorno = PSaltos.pop() #obtiene el valor de PSaltos mas auntiguo 
		rellenar_cuadruplo(retorno)  #rellena el primer cuadruplo con ese valor

def p_add_Main_2(p):
	'''add_Main_2 : empty'''
	add_quadruple('END', -1, -1, -1, -1, 0) #se genera cuadrplo de fin de programa
 
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
	'''Asignacion : ID add_Asignacion_1 EXP_EQ add_Asignacion_2 Expresion add_Asignacion_3 '''
	#print("Variable: ")
	#print(p[1])
	#print("Var_brackelist actual: ")
	#print()
	# if (vars_exists_in_list(p[1])):
	# 	if(PilaO):
	# 		operandoTEMPORAL = PilaO.pop()
	# 		resultado_quadruple = add_quadruple(p[2], p[1], -1, operandoTEMPORAL, -1, 0) #se genera cuadruplos de asignacion
	# 		PilaO.append(resultado_quadruple)
	# else:
	# 	print ('<---[UNDECLARED_VARIABLE][Asignacion]; Variable "{0}" no se encuentra previamente definida--->'.format(p[1]))
	# 	exit(1)	


def p_add_Asignacion_1(p):
	'''add_Asignacion_1 : empty '''
	PilaO.append(p[-1])
	
def p_add_Asignacion_2(p):
	'''add_Asignacion_2 : empty '''
	POper.append(p[-1])
	
def p_add_Asignacion_3(p):
	'''add_Asignacion_3 : empty '''
	if(PilaO):
		operadorDerecho = PilaO.pop()
		operadorIzquierdo = PilaO.pop()
		PilaO.append(operadorIzquierdo)
		PilaO.append(operadorDerecho)
		operadorAsigna = POper.pop()
		#tipoDerecho = PilaO.pop()
		#print('Lado izquierdo "{0}" operador "{1}" Lado derecho "{2}"'.format(operadorIzquierdo, operadorIgual, operadorDerecho))
		print('Lado izquierdo "{0}" Lado derecho "{1}"'.format(operadorIzquierdo, operadorDerecho))
		if (vars_exists_in_list(operadorIzquierdo)):
			operacion_cuadruplos(operadorAsigna)
			# if(PilaO):
			# 	#operandoTEMPORAL = PilaO.pop()
			# 	resultado_quadruple = add_quadruple(operadorIgual, operadorIgual, -1, opeandoDerecho, -1, 0) #se genera cuadruplos de asignacion
			# 	PilaO.append(resultado_quadruple)
			# else:
			# 	print("fallo aqui")
		else:
			print ('<---[UNDECLARED_VARIABLE][Asignacion]; Variable "{0}" no se encuentra previamente definida--->'.format(p[1]))
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
			  | ID add_ID_TYPE_1  '''
			  

def p_add_ID_TYPE_1(p):
	'''add_ID_TYPE_1 :  empty'''
	#if (vars_exists_in_list(p[-1])):
	#else:
	#	print ('Procedimiento {0} ya existe en el diccionario'.format(p[2]))
	#	exit(1)
	tipo = vars_return_type(p[-1])
	PTipos.append(tipo)
	PilaO.append(p[-1])
	#print(PilaO)

def p_factor2(p):
	'''Factor2 : OP_PLUS
			   | OP_MIN
			   | empty '''

def p_factor3(p):
	''' Factor3 : '''
	#quitar fondo falso
#	PilaO.pop()

def p_varcte(p): 
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
	PTipos.append("bool")

def p_addboolftype(p):
	'''Add_BOOLF_TYPE : '''
	PTipos.append("bool")

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
			#print("Si llego a: ")
			#print(resultado_quadruple)
		else:
			print ('<---ERROR_TYPE_MISMATCH[IF]; No se puede hacer la operacion con los tipos: "{0}" y "{1}"--->'.format(tempTIPOS, 'bool'))
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
	'''Funcion : FUNCTION Tipo2 ID add_Funcion_1 FuncionA add_Funcion_2'''


	
def p_funciona(p):
	'''FuncionA : PAR_I Params3 Params PAR_D  Bloque'''
	#print(var_brackList)
	
def p_add_Funcion_1(p):
	'''add_Funcion_1 : empty'''
	proc_brackList.append(p[-1])
	x.current_fid = p[-1]
	if x.current_fid in x.procs.keys():
		print ('<---[REPEATED_FUNC_DECLARATION][Funcion]; Procedimiento "{0}" esta duplicdo y ya existe en el diccionario--->'.format(p[3]))
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
		count = contador_parametros.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
		contador_parametros.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
		x.procs.update(x.add_procs_to_dict(p[-1],tipo, count, 11000, var_dict)) #se actualiza el diccionario de procedimientos
		var_dict = {}
		#print(var_dict)
		#pp.pprint(var_dict)
		#pp.pprint(x.procs)	
	
def p_add_Funcion_2(p):
	'''add_Funcion_2 : empty'''
	add_quadruple('ENDPROC', -1, -1, -1, -1, 0) #se genera cuadrplo de fin de programa

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
			print ('<---[REPEATED_DECLARATION][Params]; Variable "{0}" ya existe en el diccionario--->'.format(p[2]))
			exit(1)
		else:
			cont = contador_parametros.pop()
			contador_parametros.append(cont +1)
			ids.enqueue(p[2])
			#print(var_types)
			if ids.size() > 0:	#Si encuentra que existe un id, significa que hay que agregarlo a la tabla de variables
				#print(vars_types)
				tipo = vars_types.pop()	#obtiene el tipo de la lista de de tipos
				#print(tipo)
				identificador = ids.dequeue()
				x.var = x.add_vars_to_dict(tipo,1, 1)	#Se manda llamar el proceso de agregar variable al dict y lo guarda en el objeto
				var_brackList.append({p[2]: x.var})

def p_params2(p):
	'''Params2 : COMA Params
			   | empty empty '''

def p_llamada(p):
	'''Llamada : ID add_Llamada_1 add_Llamada_2 PAR_I Llamada2 PAR_D add_Llamada_5 '''
	# x(2);

def p_llamada2(p):
	'''Llamada2 : Expresion add_Llamada_3 Llamada3
				| empty '''

def p_llamada3(p):
	'''Llamada3 : COMA add_Llamada_4 Llamada2
			 	| empty '''
			 	
def p_add_Llamada_1(p):
	'''add_Llamada_2 : empty '''
	#global contador_parametros
	print("Nombre funcion")
	print(p[-2])
	if (proc_exists_in_list(p[-2])):
		#print(p[-2])
		add_quadruple('ERA', p[-2], -1, -1, -1)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
		contador_k = [0]  # Se inicializa el contador k en 1		
	else:
		print ('<---[UNDECLARED_FUNCTION][Llamada]; Procedimiento "{0}" no se encuentra previamente declarado--->'.format(p[-2]))
		exit(1)

def p_add_Llamada_2(p):
	'''add_Llamada_1 : empty '''
	funcion_id.append(p[-1])

def p_add_Llamada_3(p):
	'''add_Llamada_3 : empty '''
	valor_argumento = PilaO.pop()
	tipo_argumento = PTipos.pop()
	nombre_funcion = funcion_id.pop()
	funcion_id.append(nombre_funcion)
	#print(funcion_id)
	count = contador_k.pop()
	#print(count)
	tipo2 = obtain_type_from_dictionary(nombre_funcion, count)
	#print("El tipo1: "+tipo_argumento)
	#print("El tipo2: "+tipo2)
	#print(tipo_argumento)
	if(tipo_argumento == tipo2):
		resultado_quadruple = add_quadruple('PARAMETER', valor_argumento, -1, ('Param' + str(count)), -1)  #Se genera el cuadruplo PARAMETER, tiene el k-esimo argumento
		contador_k.append(count)
		PilaO.append(resultado_quadruple)
	else:
		print ('<---[ERROR_TYPE_MISMATCH][Llamada]; No se puede hacer la operacion con los tipos: "{0}" y "{1}"--->'.format(tipo2, tipo_argumento))
		exit(1)

def p_add_Llamada_4(p):
	'''add_Llamada_4 : empty '''
	count = contador_k.pop()
	contador_k.append(count+1)

def p_add_Llamada_5(p):
	'''add_Llamada_5 : empty '''
	#global contador_parametros
	contador_k = []
	nombre_funcion = funcion_id.pop()
	add_quadruple('GOSUB', nombre_funcion, -1, -1, -1)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido


		
def p_character(p):
	''' Character : PERSONAJE ID LLAVE_I CharacterA Archetype Estatuto2 LLAVE_D '''
	# pass
	# proc_brackList.append(p[2])
	# x.current_fid = p[2]
	# if x.current_fid in x.procs.keys():
	# 	print ('Procedimiento "{0}" esta duplicdo y ya existe en el diccionario.'.format(p[3]))
	# 	exit(1)
	# else:
	# 	#p.pprint(x.procs)
	# 	tipo = procs_types.pop()	#Se saca el tipo de procedimiento de la lista de tipos
	# 	#var_dict = var_brackList.pop()
	# 	var_dict = {}
	# 	#for c in range(len(var_brackList)):
	# 	#	var_dict.update(var_brackList.pop())
	# 	var_dummyBrackList = var_brackList
	# 	for c in var_dummyBrackList:
	# 		z = var_brackList.pop()
	# 		if z == '@':
	# 			break
	# 		else:
	# 			var_dict.update(z)
	# 	count = contador_parametros.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
	# 	contador_parametros.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
	# 	x.procs.update(x.add_procs_to_dict(p[3],tipo, count, var_dict)) #se actualiza el diccionario de procedimientos
	# 	var_dict = {}

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
		print ('<---[ERROR_TYPE_MISMATCH][While]; No se puede hacer la operacion con los tipos: "{0}" y "{1}"--->}'.format(aux, 'bool'))
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
# 	auxExp1 = PilaO.pop()
# 	auxID = PilaO.pop()
# 	PilaO.append(auxID)
# 	add_quadruple('=', auxID, -1, auxExp1, -1, 0)

def p_add_For_3(p):
	'''add_For_3 : empty '''
# 	#obtener variable temporal Tf
# 	auxExp2 = PilaO.pop()
# 	#obtener otra variable temporal Tx
# 	add_quadruple('=', Tf, -1, auxExp2, -1, 0)
# 	add_quadruple('<=', auxID, -1, auxExp1, -1, 0)

	

def p_add_For_4(p):
	'''add_For_4 : empty '''
	


def p_fvarasignacion(p):
	''' FVarsAsignacion : LIFE EXP_EQ Exp add_CharVar PCOMA FVarsAsignacionA
						| STUN EXP_EQ Exp add_CharVar PCOMA FVarsAsignacionA
						| TIME EXP_EQ Exp add_CharVar PCOMA FVarsAsignacionA '''

def p_add_CharVar(p):
	''' add_CharVar : empty  '''
	#print(p[-3])
	if (PilaO):
		if (p[-3] == 'life' or p[-3] == 'stun' or p[-3] == 'time'):
			operandoTEMPORAL = PilaO.pop()
			resultado_quadruple = add_quadruple(p[-2], p[-3], -1, operandoTEMPORAL, -1, 0) #se genera cuadruplos de asignacion
			PilaO.append(resultado_quadruple)
		else:
			print ('<---[UNDECLARED_VARIABLE][PersonajeVars]; Variable "{0}" no se encuentra previamente definida-->'.format(p[-3]))
			exit(1)


def p_fvarasignaciona(p):
	''' FVarsAsignacionA : FVarsAsignacion 
						 | empty'''

def p_archetype(p):
	''' Archetype : TYPE EXP_EQ ArchetypeA '''

def p_archetypea(p):
	''' ArchetypeA : SHOTO PCOMA COMANDOS EXP_EQ Scomando
			   	   | GRAPPLER PCOMA COMANDOS EXP_EQ Gcomando
				   | CHARGE PCOMA COMANDOS EXP_EQ Ccomando '''

def p_scomando(p):
	''' Scomando : STANDING ScomandoA PCOMA '''

def p_scomandoa(p):
	''' ScomandoA : Estado ScomandoA
			| Attack ScomandoA
			| Sespecial ScomandoA
			| empty '''

def p_gcomando(p):
	''' Gcomando : STANDING GcomandoA PCOMA '''

def p_gcomandoa(p):
 	''' GcomandoA :   Estado GcomandoA
			| Attack GcomandoA
			| Gespecial GcomandoA
			| empty '''

def p_ccomando(p):
	''' Ccomando : STANDING CcomandoA PCOMA '''

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
	
def obtain_type_from_dictionary(id_funcion, indice):
	#print("imprime indice: ")
	#pp.pprint(x.procs)
	param_length = x.procs[id_funcion]['#Params']	#Revise que no se manden mas parametros en una llamada de lo que la funcion puede recibir
	if(param_length >= indice):
		return x.procs[id_funcion]['Var_Table'].values()[indice-1]['Tipo']  #Busca en la tabla de variables del procedimiento "id_funcion" el tipo segun su "indice"
	else:
		print ('<---[PARAMETER_LENGTH_MISMATCH][Llamada]; La funcion esperaba "{0}" parametros y recibio "{1}" parametros--->'.format(param_length, indice))
		exit(1)
		
def proc_exists_in_list(v_id):
	for y in proc_brackList:
		if v_id in y:
			#print("entro")
			return True
			
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
	operador = tempOPERADOR
	tempTIPO2 = PTipos.pop()
	tempTIPO1 = PTipos.pop()
	if tempOPERADOR in relational_operators:
		tempOPERADOR = 'comp'
	elif tempOPERADOR in logical_operators:
		tempOPERADOR = 'log'
	resultadoTIPO = check_operation(tempTIPO1,tempOPERADOR,tempTIPO2) # Se manda llamar el cubo semantico
	if (resultadoTIPO != 'error'): 
		tempOPERAND2 = PilaO.pop()
		#print('Operando2: "{0}"'.format(resultadoTIPO))
		#pp.pprint(get_cuadruplos())

		tempOPERAND1 =  PilaO.pop()
		#print('Operando1: "{0}"'.format(tempOPERAND1))
		resultado_quadruple = add_quadruple(operador, tempOPERAND1, tempTIPO1, tempOPERAND2, tempTIPO2, 0) #se genera cuadruplos
		PilaO.append(resultado_quadruple)	#se devuelve el operando a la pila de operadores
		PTipos.append(resultadoTIPO)		#se devuelve el tipo a la pila de tipos
	else:
	    #tronarlo
	    print ('<---[ERROR_TYPE_MISMATCH][Expresion]; No se puede hacer la operacion con los tipos: {0}, {1}, {2}--->'.format(tempTIPO1, tempOPERADOR, tempTIPO2))
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
  #  p[0] = p[1] + p