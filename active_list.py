class ActiveListElem:
    def __init__(self, ins, done, itype, logreg, oldphys, tag):
        self.ins = ins
        self.tag = tag
        self.done = done
        self.itype = itype
        self.logreg = logreg
        self.oldphys = oldphys
    def __repr__(self):
        return ('active list element(tag=%s done=%s itype=%s logreg=%s oldphys=%s)' 
            % (repr(self.tag), repr(self.done), repr(self.itype), repr(self.logreg), repr(self.oldphys)))

class ActiveList:
    def __init__(self):
        self.active_list = []
        self.max_size = 32
    
    def Insert(self, inst, done, itype, logreg, oldphys):
        if(len(self.active_list)==self.max_size):
            print ("Active list is full")
            return None
        elif(len(self.active_list)==0):
            tag = 0
            ins = ActiveListElem(inst, done, itype, logreg, oldphys, tag)
            self.active_list.append(ins)
        else:
            tag = self.active_list[-1].tag + 1
            ins = ActiveListElem(inst, done, itype, logreg, oldphys, tag)
            self.active_list.append(ins)
            return tag
    
    def Remove(self):
        if(len(self.active_list)==0):
            print ("Active list is empty")
            return 0
        else:
            ins_to_commit = self.active_list[0]
            self.active_list = self.active_list[1:]
            return 1

    def setDone(self, done):    
        ins = done.instr
        for each in self.active_list:
            if(each.ins==ins):
                each.done = 1
                break

    def commit(self):
        committed = []
        size = min(4, len(self.active_list))
        for i in range(size):
            elem = self.active_list[i]
            if(not elem.done):
                break
            else:
                committed.append(elem.ins)
        num_committed = len(committed)
        self.active_list = self.active_list[num_committed:]
        return committed

    def isEmpty(self):
        if(len(self.active_list)==0):
            return True
        else:
            return False

    def isFull(self):
        if(len(self.active_list)==self.max_size):
            return True
        else:
            return False


