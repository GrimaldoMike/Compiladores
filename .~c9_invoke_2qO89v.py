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
contador_k = [0]


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
	pp.pprint(get_cuadruplos())
	#pp.pprint(x.procsGlobal)
	#pp.pprint(x.procsLocal)
	aux = get_cuadruplos()
	print (aux[0][0])
	# print(".................")

def p_add_Juego_1(p):
	'''add_Juego_1 : empty'''
	if p[-1] in x.procsGlobal.keys():  #se verifica la semantica
		print ('<---[REPEATED_FUNC_DECLARATION][Juego]; Procedimiento "{0}" ya existe en el diccionario--->'.format(p[2]))
		exit(1)
	else:
		proc_brackList.append(p[-1])	#Se agrega el nombre de la funcion a la lista para despues usar el nombre y actualizar sus parametros
		#x.procs.update(x.add_procs_to_dict(p[-1],p[-2], 0, 10000, {})) #Se da de alta el nombre del procedimiento
		count = contador_varsGlobales.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
		contador_varsGlobales.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
		x.procsGlobal.update(x.add_procs_to_dict(p[-1],p[-2], count, 10000, var_dict))
		directorio_Activo['global'] = x.procsGlobal
		#print(diectorio_Activo['global'])
		

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
	var = proc_brackList.pop() #Se obtiene el nombre de la funcion actual
	directorio_Activo['global'][var]['#Params'] = count	#Se actualiza la funcion con su numero de parametros

def p_vars(p):
	'''Vars : VAR Vars2 PCOMA'''

def p_vars2(p):
	'''Vars2 : ID add_Vars2_1 COR_I Exp add_Vars2_2 COR_D VarSize DOSP Tipo add_Vars2_4 Vars3 '''

def p_vars3(p):
	'''Vars3 : COMA Vars2
			| empty'''

def p_varsize(p):
	'''VarSize : COR_I Exp add_Vars2_3 COR_D
				| empty'''

def p_add_Vars2_1(p):
	'''add_Vars2_1 : empty'''
	if (vars_exists_in_list(p[-1])):
		print ('<---[REPEATED_DECLARATION][Vars]; Variable "{0}" ya existe en el diccionario--->'.format(p[1]))
		exit(1)	
	else:
		temp = directorio_Activo['global'].values().pop()
		temp['Var_Table'].update({p[-1] : {'Size_1': 0, 'Size_2': 0, 'Tipo': 0, 'DireccionInicio': 2000}})
		#pp.pprint(directorio_Activo)
		count = contador_varsGlobales.pop()  #se obtiene el contador actual de la lista
		contador_varsGlobales.append(count +1)	# se suma 1 ya que se agrego una variable
		var_brackList.append(p[-1])  # Se agrega la variable a bracketlist para usarse despues al agregar su size1
		#print(var_brackList)
		
def p_add_Vars2_2(p):
	'''add_Vars2_2 : empty'''
	if (PilaO):
		#print(PilaO)
		var_id = var_brackList.pop()	 # Se obtiene la variable de var_bracketlist para agregar su size1
		size1 = PilaO.pop()
		if(int(size1) > 0): #Se verifica que el tamano de la variable sea mayor a 0
			#PilaO.append(var_id)
			temp = directorio_Activo['global'].values().pop()
			temp['Var_Table'][var_id]['Size_1'] = size1 #Se el tamano de la variable size_1
			var_brackList.append(var_id)	 # Se agrega la variable a bracketlist para usarse despues al agregar su size2
		else:
			print ('<---[VARIABLE_SIZE][Vars]; Variable "{0}" debe tener un tamano mayor a 0--->'.format(p[-1]))
			exit(1)

def p_add_Vars2_3(p):
	'''add_Vars2_3 : empty'''
	if (PilaO):
		#print(PilaO)
		var_id = var_brackList.pop()	 # Se obtiene la variable de var_bracketlist para agregar su size2
		size2 = PilaO.pop()
		if(int(size2) > 0): #Se verifica que el tamano de la variable sea mayor a 0
			temp = directorio_Activo['global'].values().pop()
			temp['Var_Table'][var_id]['Size_2'] = size2 #Se el tamano de la variable size_2
			var_brackList.append(var_id) #Se agrega el id de la variable para que la use la regla Tipo
		else:
			print ('<---[VARIABLE_SIZE][Vars]; Variable "{0}" debe tener un tamano mayor a 0--->'.format(p[-1]))
			exit(1)

