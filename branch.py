class BranchStackElem:   
    def __init__(self, ins, omap, next_line):
        self.ins = ins
        self.old_map = omap
        self.nline = next_line
        self.verified = 0
        self.mispredict = 0

class BranchStack():
    def __init__(self)
        self.bstack = []
        self.max_size = 4

    def Insert(self, ins, omap, next_line):
        if(len(self.bstack)==self.max_size):
            print "\t\t\tBranch stack is full"
            return None   
        new_entry = BranchStackElem(ins, omap, next_line)
        self.bstack.append(new_entry)

    def Verify(self, ins):
        for each in bstack:
            if(each.ins is ins):
                each.verified = 1

    def isFull(self):
        if(len(self.bstack)==self.max_size):
            return 1
        else 
            return 0

    def clearMask(self):
        verified = []
        for each in self.bstack:
            if (each.verified and each.mispredict)

    def flushOnMispredict(ins):
