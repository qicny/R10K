class Map:
    def __init__(self):
        self.map = {}
        for i in range(0,32):
            self.map[i] = i
            
    def get_map(self):
        return self.map
            
    def get_mapping(self, logical):
        return self.map[logical]
            
    def add_mapping(self, logical, physical):
        self.map[logical] = physical

    def remove_mapping(self, logical, physical):
        self.map[logical] = -1
        
        
class FreeList:
    def __init__(self):
        self.list = []
        for i in range(32,64):
            self.list.append(i)
            
    def get_phyreg(self):
       if(len(self.list)==0):
           return -1
       else:
           return self.list.pop()

    def free_phys(self, old_phys):
        self.list.append(old_phys)
    
    def remove_mapping(self, logical, physical):
        self.map[logical] = -1

    def freeRegisters(self):
        return len(self.list)
        
class BusyTable:
    def __init__(self):
        self.bbit = {}
        for i in range(0,64):
            self.bbit[i] = 0
            
    def is_busy(self, reg):
        return self.bbit[reg]
        
    def set_busy(self, reg):
        if(reg): self.bbit[reg] = 1
    
    def unset_busy(self, reg):
        self.bbit[reg] = 0