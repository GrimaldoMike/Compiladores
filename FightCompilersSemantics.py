class Semantics(object):
    
    def __init__(self):
        self.procsGlobal = {} #Diccionario de procedimientos globales
        self.procsLocal = {} #Diccionario de procedimientos locales
        self.var = {}   #Diccionario que guarda la "tabla" de variables. Este va dentro de procs con id = var_dict
        self.current_fid = "" #Guarda el id fe la funcion actual

    # Agrega nuevo valor al diccionario de procedimientos
    def add_procs_to_dict(self, fid, ftipo, fparams, fdirI, fdict):
        proc_dict = {}
        proc_dict[fid] = {
        'Tipo': ftipo,
        '#Params': fparams,
        'DireccionInicio': fdirI,
        'Var_Table': fdict
        }
        return proc_dict

    # Agrega nueva variable al diccionario de variables
    def add_vars_to_dict(self, vtipo, vsize_1, vsize_2, fdirI):
        var_dict = {}
        var_dict = {
            #'Nombre' : vid,
            'Tipo' : vtipo,
            'Size_1' : vsize_1,
            'Size_2' : vsize_2,
            'DireccionInicio': fdirI
            }
        return var_dict
        
    #Revisa si existe el id en el diccionario de procedimientos
    # def proc_exists_in_dict(self, fid):
    #  if fid in self.procs:
    #   return True
    #  else:
    #   return False

    # #Revisa si existe el id en el diccionario de variables
    #  def var_exists_in_dict(self, vid):
    #   if vid in self.procs.keys():
    #    return True
    #   else:
    #    return False
      

semantics_cube = {
    # logical operators
    ('int', 'log', 'int') : 'bool',
    ('int', 'log', 'bool') : 'bool',
    ('int', 'log', 'float') : 'bool',
    ('int', 'log', 'string') : 'bool',
    ('int', 'log', 'char') : 'bool',
    ('bool', 'log', 'float') : 'bool',
    ('bool', 'log', 'char') : 'bool',
    ('bool', 'log', 'string') : 'bool',
    ('bool', 'log', 'bool') : 'bool',
    ('char', 'log', 'float') : 'bool',
    ('char', 'log', 'string') : 'bool',
    ('char', 'log', 'char') : 'bool',
    ('string', 'log', 'float') : 'bool',
    ('string', 'log', 'string') : 'bool',
    ('float', 'log', 'float') : 'bool',

    # comparators
    ('int', 'comp', 'int') : 'bool',
   #('int', 'comp', 'string') : 'bool',
    ('int', 'comp', 'char') : 'bool',
    ('int', 'comp', 'bool') : 'bool',
    ('int', 'comp', 'float') : 'bool',

    ('float', 'comp', 'float') : 'bool',

    ('bool', 'comp', 'bool') : 'bool',

    ('char', 'comp', 'char') : 'bool',
    ('char', 'comp', 'bool') : 'bool',
    ('char', 'comp', 'float') : 'bool',
   #('string', 'comp', 'string') : 'bool',

    # int with ___
    ('int', '+', 'int') : 'int',
    ('int', '+', 'string') : 'string',
    ('int', '+', 'char') : 'int',
    ('int', '+', 'bool') : 'int',
    ('int', '+', 'float') : 'float',

    ('int', '-', 'int') : 'int',
   #('int', '-', 'string') : 'string',
    ('int', '-', 'char') : 'int',
    ('int', '-', 'bool') : 'int',
    ('int', '-', 'float') : 'float',

    ('int', '*', 'int') : 'int',
   #('int', '*', 'string') : 'string',
    ('int', '*', 'char') : 'int',
   #('int', '*', 'bool') : 'int',
    ('int', '*', 'float') : 'float',

    ('int', '/', 'int') : 'int',
   #('int', '/', 'string') : 'string',
    ('int', '/', 'char') : 'int',
   #('int', '/', 'bool') : 'int',
    ('int', '/', 'float') : 'float',

   #('int', '=', 'string') : 'string',
    ('int', '=', 'int') : 'int',
    ('int', '=', 'char') : 'int',
   #('int', '=', 'bool') : 'int',
    ('int', '=', 'float') : 'int',

    # string with ___
    ('string', '+', 'string') : 'string',
    ('string', '+', 'char') : 'string',
    ('string', '+', 'bool') : 'string',
    ('string', '+', 'float') : 'string',

   #('string', '-', 'string') : 'string',
   #('string', '-', 'string') : 'string',
   #('string', '-', 'bool') : 'string',
   #('string', '-', 'char') : 'string',
   #('string', '-', 'float') : 'float',

   #('string', '*', 'string') : 'string',
   #('string', '*', 'string') : 'string',
   #('string', '*', 'char') : 'string',
   #('string', '*', 'bool') : 'string',
   #('string', '*', 'float') : 'float',

   #('string', '/', 'string') : 'string',
   #('string', '/', 'string') : 'string',
   #('string', '/', 'char') : 'string',
   #('string', '/', 'bool') : 'string',
   #('string', '/', 'float') : 'float',

    ('string', '=', 'string') : 'string',
    ('string', '=', 'char') : 'string',
    ('string', '=', 'bool') : 'string',
    ('string', '=', 'float') : 'string',

    # char with __
    ('char', '+', 'char') : 'int',
    ('char', '+', 'string') : 'string',
   #('char', '+', 'bool') : 'char',
    ('char', '+', 'float') : 'float',

    ('char', '-', 'char') : 'int',
   #('char', '-', 'string') : 'string',
   #('char', '-', 'bool') : 'char',
    ('char', '-', 'float') : 'float',

    ('char', '*', 'char') : 'int',
   #('char', '*', 'string') : 'string',
   #('char', '*', 'char') : 'char',
   #('char', '*', 'bool') : 'char',
    ('char', '*', 'float') : 'float',

    ('char', '/', 'char') : 'char',
   #('char', '/', 'string') : 'string',
   #('char', '/', 'char') : 'char',
   #('char', '/', 'bool') : 'char',
    ('char', '/', 'float') : 'float',

   #('char', '=', 'string') : 'string',
    ('char', '=', 'char') : 'char',
    ('char', '=', 'int') : 'char',
   #('char', '=', 'bool') : 'char',
   #('char', '=', 'float') : 'char',

    # bool with ___
    ('bool', '+', 'bool') : 'int',
    ('bool', '+', 'char') : 'int',
    ('bool', '+', 'float') : 'float',

    ('bool', '-', 'bool') : 'int',
   #('bool', '-', 'string') : 'string',
    ('bool', '-', 'char') : 'int',
    ('bool', '-', 'float') : 'float',

    ('bool', '*', 'bool') : 'int',
   #('bool', '*', 'string') : 'string',
    ('bool', '*', 'char') : 'int',
   #('bool', '*', 'bool') : 'bool',
    ('bool', '*', 'float') : 'float',

    ('bool', '/', 'bool') : 'int',
   #('bool', '/', 'string') : 'string',
    ('bool', '/', 'char') : 'int',
   #('bool', '/', 'bool') : 'bool',
    ('bool', '/', 'float') : 'float',

    ('bool', '=', 'string') : 'bool',
    ('bool', '=', 'bool') : 'bool',
    ('bool', '=', 'char') : 'bool',
    ('bool', '=', 'float') : 'bool',

    # float with float
    ('float', '=', 'int') : 'float',
    ('float', '=', 'float') : 'float',
    ('float', '+', 'float') : 'float',
    ('float', '-', 'float') : 'float',
    ('float', '*', 'float') : 'float',
    ('float', '/', 'float') : 'float'

}

