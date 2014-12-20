import sys

def inmask(ins, mins):
    print "\t\t\t ins is", ins
    if not ins:
        return 0
    mask = ins.mask
    for each in mask:
        if(each.ins is mins):
            print "\t\t\tInstruction came after mispredicted branch", ins
            return 1
    return 0


def mispredict(mins, active, iq, fq, aq, free, dunit, funit, bs, map):
    #Flush active list and queues, free physical registers
    old = []
    for each in active.active_list:
        if(each.ins is mins):
            break
        else:
            old.append(each.ins)
    ins_before_branch = len(old)
    to_flush = active.active_list[ins_before_branch+1:]
    active.active_list = active.active_list[0:ins_before_branch]
    not_flushed = []
    for each in to_flush:
        ins = each.ins
        if(ins.type in ['L','S']):
            if not(aq.Delete(ins)):
                not_flushed.append(ins)
            else:
                if(ins.type=='L'):
                    free.free_phys(ins.rd)
        elif(ins.type in ['A','M']):
            if not(fq.Delete(ins)):
                not_flushed.append(ins)
            else:
                free.free_phys(ins.rd)
        elif(ins.type in ['I','B']):
            if not(iq.Delete(ins)):
                not_flushed.append(ins)
            else:
                if(ins.type=='I'):
                    free.free_phys(ins.rd)
    #Empty decode buffer
    dunit.renamed = []
    dunit.old_physical = []
    dunit.logical = []
    dunit.stack = []
            
    #Update fetch unit
    lnum = mins.rd
    funit.lnum = lnum
    funit.instructions = funit.store[funit.lnum:]
    if(funit.instructions[0][-1]=='1'): 
        i_to_flip = funit.instructions[0]
        i_new = i_to_flip[0:-1] + '0'
        funit.instructions[0]= i_new
    if(funit.instructions[0][-2]=='1'): 
        i_to_flip = funit.instructions[0]
        i_new = i_to_flip[0:-2] + '0' + i_to_flip[-1]
        funit.instructions[0] = i_new
    funit.IB = []

    #mapping
    before_mins = []
    print "\t\t\tBranch stack is:", bs.bstack
    for each in bs.bstack:
        print each
        if(each.ins is mins):
            break
        else:
            before_mins.append(each)
    map = each.old_map
    bs.bstack = bs.bstack[0:len(before_mins)]


def stage(s, ins):
            try:
                if(s['fpm_3'].instr is ins): return 'M3'
            except: pass 
            try:
                if(s['fpm_2'].instr is ins): return 'M2'
            except: pass 
            try:
                if(s['fpm_1'].instr is ins): return 'M1'
            except: pass 
            try:
                if(s['fpa_3'].instr is ins): return 'A3'
            except: pass
            try:
                if(s['fpa_2'].instr is ins): return 'A2'
            except: pass
            try:
                if(s['fpa_1'].instr is ins): return 'A1'
            except: pass
            try:
                if(s['ls2'].instr is ins): return 'LS'
            except: pass 
            try:
                if(s['ls1'].instr is ins): return 'A'
            except: pass
            try:
                if(s['alu1'].instr is ins): return 'E'
            except: pass 
            try:
                if(s['alu2'].instr is ins): return 'E'
            except: pass 
            if(ins in s['fetch']): return 'F'
            if(ins in s['decode']): return 'D'
            if(ins in s['issue']): return 'I'
            if(ins in s['committed']): return 'C'
            return '_'

def printPipelineDiagram(matrix, cycle, f):
    ilist = []
    for each in matrix:
        ilist.extend(each['fetch'])

    sys.stdout.write("{:<12}".format('instruction'))
    f.write("{:<12}".format('instruction'))

    for c in range(cycle):
        sys.stdout.write("{:<3}".format(str(c)))
        f.write("{:<3}".format(str(c)))
    print '\n'
    f.write('\n')
    for i in range(len(ilist)):
        ins = ilist[i]
        sys.stdout.write("{:<12}".format(ins.type))
        f.write("{:<12}".format(ins.type))
        for c in range(cycle):
            stages = matrix[c]
            sys.stdout.write("{:<3}".format(stage(stages,ins)))
            f.write("{:<3}".format(stage(stages,ins)))
        print '\n'
        f.write('\n')
