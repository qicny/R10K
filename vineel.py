import itertools
import sys
from collections import deque
class Instr: #class for instruction
    def __init__(self, trace_line, pos):
    	self.text = trace_line.strip()
        brk = self.text.split()
        self.op = brk[0] #how are they indexed 0-31 ?
        self.pos = pos
        self.rs = '{0:05b}'.format(int(brk[1], 16))
        self.rt = '{0:05b}'.format(int(brk[2], 16))
        self.rd = '{0:05b}'.format(int(brk[3], 16))
        #print self.rs, " ", self.rt, " ", self.rd, " "
        if(self.op in "LS"):
            self.extra = int(brk[4])
            self.ex_bits = "1000"
        elif(self.op in "B"):
            self.extra = int(brk[4])
            self.ex_bits = "0010"
        elif(self.op in "AM"):
            self.ex_bits = "0100"
        elif (self.op in "I"):
            self.ex_bits = "0010"
    def __repr__(self):
        return self.text
    def set_extra_bits(self, eb):
        self.ex_bits = eb
    def toggle_extra(self):
        self.extra = self.extra ^ 1

class ActListMem: #active list member
	def __init__(self,  ins = None, ld = "", oprn = ""):
		self.done = 0
		self.instr = ins
		self.logical_dest = ld
		self.old_physical_reg_num = oprn

class InstrQMem: #active list member
	def __init__(self,  ins = None, rs = "",  rt="", ld = "" ):
		self.done = 0
		self.instr = ins
		self.prs = rs #physical
		self.prt = rt #physical
		self.pld = ld #physical

class BrStack:
	#When a branch is decoded, processor saves it's state in a four entry branch stack. This contains alternate branch 
	#address, complete copies of integer and floating point map tables - the information is distributed near it copies
	def __init__(self, alt =-1, ins = None, rm = None):
		self.instr = ins 
		self.regmap =  rm
		self.altaddr = alt 


