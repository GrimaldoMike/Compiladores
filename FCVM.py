# Proyecto compilador Python
# Maquina Virtual de Fight Compilers 2016
# Hecho por Jaime Neri y Mike Grimaldo
#!env/bin/python

import simplejson
from pprint import pprint
import os

os.system("python FightCompilersYacc.py -f example1.txt")  #Corre un archivo python externo python (copilador)

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
slocal = []
sglobal = []
stemp = []
stempglobal = []

execstack = []
paramstack = []
params = []
current_address = 0
current_func_ID = 'main'
stackpos = 'main'
#stack = []

# OP_EOP = "00"
# OP_EOI = "01"
# OP_PUSH = "02"
# OP_POP = "03"
# OP_PRINT = "04"
# OP_ADD = "05"
# OP_SUB = "06"
# OP_MUL = "07"
# OP_DIV = "08"


def load_program(argv):
	f = open(argv)
	lines = f.read().replace("\n", " ")
	lines = lines.split(" ")
	f.close()
	return lines

def parameterAction(value, parameterIndex):
    params[parameterIndex] = value
    print ("Added parameter "+value+" to parameters array for "+ current_func_ID)

def goSub(destinationDir, line):
	#pre

def do_PUSH(i, l):
	topush = int(l[i + 1], 16)
	#stack.append(topush)


def do_POP():
	#stack.pop()
	pass

def do_PRINT(stack):
	print (stack[-1])

def do_ADD(stack):
	num1 = stack.pop()
	num2 = stack.pop()
	total = num1 + num2
	stack.append(total)


def do_SUB(stack):
	num1 = stack.pop()
	num2 = stack.pop()
	total = num1 - num2
	stack.append(total)

def do_MUL(stack):
	num1 = stack.pop()
	num2 = stack.pop()
	total = num1 * num2
	stack.append(total)

def do_DIV(stack):
	num1 = stack.pop()
	num2 = stack.pop()
	total = num2 / num1
	stack.append(total)

def execute_program(l):
	loop = len(instructions)
	i = 0
	while i < loop:
		#instruction = l[i] #l son los diccionarios
		what_do = instructions[i]
		if what_do[0] == 'GOTO':
			i = what_do[3] - 1
			print ("GOTO encontrado; cambiando de posicion...")
		elif what_do[0]  == 'GOTOF':
			condition = getValueFromMemory(what_do[i][1])
			if not condition:
			    i = what_do[3] - 1
			    print ("Cambiando de posicion...")
		    #cosas para desplegar...
		elif what_do[0] == 'INPUT':
			pass
		elif what_do[0] == 'OUTPUT':
			print ("Printing to console " + getValueFromMemory( what_do[i][3] ) )
		elif what_do[0] == 'GOSUB':
			line = what_do[1]
			goSub(what_do[3], line)
			i = i - 1
		elif what_do[0] == 'RETURN':
			pass
		elif what_do[0] == 'ENDPROC':
			pass
		elif what_do[0] == 'ERA':
			pass
			#expandActivationRecord <<----- niggawhat?
		elif what_do[0] == 'PARAMETER':
			value = getValueFromMemory(what_do[1])
			parameterAction(value, what_do[3])
		elif what_do[0] == 'END':
			exit(0)
		elif what_do[0] == '=':
			#op2 = getValueFromMemory(what_do[i][1])
			#op1 = getValueFromMemory(what_do[i][3])
			op2 = what_do[1]
			op1 = what_do[3]
			dir_stack['variable'].update(op1 : op2)
			print ("Instruccion aritmetica: {0} = {1} ".format(op1, op2))
			#modIndex = what_do[i][2]
			stack.append(op1)
		elif what_do[0] == '+':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 + op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '-':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 - op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '*':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 * op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '/':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 / op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '<':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 < op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '>':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 > op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '<=':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 <= op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		elif what_do[0] == '>=':
			op1 = getValueFromMemory(what_do[1])
			op2 = getValueFromMemory(what_do[2])
			setValueInMemory(op1 >= op2, what_do[3])
			print (getValueFromMemory(what_do[3]))
		i+=1

def run_program(argv):
	#l = load_program(argv)
	execute_program(argv[0])

def main(argv):
	run_program(argv[0])
	return 0

def target(*args):
	return main, None

if __name__ == '__main__':
	main(sys.argv)