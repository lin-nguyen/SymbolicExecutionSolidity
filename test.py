from solidity_parser import parser
from solidity_parser import symbolic
asttree = parser.parse_file("test.sol")
class UserState: 
    def __init__ (self, adr , balance , token): 
        self.adr = adr 
        self.balance = balance
        self.token = token 
dse = symbolic.SymbolicExecution(asttree)
dse.run()
#dse.printc(dse.global_envi.branch)
#dse.printSym(dse.syms)
syms = dse.syms
branchs = dse.global_envi.branch

program = ""
program+='from z3 import *\n'
for b in branchs:
    program = ""
    program+='from z3 import *\n'
    for x in syms: 
        program+= x.name
        program+= '='
        if  x.value !=None: 
            if x.mType!='address':
                program+=x.value
            else:
                program+='"'+x.value +'"'
        else: 
            program+='BitVec("'+ x.name + '", 32)'
        program+='\n'

    for x in b.Stmts:
        program+=x
        program+='\n'
    program+="finalState = (userBalance, userAdr, userToken)\n"
    f = open("runSym.py", 'w')
    f.write(program)
    exec(program)
    print(finalState)
