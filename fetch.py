from instruction import*

class Fetch:
    def __init__(self, name):
        self.tfile = open(name,'r')
        self.instructions = self.tfile.readlines()
        self.store = self.instructions[:]
        self.IB = []
        self.lnum = 0
        print("Fetch unit initialized")
        
    def do(self):
        self.IB.extend(self.instructions[0:4])
        self.instructions = self.instructions[4:]
        fetched = self.IB[0:4]
        self.IB = self.IB[4:]
        fetched_ins = []
        for each in fetched:
            if(each=='\n'):
                break
            print ("\t\t\t" + "Fetching ins " + each.strip())
            ins = each.strip().split()
            if(len(ins)==4):
                ins.append('-1')
            if(ins[0] is not 'L'):
                if(ins[0]=='B'):
                    fetched_ins.append(Instruction(ins[0], int(ins[1]), int(ins[2]), int(self.lnum), ins[4]))
                else:
                    fetched_ins.append(Instruction(ins[0], int(ins[1]), int(ins[2]), int(ins[3]), ins[4]))
            else:
                ins[3]=0
                fetched_ins.append(Instruction(ins[0], int(ins[3]), int(ins[1]), int(ins[2]), ins[4])) 
            self.lnum = self.lnum + 1
        return fetched_ins


        