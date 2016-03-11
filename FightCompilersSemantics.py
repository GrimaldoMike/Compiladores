#Se inicializa el directorio de procedimientos
proc_dict = {}
current_fid = ""

# Se inserta el procedimiento 
def add_procs_to_dict(fid, ftipo, fparams, fdict):
    proc_dict[fid] = {
        'Tipo' : ftipo,
        'Params' : fparams,
        'Var_dict' : fdict
    }
    current_fid = fid
    return proc_dict

# Se insertan variables al procedimiento
def add_vars_to_dict(vid, vtipo, vparams):
    proc_dict[current_fid]['Var_dict'] = {
        'Nombre' : vid,
        'Tipo' : vtipo,
        'Params' : vparams,
    }
    return proc_dict

#Revisa si existe el id en el diccionario de procedimientos
def proc_exists_in_dict(fid):
    return true
    
#Revisa si existe el id en el diccionario de variables
def var_exists_in_dict(vid):
    return true

#dict.append(funcion de agregar(sus vars))




