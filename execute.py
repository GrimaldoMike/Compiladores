# Proyecto compilador Python
# Maquina Virtual de Fight Compilers 2016
# Hecho por Jaime Neri y Mike Grimaldo
#!env/bin/python

import simplejson
import sys
from pprint import pprint
import os

os.system("python FightCompilersYacc.py -f example1.txt")  #Corre un archivo python externo python (compilador)

with open('executable.json') as data_file:    
    data = simplejson.load(data_file)

#python FightCompilersYacc.py -f example1.txt

# functions = output_quadruples['funcs']
# instructions = output_quadruples['quadruples']
# constants = output_quadruples['constants']
# globalvars = output_quadruples['globals']
# fcinstucts = output_quadruples['fightcomp']


globalfuncs = data['funcs_Global']
localfuncs = data['funcs_Local']
instructions = data['quadruples']
codeLines = data['code']

dir_stack = {'variable' : {},
			'var_booleans' : {}
}

#Stacks que utiliza la VM

currentFunctionId = []	#lista de funcion actual
recuperar_linea = []  # linea guardada mientras se ejecuta un gosub (llamada a funcion)
listValue = []
stack = []

def load_program(argv):
	f = open(argv)
	lines = f.read().replace("\n", " ")
	lines = lines.split(" ")
	f.close()
	return lines

def save_function_name(functionId):
    currentFunctionId.append(functionId)
    
def cast_to_int_or_float(theNumber):
	intcast = int(float(theNumber))
	floatcast = float(theNumber)
	result = floatcast - intcast
	if result == 0:
		return intcast
	else:
		return floatcast

#Funcion que devuelve booleano si existe una variable en el diccionario
def var_exists_in_dict(var):
	keys = dir_stack['variable'].keys()
	x = str(var)
	for y in keys:
		
		if var in y:
			print("SUCCESS")
			print("var: ", var)
			print("y: ", y)
			return True
	return False

#Funcion que devuelve el valor de la variable si existe en el diccionario, de lo contrario "no hace nada"
def return_value_from_variable(var):
    x = var
    #print ("hola1", x)
    #print (dir_stack)
    if (var_exists_in_dict(var)):
    	#print("El ultimo que truene:", var)
    	#pprint(dir_stack.values())
    	#print("SUCCESS2")
    	x = dir_stack['variable'][var]
    	#print("x", x)
        #print ("hola2", x)
    #else:
    	#agregar temp a dict
    return x

def dictionary_update(op1, op2):
	dir_stack['variable'].update({op1 : op2})
	print ("Instruccion aritmetica: {0} = {1} ".format(op1, op2))
	print (dir_stack)

#Funcion que devuelve booleano si existe una variable para booleano
def var_exists_in_dict_bool(var):
	keys = dir_stack['var_booleans'].keys()
	for y in keys:
		if var in y:
			return True
	return False

#Funcion que devuelve el valor de la variable para booleanos
def return_value_from_variable_bool(var):
    x = var
    print (dir_stack)
    if (var_exists_in_dict_bool(var)):
    	x = dir_stack['var_booleans'][var]
    return x

# def dictionary_update_bool(op1, op2):
# 	listValue.append(op)
#     dir_stack['var_booleans'].update({op1 : op2})
#     print ("Instruccion logica: {0} = {1} ".format(op1, op2))

def dictionary_update_bool(op1, op2):
	dir_stack['var_booleans'].update({op1 : op2})
	print ("Instruccion logica: {0} = {1} ".format(op1, op2))
	#print (dir_stack)