def p_add_Vars2_4(p):
	'''add_Vars2_4 : empty'''
	var_id = var_brackList.pop()	 # Se obtiene la variable de var_bracketlist para agregar su size2
	tipo = vars_types.pop()
	if(tipo in ['int', 'float', 'char', 'bool' ]): 	#Se verifica un tipo de variable correcto
		temp = directorio_Activo['global'].values().pop()
		temp['Var_Table'][var_id]['Tipo'] = tipo  #Se agrega el Tipo de variable al directorio de variables

	else:
		print ('<---[VARIABLE_TYPE][Vars]; Variable "{0}" no es compatible con los tipos de variables permitidos--->'.format(p[-1]))
		exit(1)
			
def p_tipo(p):
	'''Tipo : INT
			| FLOAT
			| CHAR
			| BOOL'''
	#print(p[1])
	vars_types.append(p[1])
	#PTipos.append(p[1])
	#print(vars_types)
	
def p_tipo2(p):
	'''Tipo2 : INT
			| FLOAT
			| CHAR
			| BOOL
			| VOID'''
	pass
	procs_types.append(p[1])
	PTipos.append(p[1])
	#print(vars_types)

def p_mainprogram(p):
	'''MainProgram : MAIN add_Main_1 PAR_I PAR_D add_Main_2 Bloque add_Main_3'''

def p_add_Main_1(p):		#funcion que se encarga de rellenar el primer GOTO de los cuadruplos. Se salta las funciones.
	'''add_Main_1 : empty'''
	if p[-1] in x.procsLocal.keys():
		print ('<---[REPEATED_FUNC_DECLARATION][MAIN]; Funcion "{0}" esta duplicada y ya existe en el diccionario--->'.format(p[3]))
		exit(1)
	else:
		proc_brackList.append(p[-1])	#Se agrega el nombre de la funcion a la lista para despues usar el nombre y actualizar sus parametros
		#x.procs.update(x.add_procs_to_dict(p[-1],p[-2], count, 10000, {})) #Se da de alta el nombre del procedimiento
		directorio_Activo['local'].update({ p[-1]: { 'Tipo': 'main', '#Params': 0, 'DireccionInicio': 10000, 'Var_Table': {}}}) # Se da de alta el procedimiento como local
		temp = directorio_Activo['local'].values().pop()
		temp['Var_Table'].update({p[-1] : {'Size_1': 0, 'Size_2': 0, 'Tipo': 0}})
		#print("Aqui estoy")
		#pp.pprint(directorio_Activo)


def p_add_Main_2(p):		#funcion que se encarga de rellenar el primer GOTO de los cuadruplos. Se salta las funciones.
	'''add_Main_2 : empty'''
	if(PSaltos):
		retorno = PSaltos.pop() #obtiene el valor de PSaltos mas auntiguo 
		rellenar_cuadruplo(retorno)  #rellena el primer cuadruplo con ese valor
		x.procsLocal.update(directorio_Activo['local'])
		#pp.pprint("ACTUALIZANDO X.PROCS")
		#pp.pprint(procsLocal)

def p_add_Main_3(p):
	'''add_Main_3 : empty'''
	proc_brackList.pop()
	while(var_brackList):
		var_brackList.pop()
	directorio_Activo['local'] = {} #Se libera la tabla de variables locales
	add_quadruple('END', -1, -1, -1, -1, 0) #se genera cuadrplo de fin de programa
	#pp.pprint( get_cuadruplos())
 
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
	'''Asignacion : ID add_ID_TYPE_1 EXP_EQ add_Asignacion_2 Expresion add_Asignacion_3 '''
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