class MIPS_R10000:
	def __init__(self, num_physical = 64, rob_size = 32):
		self.instr_pipe = {} #instruction set
		self.pc = 0 #Program Counter
		self.clk = 0 ##current clock cycle
		self.instr_r = [None]*4 ## after FF - 4 instructions at a time by fetch
		self.instr_n = [None]*4 ## input to FF - 4 instructions at a time by fetch

		self.instr2decode_r = [None]*4 ##after FF - these are the instructions in decode stage loaded from fetch
		self.instr2decode_n = [None]*4 ##input to FF - same as above
		
		#branch history table - indexed by 11:3 - No need to implement for the project
		
		self.InstrBuff = 0 ## 8 word instruction buffer
		
		#Free Lists - stores list of currently unassigned physical registers
		self.FreeList = [''.join(it) for it in itertools.product(['0', '1'], repeat=6)] #physical registes free
		self.FreeListPtr = 0 #ptr to the netxt free list
		
		#Physical Registers - initilaized with 0
		self.PhyRegisters =  dict([(i,0) for i in self.FreeList]) #all physical registers in the mips
		
		#Bust Bit Tables
		self.BusyBit = dict([(i,0) for i in self.FreeList]) ##busy bit to denote if a a physica register is free
        
		#Active Lists - records all instructions currently active within the processor
		#remove when mispredict or graduate or exception
		self.ActList = dict([(i,None) for i in itertools.product(['0', '1'], repeat=5)])
		self.ActListPtr = (0,0) ## (p1, p2) p1 corresponds to the current pos for instruction to insert, p2 corresponds to the oldest instruction which is still not coommitted
		
		#Register Map Tables
		self.RegMapTable = {}
		for i in range(0,32):
			self.RegMapTable['r'+str(i)] = self.FreeList[self.FreeListPtr]
			self.FreeListPtr = (self.FreeListPtr + 1)%64
        
		#instruction queues
		self.IntQ  = deque( maxlen=16 )
		self.FltQ  = deque( maxlen=16 )
		self.AddrQ = deque( maxlen=16 )
		
		#Exec_units
		#ALU1, #ALU2
		self.ALU1 = None
		self.ALU2 = None
		#FPAdd, #FPMul
		self.FPAdd = None
		self.FPMul = None
        
		self.ALU1Pos = self.ALU2Pos = self.FPAddPos = self.FPMulPos = None
		self.FPAddCnt = self.FPMulCnt = 0

	def instr_fetch_edge(self):
   		self.instr_r = self.instr_n[:]
		
		
	#insert into queue, read busy bit
	def decode_calc(self):	
	#decode, renames the instructions and calculates target address for jump,  branch instructions 
	#decodes 4 instruction in parallel during stage 2 and writes them into instruction queue at the start of stage 3
	
		for instr in self.instr2decode_r:
			#if queue/list full 
			if(instr == None):
				break 
			physical_rs = self.RegMapTable[instr.rs]
			physical_rt = self.RegMapTable[instr.rt]
			physical_rd_old = self.RegMapTable[instr.rt]
			physical_rd_new = None
			if(instr.op in "IAM"):
				if(len(self.FreeList) > 0):
					physical_rd_new = self.FreeList[self.FreeListPtr]
					self.BusyBit[physical_rd_new] = 1
					self.FreeListPtr = (self.FreeListPtr  + 1)%num_physical
			self.ActList[self.ActListPtr[0]] = ActListMem(instr, physical_rd_new, physical_rd_old)
			self.ActListPtr[0] = (self.ActListPtr[0] + 1)%rob_size
			
			if(instr.op in  "IB"):
				self.IntQ.append(InstrQMem(instr, physical_rs, physical_rt, physical_rd_new))
			
			elif(instr.op in  "AM"):
				self.FltQ.append(InstrQMem(instr, physical_rs, physical_rt, physical_rd_new))
			
			elif(instr.op in  "LS"):
				self.AddrQ.append(InstrQMem(instr, physical_rs, physical_rt, physical_rd_new))
			
			spare = None
			for i in list(self.intQ):
				if(self.BusyBit[i.prs] == 0 and self.BusyBit[i.prt] == 0):
					if(i.instr.op == 'B' and ALU1Pos == None) :
						ALU1Pos = i
					elif (ALU2Pos == None) :
						ALU2Pos = i
					elif (spare == None):
						spare = i
			if(self.ALU1Pos==None):
				self.ALU1Pos = spare
			
			for i in list(self.fltQ):
				if(self.BusyBit[i.prs] == 0 and self.BusyBit[i.prt] == 0):
					if(i.instr.op == 'A' and FPAddPos == None) :
						FPAddPos = i
					elif(i.instr.op == 'M' and FPMulPos == None) :
						FPMulPos = i
						
	def decode_edge(self):	
		instr2decode_r = instr2decode_n[:]

	    
	def instr_fetch_calc(self):
	#fetches and aligns next 4 instructions
		del self.instr_n
		i1 = self.instr_pipe[self.pc] if (self.pc in instr_pipe) else None
		self.pc = self.increment_pc(self.pc)
		i2 = self.instr_pipe[self.pc] if (self.pc in instr_pipe) else None
		self.pc = self.increment_pc(self.pc)
		i3 = self.instr_pipe[self.pc] if (self.pc in instr_pipe) else None
		self.pc = self.increment_pc(self.pc)
		i4 = self.instr_pipe[self.pc] if (self.pc in instr_pipe) else None
		self.pc = self.increment_pc(self.pc)
		self.instr_n = [i1, i2, i3, i4]


	def exec_calc(self):
		#check for integer scheduling - two branch instructions cant be resolved
		if(self.ALU1 != None):
			#remove the instruction 
			self.BusyBit[ALU1.prd] = 0 
			#busy bit of target address to 0
			# done bit for active list = 1 
			self.ActList[self.ALU1.instr] = 1
			self.PhyRegisters[self.ALU1.rd] = self.PhyRegisters[self.ALU1.rs] + self.PhyRegisters[self.ALU1.rt] 
			
		self.ALU1 = self.ALU1Pos	
		
		#check for integer scheduling - two branch instructions cant be resolved
		if(self.ALU2 != None):
			#remove the instruction 
			self.BusyBit[ALU2.prd] = 0 
			#busy bit of target address to 0
			# done bit for active list = 1 
			self.ActList[self.ALU2.instr] = 1
			self.PhyRegisters[self.ALU2.rd] = self.PhyRegisters[self.ALU2.rs] + self.PhyRegisters[self.ALU2.rt] 
			
		self.ALU2 = self.ALU2Pos	
		
		
		
		if(FPMul != None):
			if(FPMulCnt == 0): 
				self.FPMulCnt = 1 
			else:
				self.FPMulCnt = 0 
				self.BusyBit[self.FPMul.prd] = 0 
				#busy bit of target address to 0
				# done bit for active list = 1 
				self.ActList[self.FPMul.instr] = 1
				self.PhyRegisters[self.FPMul.rd] = self.PhyRegisters[self.FPMul.rs] + self.PhyRegisters[self.FPMul.rt] 
				
		if(FPMulCnt == 0):
			FPMul = FPMulPos
			
		if(FPAdd != None):
			if(FPAddCnt == 0): 
				self.FPMulCnt = 1 
			else:
				self.FPAddCnt = 0 
				self.BusyBit[self.FPAdd.prd] = 0 
				#busy bit of target address to 0
				# done bit for active list = 1 
				self.ActList[self.FPAdd.instr] = 1
				self.PhyRegisters[self.FPAdd.rd] = self.PhyRegisters[self.FPAdd.rs] + self.PhyRegisters[self.FPAdd.rt] 
				
		if(FPAddCnt == 0):
			FPAdd = FPAddPos
	def load_instructions (self):
		#print ("Enter trace file to read instructions - ")
		trace_file = 'tracefile.txt'
		num_tries = 3
		file_found = False

		while(num_tries!=0 and  not file_found):
			num_tries = num_tries - 1
			try:
				f = open(trace_file)
			except IOError :
				print "I/O error: cannot open '", trace_file, "'"
				print "Enter trace file to read instructions - "
				trace_file = raw_input()
				continue
			except:
				print "Unexpected error:", sys.exc_info()[0]
				return
			file_found = True
		if not file_found : return
		cur_mem = '0'*32
		for num, line in enumerate(f):
			self.instr_pipe[cur_mem] = Instr(line, num )
			#cur_mem = self.increment_pc(cur_mem)
		f.close()
		print "Instructions loaded successfully (y)"

	def increment_pc (self, cur_pc):
		return cur_pc + 1

class IntQueue: #integer queue
	def __init__(self,  ins = "", ld = "00000", oprn = "0000000"):
		self.done = 0
		self.instr = ins
		self.logical_dest = ld
		self.old_physical_reg_num = oprn


