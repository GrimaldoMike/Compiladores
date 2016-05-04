# Proyecto compilador Python
# Maquina Virtual de Fight Compilers 2016
# Hecho por Jaime Neri y Mike Grimaldo
#!env/bin/python

import simplejson
import sys
from pprint import pprint
import os

os.system("python FightCompilersYacc.py -f example2.txt")  #Corre un archivo python externo python (compilador)

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

dir_stack = {'variable' : {}}

#Stacks que utiliza la VM

currentFunctionId = []


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
	keys = dir_stack['variable']
	#print ("dude",keys)
	aux = keys.keys()
	for y in aux:
		if var in y:
			return True
	return False

#Funcion que devuelve el valor de la variable si existe en el diccionario, de lo contrario "no hace nada"
def return_value_from_variable(var):
    x = var
    #print ("hola1", x)
    if (var_exists_in_dict(var)):
        x = dir_stack['variable'][var]
        #print ("hola2", x)
    return x

def dictionary_update(op1, op2):
    dir_stack['variable'].update({op1 : op2})
    print ("Instruccion aritmetica: {0} = {1} ".format(op1, op2))
    #print (dir_stack)

def execute_program(l):
	loop = len(instructions)
	i = 0
	while i < loop:
		#instruction = l[i] #l son los diccionarios
		quad_actual = instructions[i]
		if quad_actual[0] == 'GOTO':
			#i = quad_actual[3] - 1
			print ("GOTO encontrado; cambiando de posicion...")
		elif quad_actual[0]  == 'GOTOF':
			condition = return_value_from_variable(quad_actual[1])
			if not condition:
			    i = quad_actual[3] - 1
			    print ("Cambiando de posicion...")
		elif quad_actual[0] == '=':
			#op2 = getValueFromMemory(quad_actual[i][1])
			#op1 = getValueFromMemory(quad_actual[i][3])
			op2 = quad_actual[1]
			op1 = quad_actual[3]
			dictionary_update(op1, op2)
			#modIndex = quad_actual[i][2]
			#pprint(dir_stack)
			stack.append(op1)
		elif quad_actual[0] == 'ERA':
			save_function_name(quad_actual[3])  #guarda el nombre de la funcion de ERA
			#print ("id es: ", currentFunctionId)
		elif quad_actual[0] == 'PARAMETER':
			#print("dir_stack", dir_stack)
			op2 = return_value_from_variable(quad_actual[1])
			op1 = quad_actual[3]
			dictionary_update(op1, op2)
			#pprint("aqui", dir_stack)
		elif quad_actual[0] == '+':
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			dictionary_update(quad_actual[3], (op1 + op2))
			print(dir_stack)
		elif quad_actual[0] == '-':
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			dictionary_update(quad_actual[3], (op1 - op2))
			print(dir_stack)
		elif quad_actual[0] == '*':
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			dictionary_update(quad_actual[3], (op1 * op2))
			print(dir_stack)
		elif quad_actual[0] == '/':
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			dictionary_update(quad_actual[3], (op1 / op2))
			print(dir_stack)
		elif quad_actual[0] == '<':
			boolAux = False
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			if op1 < op2:
				boolAux = True
			dictionary_update(quad_actual[3], boolAux)
		elif quad_actual[0] == '>':
			boolAux = False
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			if op1 > op2:
				boolAux = True
			dictionary_update(quad_actual[3], boolAux)
		elif quad_actual[0] == '<=':
			boolAux = False
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			if op1 <= op2:
				boolAux = True
			dictionary_update(quad_actual[3], boolAux)
			print(dir_stack)
		elif quad_actual[0] == '>=':
			boolAux = False
			op1 = cast_to_int_or_float(return_value_from_variable(quad_actual[1]))
			op2 = cast_to_int_or_float(return_value_from_variable(quad_actual[2]))
			if op1 >= op2:
				boolAux = True
			dictionary_update(quad_actual[3], boolAux)
			
			#parameterAction(op2, quad_actual[3])
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