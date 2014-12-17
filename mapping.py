class Mapping:
    def __init__(self):
        self.map = {}
        for i in range(32):
            self.map[i] = -1
            
    def add_mapping(self, logical, physical):
        self.map[logical] = physical

    def remove_mapping(self, logical, physical):
        self.map[logical] = -1
        

class FreeList:
    def __init__(self):
        self.list = []
        for i in range(32):
            self.list.append(i)
    
    def get_physreg(self):
        if(len(self.list)==0):
            return -1
        else:
            return self.list.pop()
            
    def free_physreg(self, f):
        self.list.append(f)