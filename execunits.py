class Exec:
    def __init__(self, bt, alist):
        self.bt = bt
        self.alist = alist

class ALU1(Exec):
    def __init__(self, bt, alist, bs):
        self.bt = bt
        self.alist = alist
        self.bs = bs

    def do(self, inst):
        mispredict = None
        if inst: 
            print("\t\t\tExecuting in ALU1")
            if(inst.instr.type=='I'):
                self.bt.unset_busy(inst.instr.rd)
            else:
                if(int(inst.instr.extra)): #mispredict
                    mispredict = inst.instr
                    #self.bs.flushOnMispredict(inst)
        return (inst, mispredict)
        
    def write(self, inst):
        if inst: 
            print("\t\t\tWriting ALU1 result")
            self.alist.setDone(inst)
        return inst

class ALU2(Exec):
    def do(self, inst):
        if inst: 
            print("\t\t\tExecuting in ALU2")
            self.bt.unset_busy(inst.instr.rd)
        return inst
        
    def write(self, inst):
        if inst: 
            print("\t\t\tWriting ALU2 result")
            self.alist.setDone(inst)
        return inst

class FPA(Exec):
    def alignment(self, inst):
        if inst: 
            print("\t\t\tExecuting in FPA alignment")
        return inst

    def add(self, inst):
        if inst: 
            print("\t\t\tExecuting in FPA add")
            self.bt.unset_busy(inst.instr.rd)  
        return inst
        
    def pack(self, inst):
        if inst: 
            print("\t\t\tExecuting in FPA pack")      
        return inst
        
    def write(self, inst):        
        if inst: 
            print("\t\t\tWriting FPA result")
            self.alist.setDone(inst)
        return inst
        
class FPM(Exec):
    
    def multiply(self, inst):
        if inst: 
            print "\t\t\tExecuting in FPM multiply: ", inst
        return inst

    def sum(self, inst):
        if inst: 
            print("\t\t\tExecuting in FPM sum")
            self.bt.unset_busy(inst.instr.rd)  
        return inst
    
    def pack(self, inst):
        if inst: 
            print("\t\t\tExecuting in FPM pack")
        return inst
        
    def write(self, inst):
        if inst: 
            print("\t\t\tWriting FPM result")
            self.alist.setDone(inst)
        return inst
        
class LS(Exec):
    def __init__(self, bt, alist, lsq):
        self.bt = bt
        self.alist = alist
        self.lsq = lsq

    def LS1(self, inst):
        if inst: 
            print("\t\t\tAddress calculation in LS")
            self.lsq.setADone(inst)
        return inst

    def LS2(self):
        inst = self.lsq.Remove() 
        print "\t\t\tExecuting in LS:", inst
        if(inst and inst.instr.type=='L'):
                self.bt.unset_busy(inst.instr.rd)
        return inst
    
    def write(self, inst):
        if inst: 
            print("Writing LS result")
            self.alist.setDone(inst)
        return inst