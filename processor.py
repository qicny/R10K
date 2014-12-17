from queues import *
from active_list import *
from fetch import *
from decode import *
from issue import *
from execunits import *
from mapping import *
from registers import *
from helper import *
from copy import deepcopy

sep = '**********************************'
line = '----------------------------------'
all_stages = {'fetch':[], 'decode':[], 'issue':[], 'alu1':None, 'alu2':None, 
'alu1_write':None, 'alu2_write':None, 'ls1':None, 'ls2':None, 'ls_write':None, 
'fpa_1':None, 'fpa_2':None, 'fpa_3':None, 'fpa_write':None, 'fpm_1':None, 
'fpm_2':None, 'fpm_3':None, 'fpm_write':None}

class Processor:  
    def __init__(self, name):
        self.BS = []
        self.active = ActiveList()
        self.bbit = BusyTable()
        self.aqueue = AddressQueue(self.bbit)
        self.fqueue = FPQueue(self.bbit)
        self.iqueue = IntegerQueue(self.bbit)
        self.map = Map()
        self.flist = FreeList()
        
        self.funit = Fetch(name)
        self.dunit = Decode(self.map,self.flist, self.aqueue, self.fqueue, self.iqueue, self.bbit, self.active)
        self.iunit = Issue(self.active, self.aqueue, self.fqueue, self.iqueue, self.bbit)
        self.alu1 = ALU1(self.bbit, self.active)
        self.alu2 = ALU2(self.bbit, self.active)
        self.fpa = FPA(self.bbit, self.active)
        self.fpm = FPM(self.bbit, self.active)
        self.ls = LS(self.bbit, self.active)

    def printFreeList(self, cycle):
        print("Cycle " + str(cycle) + ": free list at the end of cycle")
        print "\t\t\t", self.flist.list

    def printMapping(self, cycle): 
        print("Cycle " + str(cycle) + ": mapping at the end of cycle")
        keys = self.map.map.keys()
        for each in keys:
            if(each!=self.map.map[each]):
                print "\t\t\t", each, self.map.map[each]
    
    def Run10kRun(self):
        print(sep) 
        bypass_alu1, bypass_alu2, alu1_write, alu2_write = None, None, None, None
        bypass_ls1, bypass_ls2, ls_write = None, None, None
        val_fpa_stage1, bypass_fpa_stage2, bypass_fpa_stage3, fpa_write = None, None, None, None
        val_fpm_stage1, bypass_fpm_stage2, bypass_fpm_stage3, fpm_write = None, None, None, None
        to_decode, renamed, old_phys, logical = [], [], [], []
        to_execute = {'alu1':None, 'alu2':None, 'a':None, 'm':None, 'ls':None}
        cycle = 0
        matrix = []
        while True:
            this_cycle = {}

            #Execute stage 4#
            print("Cycle " + str(cycle) + ": execute stage 4")
            fpa_write = self.fpa.write(bypass_fpa_stage3)
            fpm_write = self.fpm.write(bypass_fpm_stage3)

            #Execute stage 3#
            print("Cycle " + str(cycle) + ": execute stage 3")
            bypass_fpa_stage3 = self.fpa.pack(bypass_fpa_stage2)
            bypass_fpm_stage3 = self.fpm.pack(bypass_fpm_stage2)
            ls_write = self.ls.write(bypass_ls2)  
            this_cycle['fpa_3'], this_cycle['fpm_3'] = bypass_fpa_stage3, bypass_fpm_stage3

            #Execute stage 2#
            print("Cycle " + str(cycle) + ": execute stage 2")
            alu1_write = self.alu1.write(bypass_alu1)
            alu2_write = self.alu2.write(bypass_alu2)
            bypass_fpa_stage2 = self.fpa.add(val_fpa_stage1)
            bypass_fpm_stage2 = self.fpm.sum(val_fpm_stage1)
            bypass_ls2 = self.ls.LS2(bypass_ls1)
            this_cycle['fpa_2'], this_cycle['fpm_2'], this_cycle['ls2'] = bypass_fpa_stage2, bypass_fpm_stage2, bypass_ls2

            #Execute stage 1#
            print("Cycle " + str(cycle) + ": execute stage 1")
            bypass_alu1 = self.alu1.do(to_execute['alu1'])
            bypass_alu2 = self.alu2.do(to_execute['alu2'])
            val_fpa_stage1 = self.fpa.alignment(to_execute['a'])
            val_fpm_stage1 = self.fpm.multiply(to_execute['m'])
            bypass_ls1 = self.ls.LS1(to_execute['ls'])
            this_cycle['alu1'], this_cycle['alu2'] = bypass_alu1, bypass_alu2
            this_cycle['fpa_1'], this_cycle['fpm_1'] = val_fpa_stage1, val_fpm_stage1
            this_cycle['ls1'] = bypass_ls1

            #Issue#
            print("Cycle " + str(cycle) + ": issue stage")
            issued, to_execute = self.iunit.do(renamed, old_phys, logical)
            this_cycle['issue'] = issued

            #Decode#
            print("Cycle " + str(cycle) + ": decode stage")
            (renamed, old_phys, logical) = self.dunit.calc(to_decode)
            this_cycle['decode'] = renamed

            #Fetch#
            print("Cycle " + str(cycle) + ": fetch stage")
            (to_decode, fetch_buffer) = self.funit.do()
            this_cycle['fetch'] = to_decode

            #Active list commit
            committed = self.active.commit()
            #print committed
            this_cycle['committed'] = committed

            print(line)
            self.printFreeList(cycle)
            self.printMapping(cycle)
            print this_cycle
            matrix.append(this_cycle)
            print self.active.active_list
            cycle = cycle + 1 
            print(sep)
            if not (to_decode or renamed or not self.active.isEmpty()):          
                print "Done! Done! Done!\n"
                break      
        
        printPipelineDiagram(matrix, cycle)







#all_stages = {'fetch':[], 'decode':[], 'issue':[]  


            
        