# def p_add_Asignacion_1(p):
# 	'''add_Asignacion_1 : empty '''
# 	PilaO.append(p[-1])
	
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
		#print('Lado izquierdo "{0}" Lado derecho "{1}"'.format(operadorIzquierdo, operadorDerecho))
		#pp.pprint(get_cuadruplos())
		#print(var_brackList)
		#if (vars_exists_in_list(operadorIzquierdo)):
		#pp.pprint(operadorIzquierdo)

		nombre_funcion = proc_brackList.pop()  #Se obtiene el nombre de la funcion
		#print("Nombre de funciones:")
		proc_brackList.append(nombre_funcion)
		if (busca_variable_en_directorio(nombre_funcion, operadorIzquierdo)):
			operacion_cuadruplos(operadorAsigna)
		else:
			print ('<---[UNDECLARED_VARIABLE][Asignacion]; Variable "{0}" no se encuentra previamente definida--->'.format(operadorIzquierdo))
			exit(1)	

def p_expresion(p):
	'''Expresion : Exp ExpresionA '''

def p_expresiona(p):
	'''ExpresionA : ExpresionB add_Exp
				  | empty'''

def p_expresionb(p):
	'''ExpresionB : EXP_GT add_Operator Exp 
				  | EXP_LT add_Operator Exp
				  | EXP_GEQ add_Operator Exp
				  | EXP_LEQ add_Operator Exp
			  	  | EXP_DEQ add_Operator Exp
			  	  | EXP_NEQ add_Operator Exp'''

def p_add_Operator(p):
	'''add_Operator : empty'''
	POper.append(p[-1])

def p_add_Exp(p):
	'''add_Exp : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR in relational_operators): # Si el operador es relational_operators, se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un relational_operators

def p_exp(p):
	'''Exp : Termino add_Term Exp2 '''
	
def p_exp2(p):
	'''Exp2 : OP_PLUS add_Operator Exp
			| OP_MIN add_Operator Exp
			| empty empty '''
	# if (p[1] == '+' or p[1] == '-'):
	# 	POper.append(p[1]) #Se agrega el operador  suma/resta a la pila de operadores
	# 	#print(POper)

def p_addTerm(p):
	'''add_Term : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR == '+' or tempOPERADOR == '-' ): # Si eloperador es "+" o "-", se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un "+" o "-"

def p_termino(p):
	'''Termino : Factor add_Factor Termino2 '''

def p_addFactor(p):
	'''add_Factor : empty'''
	if (POper):
		tempOPERADOR = POper.pop() #Se obtiene el operador tope de la lista
		if (tempOPERADOR == '*' or tempOPERADOR == '/' ): # Si eloperador es "*" o "/", se continua evaluar los operandos
			operacion_cuadruplos(tempOPERADOR) # se manda llamar la funcion que verifica los cuadruplos en el cubo semantico
		else:
			POper.append(tempOPERADOR) # no es un "*" o "/" 


def p_termino2(p):
	'''Termino2 : OP_MULT add_Operator Termino
				| OP_DIV add_Operator Termino
				| empty '''
	# if (p[1] == '*' or p[1] == '/'):
	# 	POper.append(p[1])	#Se agrega el operador multiplicacion/division a la pila de operadores
	# 	#print(POper)

def p_factor(p):
	'''Factor : PAR_I add_Factor_PAR_I Expresion PAR_D add_Factor_PAR_D Factor3
			  | Factor2 VarCte
			  | Llamada_Factor  empty
			  | ID add_ID_TYPE_1  '''
			  
def p_add_Factor_PAR_I(p):
	'''add_Factor_PAR_I :  empty'''
	POper.append(p[-1])		#Se introduceel parentesis como fondo falso

def p_add_Factor_PAR_D(p):
	'''add_Factor_PAR_D :  empty'''
	POper.pop()				#Se remueve el fondo falso

def p_add_Llamada_Factor(p):
	'''Llamada_Factor :  ID add_Llamada_Factor_1 PAR_I Llamada_Factor_2 PAR_D add_Llamada_Factor_5 add_Llamada_Factor_6'''
	#print("Estoy en llamada factor: ", PilaO)

def p_add_Llamada_Factor_1(p):
	'''add_Llamada_Factor_1 :  empty'''
	if (proc_exists_in_list(p[-1])):
		funcion_id.append(p[-1])	#Se guarda el nombre de la funcion que inicio la llamada en una lista = funcion_id
		add_quadruple('ERA', p[-1], -1, -1, -1, 0)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
		contador_k = [0]  # Se inicializa el contador k en 1
		POper.append('[')	#Agregando el fondo falso
	else:
		print ('<---[UNDECLARED_FUNCTION][Llamada_Factor]; Procedimiento "{0}" no se encuentra previamente declarado--->'.format(p[-1]))
		exit(1)

