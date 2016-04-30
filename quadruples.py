from sets import Set
from FightCompilersSemantics import Semantics, semantics_cube

quadruples = [] # Lista de cuadruplos
count_cuadruplos = 0 # Contador que cuenta en que numero de cuadruplos va

offset = 0 #variable que va contando los espacios de memoria

relational_operators = set(['<', '>', '<>', '==', '<=', '>='])
logical_operators = set(['AND', 'OR'])
ignored_checks = set(['PRINT', 'READ', 'INPUT', 'GOTOF', 'GOTO', 'RETURN', 'PARAMETER', 'ERA', 'GOSUB', 'ENDPROC'])
    

def check_operation(type1, operator,  type2):
    if operator is '=':
        return semantics_cube.get( (type1, operator, type2) , 'error')
    elif operator in ignored_checks:
        return 'continue'
    elif operator in relational_operators:
        result_type = semantics_cube.get( (type1, 'comp', type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, 'comp', type1) , 'error')
        return result_type
    elif operator in logical_operators:
        result_type = semantics_cube.get( (type1, 'log', type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, 'log', type1) , 'error')
        return result_type
    else:
        result_type = semantics_cube.get( (type1, operator, type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, operator, type1) , 'error')
        return result_type

def get_count_cuadruplos():
    return count_cuadruplos

def get_cuadruplos():
    return quadruples
    
def rellenar_cuadruplo(saltos):
    quadruples[saltos][3] = count_cuadruplos  # Se busca el numero de cuadruplo enviado, en la posicion 4 (sub 3) y se inserta el contador actual
    #print(quadruples[saltos])  # Se busca el numero de cuadruplo enviado, en la posicion 4 (sub 3) y se inserta el contador actual

#def add_quadruple(operator, op1, type1,  op2, type2, mem_temps, mem_global_temps, modIndex=0):
def add_quadruple(operator, op1, type1,  op2, type2, modIndex=0):
    global count_cuadruplos
    global offset
    count_cuadruplos += 1
    #print current['scope'], operator, op1, type1, op2 ,type2

    #result_type = check_operation(type1, operator, type2)

    if operator is '=':
        quadruples.append( [operator, op1, modIndex, op2] )
        #   print("Lado derecho es"+op2)
        return op2
    elif operator in relational_operators:
        quadruples.append( [operator, op1, op2, 'temp'+str(offset)] )  #aqui se debe de validar las variables temporales por scope
        offset += 1
        return ('temp'+str(offset-1))
    elif operator == 'GOTOF':
        quadruples.append( [operator, op1, op2, -1] ) 
        return count_cuadruplos
    elif operator == 'GOTO':
        quadruples.append( [operator, -1, -1, op1] )
        return count_cuadruplos
    elif operator == 'OUTPUT':
        quadruples.append( [operator, -1, -1, op1] )
        return op1
    elif operator == 'INPUT':
        quadruples.append( [operator, -1, -1, op1] )
        return op1
    elif operator == 'RETURN':
        quadruples.append( [operator, type1, -1, op1] )
        return op1
    elif operator == 'ERA':
        quadruples.append( [operator, -1, -1, op1] )
        return op1
    elif operator == 'ENDPROC':
        quadruples.append( [operator, -1, -1, op1] )
        return op1
    elif operator == 'PARAMETER':
        quadruples.append( [operator, op1, -1, op2] )
        return op1
    elif operator == 'GOSUB':
        quadruples.append( [operator, -1, -1, op1] )
        offset += 1
        return ('temp'+str(offset-1))
    elif operator == 'END':
        quadruples.append( [operator, -1, -1, -1] )
        return op1

    temp = 0
    
    # if operator is '+':
    #     temp = int(op1)+int(op2)
    # elif operator is '-':
    #     temp = int(op1)-int(op2)
    # elif operator is '*':
    #     temp = int(op1)*int(op2)
    # elif operator is '/':
    #     temp = int(op1)/int(op2)
    
    if operator is not '=':
        quadruples.append( [operator, op1, op2, 'temp'+str(offset)] )
        offset += 1
    return ('temp'+str(offset-1))


# def assign_mem_value(operator, var_type1, var_type2, scope):
#     mtype = check_operation(var_type1,operator,var_type2) # Se manda llamar el cubo semantico
    
#     if mtype == 'bool':
#         return memory.add_bool(num)
#     elif mtype == 'int':
#         return memory.add_int(num)
#     elif mtype == 'float':
#         return memory.add_float(num)
#     elif mtype == 'char':
#         return memory.add_char(num)
#     elif mtype == 'string':
#         return memory.add_string(num)
#     else:
#         print ('Void')
#     # TODO: write code...