def execute_program(l):
	loop = len(instructions)
	i = 0
	while i < loop:
		#instruction = l[i] #l son los diccionarios
		quad_actual = instructions[i]
		if quad_actual[0] == 'GOTO':
			i = quad_actual[3] - 1
			print ("GOTO encontrado; cambiando a posicion {0}".format(i+1))
			
		elif quad_actual[0]  == 'GOTOF':
			condition = return_value_from_variable_bool(quad_actual[1])
			if not condition:
			    i = quad_actual[3] - 1
			    print ("Cambiando de posicion...")
			    
		elif quad_actual[0] == '=':
			#op2 = getValueFromMemory(quad_actual[i][1])
			#op1 = getValueFromMemory(quad_actual[i][3])
			try:
				op2 = return_value_from_variable(quad_actual[1])
			except KeyError:
				op2 = quad_actual[1]
				
			op1 = quad_actual[3]
			dictionary_update(op1, op2)
			#modIndex = quad_actual[i][2]
			#pprint(dir_stack)
			stack.append(op1)
			
		elif quad_actual[0] == '+':
			try:
				op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			except KeyError:
				print("ripperino")
				op1 = cast_to_int_or_float(quad_actual[1])
			try:
				op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
				print("SUCCESS op2 = 3: ", op2)
			except KeyError:
				print("ripperino2")
				op2 = cast_to_int_or_float(quad_actual[2])
			dictionary_update(quad_actual[3], (op1 + op2))
			
		elif quad_actual[0] == '-':
			try:
				op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			except KeyError:
				print("ripperino")
				op1 = cast_to_int_or_float(quad_actual[1])
			try:
				op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
				#print("SUCCESS op2 = 3: ", op2)
			except KeyError:
				print("ripperino2")
				op2 = cast_to_int_or_float(quad_actual[2])
			dictionary_update(quad_actual[3], (op1 - op2))
			
		elif quad_actual[0] == '*':
			try:
				op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			except KeyError:
				print("ripperino")
				op1 = cast_to_int_or_float(quad_actual[1])
			try:
				op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
				#print("SUCCESS op2 = 3: ", op2)
			except KeyError:
				print("ripperino2")
				op2 = cast_to_int_or_float(quad_actual[2])
			dictionary_update(quad_actual[3], (op1 * op2))
			
		elif quad_actual[0] == '/':
			try:
				op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			except KeyError:
				print("ripperino")
				op1 = cast_to_int_or_float(quad_actual[1])
			try:
				op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
				print("SUCCESS op2 = 3: ", op2)
			except KeyError:
				print("ripperino2")
				op2 = cast_to_int_or_float(quad_actual[2])
			dictionary_update(quad_actual[3], (op1 / op2))
			
		elif quad_actual[0] == 'ERA':
			save_function_name(quad_actual[3])  #guarda el nombre de la funcion de ERA
			#print ("id es: ", currentFunctionId)
		elif quad_actual[0] == 'PARAMETER':
			#print("dir_stack", dir_stack)
			op2 = return_value_from_variable(quad_actual[1])
			op1 = quad_actual[3]
			dictionary_update(op1, op2)
			stack.append(op1)
			#pprint(dir_stack)
		elif quad_actual[0] == 'GOSUB':
			save_function_name(quad_actual[3])	#guarda el nombre de funcion que se llamara con el gosub
			recuperar_linea.append(i)
			#print (recuperar_linea)			#guarda el cuadruplo donde se quedo andtes de llamar al gosub
			i =  quad_actual[1] - 1
			print ("GOSUB encontrado; cambiando a posicion: {0}".format(i+1))
		elif quad_actual[0] == '<':
			boolAux = False
			op1 = return_value_from_variable_bool(quad_actual[1])
			op2 = return_value_from_variable_bool(quad_actual[2])
			if (op1 < op2):
				boolAux = True
			dictionary_update_bool(quad_actual[3], boolAux)
		elif quad_actual[0] == '>':
			boolAux = False
			op1 = return_value_from_variable_bool(quad_actual[1])
			op2 = return_value_from_variable_bool(quad_actual[2])
			if (op1 > op2):
				boolAux = True
			dictionary_update_bool(quad_actual[3], boolAux)
		elif quad_actual[0] == '<=':
			boolAux = False
			op1 = return_value_from_variable_bool(quad_actual[1])
			op2 = return_value_from_variable_bool(quad_actual[2])
			if (op1 <= op2):
				boolAux = True
			dictionary_update_bool(quad_actual[3], boolAux)
			#print(dir_stack)
		elif quad_actual[0] == '>=':
			boolAux = False
			op1 = return_value_from_variable_bool(quad_actual[1])
			op2 = return_value_from_variable_bool(quad_actual[2])
			if (op1 >= op2):
				boolAux = True
			dictionary_update_bool(quad_actual[3], boolAux)
		elif quad_actual[0] == '==':
			boolAux = False
			op1 = return_value_from_variable_bool(quad_actual[1])
			op2 = return_value_from_variable_bool(quad_actual[2])
			if (op1 == op2):
				boolAux = True
			dictionary_update_bool(quad_actual[3], boolAux)
		elif quad_actual[0] == 'ENDPROC':
			print (recuperar_linea)
			i = recuperar_linea.pop()			#recupera el numero de cuadruplo donde se quedo
			#print("es la i: ", i)
			#i= len(instructions) - 2
		elif quad_actual[0] == 'INPUT':
			print("PRINT TO CONSOLE:" +  quad_actual[3]  );
		elif quad_actual[0] == 'OUTPUT':
			print ("Printing to console " +  quad_actual[3]  )
		elif quad_actual[0] == 'RETURN':
			op1 = quad_actual[3]
			op2 = return_value_from_variable(quad_actual[3])
			#line = quad_actual[1];
			#returnAction(value, line);
			dictionary_update(op1, op2)
		i+=1

#execute_program(1)

def run_program(argv):
	#l = load_program(argv)
	execute_program(argv)

def main(argv):
	run_program(argv[0])
	return 0

def target(*args):
	return main, None

if __name__ == '__main__':
	main(sys.argv)