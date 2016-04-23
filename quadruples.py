from sets import Set
from FightCompilersSemantics import Semantics, semantics_cube

quadruples = [] # Lista de cuadruplos
count_cuadruplos = 0 # Contador que cuenta en que numero de cuadruplos va

offset = 0 #variable que va contando los espacios de memoria

relational_operators = set(['<', '>', '<>', '==', '<=', '>='])
logical_operators = set(['AND', 'OR'])
ignored_checks = set(['PRINT', 'READ', 'INPUT', 'GOTOF', 'GOTO', 'RETURN', 'PARAMETER', 'ERA', 'GOSUB', 'ENDPROC'])
    
temps = {
    'bool': { 'unused': set([]), 'used': set([])},
    'int': {'unused': set([]), 'used': set([])},
    'float': {'unused': set([]), 'used': set([])},
    'char': {'unused': set([]), 'used': set([])},
    'string': {'unused': set([]), 'used': set([])}
}
next_temp = 1    

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
    count_cuadruplos += 1
    #print current['scope'], operator, op1, type1, op2 ,type2

    #result_type = check_operation(type1, operator, type2)

    if operator is '=':
        quadruples.append( [operator, op2, modIndex, op1] )
        return op2
    elif operator in relational_operators:
        quadruples.append( [operator, op2, modIndex, op1] )
        return op1
    elif operator == 'GOTOF':
        quadruples.append( [operator, op1, op2, -1] ) 
        return count_cuadruplos
    elif operator == 'GOTO':
        #print ("op1: ")
        #print (op1)
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
    temp = 0
    
    if operator is '+':
        temp = int(op1)+int(op2)
    elif operator is '-':
        temp = int(op1)-int(op2)
    elif operator is '*':
        temp = int(op1)*int(op2)
    elif operator is '/':
        temp = int(op1)/int(op2)
    
    if operator is not '=':
        quadruples.append( [operator, op1, op2, temp] )

    #print("-----Inicia cuadruplos----")
    #print (quadruples)
    #print("-----Termina cuadruplos----")
    #print(count_cuadruplos)
    return temp
    #else:
    #    quadruples.append( [operator, op1, op2, 1000+offset] )
    #    offset += 1
    #    print(quadruples)
    # elif operator == 'PRINT':
    #     quadruples.append( [operator, op2, -1, op1] )
    # elif operator == 'READ':
    #     quadruples.append( [operator, -1, -1, op1] )
    # elif operator == 'GOTOF':
    #     quadruples.append( [operator, op1, op2, -1] )
    # elif operator == 'GOTO':
    #     quadruples.append( [operator, -1, -1, op1] )
    # elif operator == 'RETURN':
    #     quadruples.append( [operator, op2, -1, op1] )
    # elif operator == 'PARAMETER':
    #     quadruples.append( [operator, op1, -1, op2] )
    # elif operator == 'ERA':
    #     quadruples.append( [operator, -1, -1, op1] )
    # elif operator == 'GOSUB':
    #     quadruples.append( [operator, op2, -1, op1] )
    # elif operator == 'ENDPROC':
    #     quadruples.append( [operator, -1, -1, op1] )
    # elif operator == 'SHOW':
    #     quadruples.append( [operator, -1, -1, op1] )
    # elif operator == 'DECLARE':
    #     quadruples.append( [operator, op1, -1, op2] )
    # elif operator == 'VERIFY':
    #     quadruples.append( [operator, op1, -1, op2] )

    # elif operator == 'ROWOFFSET':
    #     result_type = type1
    #     if current['scope'] == 'global':
    #         temp = get_global_temp(result_type, mem_global_temps)
    #     else:
    #         temp = get_temp(result_type, mem_temps)

    #     quadruples.append( ['ROWOFFSET', op1, op2, temp] )
    #     operands.append( temp )
    #     types.append(result_type)
    # elif operator == 'COLUMNOFFSET':
    #     result_type = type1
    #     if current['scope'] == 'global':
    #         temp = get_global_temp(result_type, mem_global_temps)
    #     else:
    #         temp = get_temp(result_type, mem_temps)

    #     quadruples.append( ['COLUMNOFFSET', op1, op2, temp] )
    #     operands.append(temp)
    #     types.append(result_type)
    # elif operator == 'SUMDIR':
    #     result_type = type1
    #     if current['scope'] == 'global':
    #         temp = get_global_temp(result_type, mem_global_temps)
    #     else:
    #         temp = get_temp(result_type, mem_temps)

    #     quadruples.append( ['SUMDIR', op1, op2, temp] )
    #     operands.append(str( op1 )+'*'+str( temp ))
    #     types.append(type1)
    # else:
    #     if current['scope'] == 'global':
    #         temp = get_global_temp(result_type, mem_global_temps)
    #     else:
    #         temp = get_temp(result_type, mem_temps)

    #     quadruples.append( [operator, op1, op2, temp] )
    #     operands.append(temp)
    #     types.append(result_type)

    # print_quadruples()
    # print_operators()
    # print_operands()
    # if current['scope'] == 'global':
    #     return_global_temp_operands(op1, type1,  op2, type2)
    # else:
    #     if not ( operator == '=' and op1 in temps[type1]['used'] ):
    #         return_temp_operands(op1, type1,  op2, type2)