def p_Llamada_Factor_2(p):
	'''Llamada_Factor_2 : Expresion add_Llamada_Factor_3 Llamada_Factor_3
				| empty '''

def p_Llamada_Factor_3(p):
	'''Llamada_Factor_3 : COMA add_Llamada_Factor_4 Llamada_Factor_2
			 	| empty '''
				
def p_add_Llamada_Factor_3(p):
	'''add_Llamada_Factor_3 : empty '''
	valor_argumento = PilaO.pop() #aqui estamos obteniendo el 2.4
	tipo_argumento = PTipos.pop() #tipo de 2.4 = float
	
	nombre_funcion = funcion_id.pop() 
	funcion_id.append(nombre_funcion)

	count = contador_k.pop()
	tipo2 = x.procsLocal[nombre_funcion]['Var_Table'].values()[count]['Tipo']

	#print('Lado izquierdo "{0}" Lado derecho "{1}"'.format(tipo_argumento, valor_argumento))
	#print(PilaO)
	#print("xprocs :", x.procsLocal[nombre_funcion]['Var_Table'].values()[count])
	if(tipo_argumento == tipo2):
		resultado_quadruple = add_quadruple('PARAMETER', valor_argumento, -1, ('Param' + str(count)), 0)  #Se genera el cuadruplo PARAMETER, tiene el k-esimo argumento
		contador_k.append(count)
		#print("parameter es:", resultado_quadruple)
		#PilaO.append(resultado_quadruple)
	else:
		print ('<---[ERROR_TYPE_MISMATCH][Llamada]; No se puede hacer la operacion con los tipos: "{0}" y "{1}"--->'.format(tipo2, tipo_argumento))
		exit(1)

def p_add_Llamada_Factor_4(p):
	'''add_Llamada_Factor_4 : empty '''
	count = contador_k.pop()
	contador_k.append(count+1)

def p_add_Llamada_Factor_5(p):
	'''add_Llamada_Factor_5 : empty '''
	#global contador_parametros
	if (POper and p[-1]) == ')':
	    POper.pop()				#Se remueve el fondo falso
	contador_k = [0]
	nombre_funcion = funcion_id.pop()  #Se obtiene el nombre de la funcion que activo la llamada
	funcion_id.append(nombre_funcion)
	resultado_quadruple = add_quadruple('GOSUB', nombre_funcion, -1, -1, 0)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
	#print("probando: ", resultado_quadruple)
	PilaO.append(resultado_quadruple)
	
def p_add_Llamada_Factor_6(p):
	'''add_Llamada_Factor_6 : empty '''
	nombre_funcion = funcion_id.pop()  #Se obtiene el nombre de la funcion que activo la llamada
	tipo_funcion = procs_return_type(nombre_funcion)
	if(tipo_funcion != 'void'):
		#nombre_funcion = proc_brackList.pop()  #Se obtiene el nombre de la funcion
		operadorIzquierdo = PilaO.pop()
		#PilaO.append(operadorIzquierdo)
		#PilaO.append(nombre_funcion)
		
		#tipoDerecho = PilaO.pop()
		#print('Lado izquierdo "{0}" operador "{1}" Lado derecho "{2}"'.format(operadorIzquierdo, operadorIgual, operadorDerecho))
		#rint('Lado izquierdo "{0}" Lado derecho "{1}"'.format(operadorIzquierdo, operadorDerecho))
		#print(PilaO)
		#print(var_brackList)
		#if (vars_exists_in_list(operadorIzquierdo)):
		#pp.pprint(operadorIzquierdo)

		#print("Nombre de funciones:")
		proc_brackList.append(nombre_funcion)
		#operacion_cuadruplos('=')
		resultado_quadruple = add_quadruple('=', operadorIzquierdo, -1, nombre_funcion, -1, 0) #se genera cuadruplos
		PilaO.append(resultado_quadruple)	#se devuelve el operando a la pila de operadores		
		
		#print("TE ESTOY IMPRIMIENO; ", procs_return_type(nombre_funcion))
		#pp.pprint( x.procsLocal)
		PTipos.append(procs_return_type(nombre_funcion))
		
		
		#pp.pprint(get_cuadruplos())

	else:
		PTipos.append('void')

