class Exec:
    def __init__(self, bt, alist):
        self.bt = bt
        self.alist = alist

class ALU1(Exec):
    def do(self, inst,):
        if inst: 
            print("\t\t\tExecuting in ALU1")
            self.bt.unset_busy(inst.instr.rd)
        return inst
        
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
            print("\t\t\tExecuting in FPM multiply")
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
    def LS1(self, inst):
        if inst: 
            print("\t\t\tAddress calculation in LS")
        return inst

    def LS2(self, inst):
        if inst: 
            print("\t\t\t" + inst.instr.type + "in LS")
            if(inst.instr.type=='L'):
                self.bt.unset_busy(inst.instr.rd)
        return inst
    
    def write(self, inst):
        if inst: 
            print("Writing LS result")
            self.alist.setDone(inst)
        return inst