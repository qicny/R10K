class Instruction:
    def __init__(self, type, rs, rt, rd, extra):
        self.type = type
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.extra = extra

    def __repr__(self):
        return ('instruction(type=%s rs=%s rt=%s rd=%s extra=%s)' 
        	% (repr(self.type), repr(self.rs), repr(self.rt), repr(self.rd), repr(self.extra)))           

 