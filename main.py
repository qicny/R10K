from processor import *

f = open('debug','w')
filename = raw_input()
p = Processor(filename)
p.Run10kRun()
