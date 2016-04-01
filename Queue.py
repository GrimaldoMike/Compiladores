class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop() 

    def size(self):
        return len(self.items)
        
    def proc_exists_in_dict(self, f_id):
        for y in self.items:
            if y == f_id:
                return True
        return False
        
    def vars_exists_in_list(self, v_id):
        for y in self.items:
            if y == v_id:
                return True
        return False
        
#{   'Juego_A': {   'Params': 'void',
#                  'Tipo': 'juego',
#                   'Var_Table': {   'Nombre': 'x',
#                                    'Size_1': '4',
#                                    'Size_2': None,
#                                   'Tipo': 'int'}}}