def p_add_ID_TYPE_1(p):
	'''add_ID_TYPE_1 :  empty'''
	#if (vars_exists_in_list(p[-1])):
	#else:
	#	print ('Procedimiento {0} ya existe en el diccionario'.format(p[2]))
	#	exit(1)
	nombre = proc_brackList.pop()
	proc_brackList.append(nombre)
	#print("imprimiendo suma:", p[-1])
	tipo = vars_return_type(nombre, p[-1])
	#print("Ya imprimi el tipo")
	#print(tipo)
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
	'''Escritura2 :  ID add_Escritura1 add_Escritura Escritura3
 			  |  CTE_STRING add_Escritura2 add_Escritura Escritura3
 			  |  Llamada_Factor add_Escritura Escritura3 '''

#def p_escritura2(p):
#	'''Escritura2 :  Expresion add_Escritura Escritura3'''

def p_escritura3(p):
	'''Escritura3 : PAR_D
				  | COMA Escritura2'''


def p_add_Escritura1(p):
	'''add_Escritura1 : empty'''
	nombre = proc_brackList.pop()
	proc_brackList.append(nombre)
	if(busca_variable_en_directorio(nombre, p[-1])):
		PilaO.append(p[-1])
	else:
		print ('<---[UNDECLARED_VARIABLE][Escritura]; Variable "{0}" no se encuentra previamente definida--->'.format( p[-1]))
		exit(1)	

def p_add_Escritura2(p):
	'''add_Escritura2 : empty'''
	PilaO.append(p[-1])


def p_add_Escritura(p):
	'''add_Escritura : empty'''
	#PilaO.append(p[-1])				# Se otiene el ID directamente y se manda a la pila
	#print("imprimiendo esto: ", PilaO)

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
	#PilaO.append()				# Se otiene el ID directamente y se manda a la pila
	#operandoTEMPORAL = PilaO.pop()  # Se obtiene operando y se genera el cuadruplo
	nombre = proc_brackList.pop()
	proc_brackList.append(nombre)
	if(busca_variable_en_directorio(nombre, p[-1])):
	#print(operandoTEMPORAL)
		add_quadruple('INPUT',  p[-1], -1, -1, -1, 0) #se genera cuadruplos INPUT
	else:
		print ('<---[UNDECLARED_VARIABLE][Lectura]; Variable "{0}" no se encuentra previamente definida--->'.format( p[-1]))
		exit(1)		
		
def p_funcion(p):
	'''Funcion : FUNCTION Tipo2 ID add_Funcion_1 FuncionA add_Funcion_3'''

def p_funciona(p):
	'''FuncionA : PAR_I Params PAR_D add_Funcion_2  Bloque'''
	#print(var_brackList)
	
def p_add_Funcion_1(p):
	'''add_Funcion_1 : empty'''
	if p[-1] in x.procsLocal.keys():
		print ('<---[REPEATED_FUNC_DECLARATION][Funcion]; Funcion "{0}" esta duplicada y ya existe en el diccionario--->'.format(p[3]))
		exit(1)
	else:
		proc_brackList.append(p[-1])	#Se agrega el nombre de la funcion a la lista para despues usar el nombre y actualizar sus parametros
		count = contador_varsGlobales.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
		contador_varsGlobales.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
		func_Tipo = PTipos.pop()	#se saca el tipo de la funcion
		directorio_Activo['local'].update({ p[-1]: { 'Tipo': func_Tipo, '#Params': count, 'DireccionInicio': 10000, 'Var_Table': {}}}) # Se da de alta el procedimiento como local
		x.procsLocal.update(directorio_Activo['local'])

		#print("Aqui estoy")
		#pp.pprint(directorio_Activo)
	
def p_add_Funcion_2(p):
	'''add_Funcion_2 : empty'''
	count = contador_varsGlobales.pop() # Se otiene el contador de parametros y se manda al dir. de procs.
	contador_varsGlobales.append(0)	#Se vacia el listado y se reinicializa en 0 parametros
	var = proc_brackList.pop() #Se obtiene el nombre de la funcion actual
	proc_brackList.append(var)
	directorio_Activo['local'][var]['#Params'] = count	#Se actualiza la funcion con su numero de parametros
	x.procsLocal.update(directorio_Activo['local'])

	
