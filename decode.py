''' I / rs, rt / rd
        A / rs, rt / rd
        M / rs, rt / rd
        L / rs / rt ---> rs->rd, rt->rs
        S / rs / rt 
        B / rs, rt / --
''' 

class Decode:
    def __init__(self, map, free, aq, fq, iq, bt, active):
        self.map = map
        self.free = free
        self.aq = aq
        self.fq = fq
        self.iq = iq
        self.bt = bt
        self.active = active
        self.dbuffer = []
        self.decoded = []
        self.renamed = []
        self.old_physical = []
        print("Decode unit initialized")

    def rename(self):
        renamed = []
        old_physical = []
        logical = []
        for ins in self.dbuffer[0:4]:
            if(self.active.isFull()):
                break
            ins.rs, ins.rt = self.map.get_mapping(ins.rs), self.map.get_mapping(ins.rt)
            log = ins.rd
            if(ins.type not in ['S', 'B'] and log):
                f = self.free.get_phyreg()
                self.bt.set_busy(f)
                old_phys = self.map.get_mapping(ins.rd)
                self.map.add_mapping(ins.rd, f)
                ins.rd = f
            else:
                old_phys = -1
            renamed.append(ins)
            old_physical.append(old_phys)
            logical.append(log)
        num_decoded = len(renamed)
        self.dbuffer = self.dbuffer[num_decoded:]

        return (renamed, old_physical, logical)
    
    def calc(self, to_decode):
        self.dbuffer.extend(to_decode)
        (renamed, old_phys, logical) = self.rename()
        return (renamed, old_phys, logical)
    
                
            
            
            
    