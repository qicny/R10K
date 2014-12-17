class Issue:
    def __init__(self, alist, aq, fq, iq, busy):
        self.alist = alist
        self.aq = aq
        self.fq = fq
        self.iq = iq
        self.busy = busy
        print("Issue unit initialized")
    
    def do(self, renamed_ins, old_phys, logical):
        #Add decoded instructions to lists
        issued = []
        for i in range(len(renamed_ins)):
            ins = renamed_ins[i]
            mask = 0 #junk for now
            tag = self.alist.Insert(ins, 0, ins.type, logical[i], old_phys[i])
            rs = self.busy.is_busy(ins.rs)
            rt = self.busy.is_busy(ins.rt)
            rd = self.busy.is_busy(ins.rd)
            if ins.type in ['I', 'B']:
                print "\t\t\tIssuing ", ins
                self.iq.Insert(ins, mask, tag, rs, rt, rd)
            elif ins.type in ['A','M']:
                print "\t\t\tIssuing ", ins
                self.fq.Insert(ins, mask, tag, rs, rt, rd)
            elif ins.type in ['L','S']:
                print "\t\t\tIssuing ", ins
                self.aq.Insert(ins, mask, tag, rs, rt, rd)
            issued.append(ins)

        #Select instructions for execution
        to_execute = {}
        i = self.iq.Remove()
        to_execute['alu1'], to_execute['alu2'] = i[0], i[1]

        f = self.fq.Remove()
        to_execute['a'], to_execute['m'] = f[0], f[1]

        a = self.aq.Remove()
        to_execute['ls'] = a
        return issued, to_execute

    def write_half(self):
        a = 1
	    #print("Issue cycle write second half started")
    	