def p_add_Funcion_3(p):
	'''add_Funcion_3 : empty'''
	add_quadruple('ENDPROC', -1, -1, -1, -1, 0) #se genera cuadrplo de fin de programa
	#print("Aqui estoy")
	#pp.pprint(directorio_Activo)
	proc_brackList.pop()
	while(var_brackList):
		var_brackList.pop()
	x.procsLocal.update(directorio_Activo['local'])
	#print("wow")
	#pp.pprint(directorio_Activo)
	#pp.pprint("ACTUALIZANDO X.PROCS")
	#pp.pprint(directorio_Activo)
	directorio_Activo['local'] = {} #Se libera la tabla de variables locales


def p_params(p):
	'''Params : Tipo ID add_Params1 Params2
			   | empty empty empty '''
			   
def p_add_Params1(p):
	'''add_Params1 : empty '''
	if (vars_exists_in_list(p[-1])):
		#vars_types.pop()
		print ('<---[REPEATED_DECLARATION][Params]; Variable "{0}" ya existe en el diccionario--->'.format(p[-1]))
		exit(1)
	else:
		var_brackList.append(p[-1])
		count = contador_varsGlobales.pop()  #se obtiene el contador actual de la lista
		contador_varsGlobales.append(count +1)	# se suma 1 ya que se agrego una variable
		tipo = vars_types.pop()	#Se obtiene el tipo de la variable
		temp = directorio_Activo['local'].values().pop()
		temp['Var_Table'].update({p[-1] : {'Size_1': 1, 'Size_2': 0, 'Tipo': tipo, 'DireccionInicio': 2000}})	#Se agrega la variable al diccionario local
		#print("Aca vamos")
		#pp.pprint(directorio_Activo)

def p_params2(p):
	'''Params2 : COMA Params
			   | empty empty '''

def p_llamada(p):
	'''Llamada : ID add_Llamada_1 PAR_I add_Llamada_2 Llamada2 PAR_D add_Llamada_5 '''
	# x(2);

def p_llamada2(p):
	'''Llamada2 : Expresion add_Llamada_3 Llamada3
				| empty '''

def p_llamada3(p):
	'''Llamada3 : COMA add_Llamada_4 Llamada2
			 	| empty '''

def p_add_Llamada_1(p):
	'''add_Llamada_1 : empty '''
	#global contador_parametros
	#print("Nombre funcion")
	#pp.pprint(proc_brackList)
	if (proc_exists_in_list(p[-1])):
		funcion_id.append(p[-1])
		print("estoy imprimiendo llamadas: ", p[-1])
	else:
		print ('<---[UNDECLARED_FUNCTION][Llamada]; Procedimiento "{0}" no se encuentra previamente declarado--->'.format(p[-1]))
		exit(1)


def p_add_Llamada_2(p):
	'''add_Llamada_2 : empty '''
	#print(p[-2])
	add_quadruple('ERA', p[-3], -1, -1, 0)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
	contador_k = [0]  # Se inicializa el contador k en 1		

	#	sacar #params del nombre de la funcion funcion_id.pop(), despues asignar memoria dependiendo de ese numero
	#	x.procsLocal[nombre_funcion_que_lo_llama]['#Params']
	
