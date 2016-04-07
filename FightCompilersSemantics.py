class Semantics(object):

    def __init__(self):
        self.procs = {} #Diccionario de procedimientos
        self.var = {}   #Diccionario que guarda la "tabla" de variables. Este va dentro de procs con id = var_dict
        self.current_fid = "" #Guarda el id fe la funcion actual

    # Agrega nuevo valor al diccionario de procedimientos
    def add_procs_to_dict(self, fid, ftipo, fparams, fdict):
        proc_dict = {}
        proc_dict[fid] = {
        'Tipo': ftipo,
        'Params': fparams,
        'Var_Table': fdict
        }
        return proc_dict

    # Agrega nueva variable al diccionario de variables
    def add_vars_to_dict(self, vtipo, vsize_1, vsize_2):
        var_dict = {}
        var_dict = {
            #'Nombre' : vid,
            'Tipo' : vtipo,
            'Size_1' : vsize_1,
            'Size_2' : vsize_2
            }
        return var_dict

    #Revisa si existe el id en el diccionario de procedimientos
    def proc_exists_in_dict(self, fid):
        if fid in self.procs:
            return True
        else:
            return False

    #Revisa si existe el id en el diccionario de variables
    def var_exists_in_dict(self, vid):
        return True
    
