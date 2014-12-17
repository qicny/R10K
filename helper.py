import sys

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
                if(s['ls2'].instr is ins): return 'LS2'
            except: pass 
            try:
                if(s['ls1'].instr is ins): return 'LS1'
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
        ilist.extend(each['decode'])
    for c in range(cycle):
        sys.stdout.write('%2s' % (str(c)))
        f.write('%2s' % (str(c)))
    print '\n'
    f.write('\n')
    for i in range(len(ilist)):
        ins = ilist[i]
        for c in range(cycle):
            stages = matrix[c]
            sys.stdout.write('%2s' % (stage(stages,ins)))
            f.write('%2s' % (stage(stages,ins)))
        print '\n'
        f.write('\n')