def p_add_Llamada_3(p):
	'''add_Llamada_3 : empty '''
	valor_argumento = PilaO.pop() #aqui estamos obteniendo el 2.4
	tipo_argumento = PTipos.pop() #tipo de 2.4 = float
	
	#print()
	nombre_funcion = funcion_id.pop() 
	funcion_id.append(nombre_funcion)

	#print(funcion_id)
	count = contador_k.pop()
	#print(count)
	tipo2 = x.procsLocal[nombre_funcion]['Var_Table'].values()[count]['Tipo']
	#aux = x.procsLocal[nombre_funcion]['Var_Tables'].keys()
	#x.procsLocal[nombre_funcion]['Var_Table'].keys()[n]
	
	#print('Lado izquierdo "{0}" Lado derecho "{1}"'.format(tipo_argumento, valor_argumento))
	#print(PilaO)
	#pp.pprint(get_cuadruplos())	
	#tipo2 = vars_return_type(nombre_funcion, count)
	#print("El tipo1: "+tipo_argumento)
	#print("El tipo2: "+tipo2)
	#print(tipo_argumento)
	#pp.pprint(get_cuadruplos())
	if(tipo_argumento == tipo2):
		resultado_quadruple = add_quadruple('PARAMETER', valor_argumento, -1, ('Param' + str(count)), 0)  #Se genera el cuadruplo PARAMETER, tiene el k-esimo argumento
		contador_k.append(count)
		#PilaO.append(resultado_quadruple)
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
	contador_k = [0]
	nombre_funcion = funcion_id.pop()
	#add_quadruple('GOSUB', nombre_funcion, -1, -1, -1)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
	resultado_quadruple = add_quadruple('GOSUB', nombre_funcion, -1, -1, 0)  #Se genera el cuadruplo ERA, tiene expansion del registro activacion de acuerdo al tamano definido
	#print("probando: ", resultado_quadruple)
	PilaO.append(resultado_quadruple) #Se devuelve el temporal del gosub

		
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
	'''LlamadaPersonaje3 : COMA  LlamadaPersonaje2
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
	if (vars_exists_in_list(p[-1])):
		PilaO.append(p[-1])  # Guardar el identificador (direccion) en pila de Operandos (PilaO), verificar semantica

def p_add_For_2(p):
	'''add_For_2 : empty '''
	auxExp1 = PilaO.pop()
	p
	auxID = PilaO.pop()
	PilaO.append(auxID)
	add_quadruple('=', auxID, -1, auxExp1, -1, 0)

def p_add_For_3(p):
	'''add_For_3 : empty '''
	auxExp2 = PilaO.pop()
	temp_Tf = auxExp2
	temp_Tx = 0
	resultado_Tf = add_quadruple('=', auxExp2, -1, temp_Tf, -1, 1)
	#pp.pprint(get_cuadruplos())
	auxID = PilaO.pop()
	PilaO.append(auxID)
	resultado_Tx = add_quadruple('<=', auxID, -1, resultado_Tf, -1, 0)
	
	add_quadruple('GOTOF', resultado_Tx, -1, -1, -1, 0) #se genera cuadruplo 
	#liberar Tx
	PSaltos.append(get_count_cuadruplos() - 2)

def p_add_For_4(p):
	'''add_For_4 : empty '''
	auxID = PilaO.pop()
	add_quadruple('+', auxID, -1, auxID, -1, 0)
	retorno = PSaltos.pop()
	add_quadruple('GOTO', retorno, -1, -1, -1, 0)
	rellenar_cuadruplo(retorno+1)
#	Liberar var temp Tf
	
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
	
	
# def obtain_type_from_dictionary(id_funcion, v_id):
# 	#print("imprime indice: ")
# 	pp.pprint(x.procs)
# 	param_length = x.procs[id_funcion]['#Params']	#Revise que no se manden mas parametros en una llamada de lo que la funcion puede recibir
# 	#print(id_funcion)
# 	if(param_length >= indice):
# 		return x.procs[id_funcion]['Var_Table'].values()[indice-1]['Tipo']  #Busca en la tabla de variables del procedimiento "id_funcion" el tipo segun su "indice"
# 	else:
# 		print ('<---[PARAMETER_LENGTH_MISMATCH][Llamada]; La funcion esperaba "{0}" parametros y recibio "{1}" parametros--->'.format(param_length, indice))
# 		exit(1)
		
def proc_exists_in_list(v_id):
	aux =x.procsLocal.keys()
	for y in aux:
		if v_id in y:
			#print("entro")
			return True
	
	aux = x.procsGlobal.keys()
	print("tu vid es: ", v_id)
	print("aux es: ", aux)	
	for y in aux:
		if v_id in y:
			#print("entro")
			return True
			
	return False
	
def busca_variable_en_directorio(nombre, var):
	aux = directorio_Activo['local'].keys()
	nombre = aux.pop()
	#print (proc_)
	aux = directorio_Activo['local'][nombre]['Var_Table'].keys()
	for c in aux:
	    if var == c:
	        return True
	        
	aux2 = directorio_Activo['global'].keys()
	nombre = aux2.pop()
	#print("IMPRIME M")
	#print (var)
	aux2 = directorio_Activo['global'][nombre]['Var_Table'].keys()
	#print("AUX ES ")
	#pp.pprint (directorio_Activo['global'])
	#pp.pprint (directorio_Activo['global'].keys())
	for c in aux2:
	    if var == c:
	        return True
	        
	return False	


def vars_exists_in_list(v_id):
	#print (v_id)
	#print(var_brackList) for key in var_bracklist[v_id]
	#pp.pprint(directorio_Activo)
	for y in var_brackList:
		#if y == v_id:
		if v_id in y:
			#print(y)
			return True
	return False

#direc_activo['local'][nombre]['Var_Table'][v_id]['Tipo']

def procs_return_type(nombre):
	aux =x.procsLocal.keys()
	for y in aux:
		if nombre in y:
			#print("entro")
			#print("El tipo es", x.procsLocal[nombre]['Tipo'])
			return x.procsLocal[nombre]['Tipo']
	
	aux = x.procsGlobal.keys()
	for y in aux:
		if nombre in y:
			#print("entro")
			#print("El tipo es", x.procsGlobal[nombre]['Tipo'])
			return x.procsGlobal[nombre]['Tipo']			
	return False

# def vars_return_type(nombre, v_id):
# 	aux = directorio_Activo['local'][nombre]['Var_Table'].keys()
# 	#pp.pprint(aux)
# 	for c in aux:
# 	    if v_id == c:
# 	        return directorio_Activo['local'][nombre]['Var_Table'][v_id]['Tipo']
# 	aux = directorio_Activo['global'][nombre]['Var_Table'].keys()
# 	for c in aux:
# 	    if v_id == c:
# 	        return directorio_Activo['global'][nombre]['Var_Table'][v_id]['Tipo']
# 	return False

def vars_return_type(nombre, v_id):
	auxlocal = x.procsLocal[nombre]['Var_Table'].keys()
	auxglobal = x.procsGlobal.keys()
	auxglobalnombre = auxglobal.pop()
	auxglobal = x.procsGlobal[auxglobalnombre]['Var_Table'].keys()
	for key in auxlocal:
		if key == v_id:
			return (x.procsLocal[nombre]['Var_Table'][v_id]['Tipo'])
	for key in auxglobal:
		if key == v_id:
			return (x.procsGlobal[auxglobalnombre]['Var_Table'][v_id]['Tipo'])
	return False


def operacion_cuadruplos(tempOPERADOR): 
	operador = tempOPERADOR
	tempTIPO2 = PTipos.pop()
	#print("El tipo de op2 es: ", tempTIPO2)
	tempTIPO1 = PTipos.pop()
	#print("El tipo de op1 es: ", tempTIPO1)
	if tempOPERADOR in relational_operators:
		tempOPERADOR = 'comp'
	elif tempOPERADOR in logical_operators:
		tempOPERADOR = 'log'
	#print("PilaO es: ", PilaO)	
	#print("PTipos es: ", PTipos)	
	#print("----------------------------")	
	resultadoTIPO = check_operation(tempTIPO1,operador,tempTIPO2) # Se manda llamar el cubo semantico
	if (resultadoTIPO != 'error'): 
		tempOPERAND2 = PilaO.pop()
		#print('Operando2: "{0}"'.format(resultadoTIPO))
		#pp.pprint(get_cuadruplos())
		#print("El operando 2 es: ", tempOPERAND2)
		#print("El operandador es: ", operador)

		tempOPERAND1 =  PilaO.pop()
		#print("El operando 1 es: ", tempOPERAND1)

		#print('Operando1: "{0}"'.format(tempOPERAND1))
		resultado_quadruple = add_quadruple(operador, tempOPERAND1, tempTIPO1, tempOPERAND2, tempTIPO2, 0) #se genera cuadruplos
		if (operador != '='):
			PilaO.append(resultado_quadruple)	#se devuelve el operando a la pila de operadores
			PTipos.append(resultadoTIPO)		#se devuelve el tipo a la pila de tipos

	else:
	    #tronarlo
	    print ('<---[ERROR_TYPE_MISMATCH][Expresion]; No se puede hacer la operacion con los tipos: {0}, {1}, {2}--->'.format(tempTIPO1, operador, tempTIPO2))
	    exit(1)


def p_error(p):
	print ("<---[SYNTAX_ERROR]--->")
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