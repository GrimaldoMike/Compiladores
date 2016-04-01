import To_Do_lists
#Se inicializa el directorio de procedimientos

#proc_dict = {}
#var_dict = {}
#current_fid = ""

#Se graba un diccionario en el archivo json
def writeToFile(diccionario):
    print("3")
    print (diccionario)
    print("4")
    f = open('workfile.txt', 'w')
    f.write(str(diccionario))
    f.close()

def readFromFile():
    data = {}
    f = open('workfile.txt', 'r')
    print ("5")
    print (f.read()) # display data read
    print ("6")
    data = f.read()
    #print (data.update(f.read()))
    f.close()
    print ("7")
    print (data)
    print ("8")
    return data

# Se inserta el procedimiento 
def add_procs_to_dict(fid, ftipo, fparams, fdict):
    proc_dict = {}
    proc_dict[fid] = {
        'Tipo' : ftipo,
        'Params' : fparams,
        'Var_dict' : fdict
    }
    #current_fid = fid
    if (fid == ""):
        print("no jalo1")
    else:
        print("si jalo1")
    #To_Do_lists.writeToFile(proc_dict)
    return proc_dict    

# Se insertan variables al procedimiento
def add_vars_to_dict(fid, vid, vtipo, vparams):
    var_dict = {
        'Nombre' : vid,
        'Tipo' : vtipo,
        'Params' : vparams
        }
    proc_dict = To_Do_lists.readFromFile()
    #print ("1")
    #print (proc_dict)
    print ("2")
    print(fid)
    print cd ("3")
    #proc_dict[fid]['Var_dict'] =  var_dict 
    print (proc_dict)
    return proc_dict



#Revisa si existe el id en el diccionario de procedimientos
def proc_exists_in_dict(fid):
    return True
    
#Revisa si existe el id en el diccionario de variables
def var_exists_in_dict(vid):
    return True

#dict.append(funcion de agregar(sus vars))



#	f = open('workfile.json', 'r')
#	print (f.readlines())
#	f.close()
	#return x

    
