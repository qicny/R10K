from instruction import*

class QElem:
    def __init__(self, instr, mask, tag, rs_ready, rt_ready, rd_ready):
        self.instr = instr
        self.rs_ready = rs_ready
        self.rt_ready = rt_ready
        self.rd_ready = rd_ready
        self.mask = mask        #0000-1111
        self.tag = tag          #0-31

    def __repr__(self):
        return ('queue element(instr=%s rs_ready=%s rs_ready=%s rd_ready=%s mask=%s tag=%s)' 
            % (repr(self.instr), repr(self.rs_ready), repr(self.rt_ready), repr(self.rd_ready), repr(self.mask), repr(self.tag)))


class Queue:
    def __init__(self, bbit):
        self.queue = []
        self.max_size = 16
        self.bt = bbit

    def __repr__(self):
        return str(self.queue)


    def Insert(self, instr, mask, tag, rs_ready, rt_ready, rd_ready):
        if(len(self.queue)==self.max_size):
            print ("\t\t\tQueue is full")
            return 0
        else:
            ins = QElem(instr, mask, tag, rs_ready, rt_ready, rd_ready)
            self.queue.append(ins)
            return 1

    def isFull(self):
        if(len(self.queue)==self.max_size):
            return 1
        else:
            return 0

    def freeSlots(self):
        return (self.max_size-len(self.queue))

class IntegerQueue(Queue):
    def Remove(self):
        if(len(self.queue)==0):
            print ("\t\t\tInteger queue is empty")
            return None, None
        else:
            alu1, alu2 = None, None
            for each in self.queue:
                rs_ready = self.bt.is_busy(each.instr.rs)
                rt_ready = self.bt.is_busy(each.instr.rt)
                if(not rs_ready and not rt_ready and each.instr.type=='B'):
                    alu1 = each
                    break
            for each in self.queue:
                rs_ready = self.bt.is_busy(each.instr.rs)
                rt_ready = self.bt.is_busy(each.instr.rt)
                if(not rs_ready and not rt_ready and each.instr.type=='I'):
                    alu2 = each
                    break
            if(alu1): #B present
                self.queue.remove(alu1)
                if(alu2): #B and A present
                    self.queue.remove(alu2)
                return alu1, alu2
            else: #B not present
                if(alu2): #B not present and A present
                    self.queue.remove(alu2)
                    for each in self.queue:
                        rs_ready = self.bt.is_busy(each.instr.rs)
                        rt_ready = self.bt.is_busy(each.instr.rt)
                        if(not rs_ready and not rt_ready and each.instr.type=='I'):
                            alu1 = each
                            break
                    if(alu1):
                        self.queue.remove(alu1)
                    return alu1, alu2
                else: #B not present and A not present
                    return alu1, alu2                 
                
            
class FPQueue(Queue):
    def Remove(self):
        if(len(self.queue)==0):
            print ("\t\t\tFloating point queue is empty")
            return None, None
        else:
            add, mult = None, None
            for each in self.queue:
                rs_ready = self.bt.is_busy(each.instr.rs)
                rt_ready = self.bt.is_busy(each.instr.rt)
                if(not rs_ready and not rt_ready and each.instr.type=='A'):
                    add = each
                    break
            if(add): self.queue.remove(add)
            for each in self.queue:
                rs_ready = self.bt.is_busy(each.instr.rs)
                rt_ready = self.bt.is_busy(each.instr.rt)
                if(not rs_ready and not rt_ready and each.instr.type=='M'):
                    mult = each
                    break
            if(mult): self.queue.remove(mult)
            return add, mult
    
class AddressQueue(Queue): 
    def __init__(self, bbit):
        self.queue = [] #address calculation queue
        self.max_size = 16
        self.bt = bbit

    def Remove(self):
        if(len(self.queue)==0):
            print ("\t\t\tAddress queue is empty")
            return None
        else:
            ls = None
            for each in self.queue:
                rs_ready = self.bt.is_busy(each.instr.rs)
                rt_ready = self.bt.is_busy(each.instr.rt)
                if(not rt_ready and each.instr.type=='L'):
                    ls = each
                    break
                elif(not rt_ready and not rs_ready and each.instr.type=='S'):
                    ls = each
                    break
            if(ls): self.queue.remove(ls)
            return ls        
            
    
    