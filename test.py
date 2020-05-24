from solidity_parser import parser
from solidity_parser import symbolic
asttree = parser.parse_file("test.sol")
class UserState: 
    def __init__ (self, adr , balance , token): 
        self.adr = adr 
        self.balance = balance
        self.token = token 
dse = symbolic.SymbolicExecution(asttree)
listFunc= dse.run()
#print(listFunc)
#dse.printc(dse.global_envi.branch)
#dse.printSym(dse.syms)
syms = dse.syms
branchs = listFunc[0].branch
#symsLocal = listFunc[0].symsLocal
#b = branchs[0]
def printSym(lstSym): print([(x.name, x.value, x.mType)for x in lstSym])

for one_func in listFunc:
    nameFile=1
    program = ""
    program+='from z3 import *\n'
    lstParam = ''
        #print(one_func.symsParam.name)
    for x in one_func.symsParam:
        lstParam+= x.name+','
    lstParam = lstParam[:-1]
    for b in one_func.branch:
        symsLocal = one_func.symsLocal
        if lstParam!='':
            program+= 'def '+ one_func.name +'_'+str(nameFile)+'(' + lstParam+ '): \n'
        #printSym(syms)
        for x in syms: 
            program+= '\t'+x.name
            program+= '='
            if  x.value !=None: 
                if x.mType!='address':
                    program+=x.value
                else:
                    program+='"'+x.value +'"'
            else: 
                program+='\t'+'BitVec("'+ x.name + '", 32)'
            program+='\n'
        for x in symsLocal: 
            program+= '\t'+x.name
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
            program+='\t'+x
            program+='\n'
        program+= '\treturn '+ one_func.returnVar + '\n'
        nameFile+=1
    program+= 'def '+ one_func.name +'('+ lstParam+ '):\n'
    nameFile=1
    for x in one_func.branch:
        condition = ''
        for k in x.Conds:
            if k[1]==True: condition+=k[0]
            else : condition+='not '+k[0]
            condition+= ' and '
        condition = condition[:-5]
        program+= '\tif '+ condition +':'+ one_func.name +  '_'+ str(nameFile)+'('+lstParam+')' + '\n'
        nameFile+=1
    f = open(one_func.name+".py", 'w+')
    f.write(program)
    '''
    
    
    program+="finalState = (userBalance, userAdr, userToken)\n"
    program+= "print (finalState)\n"
    '''
    
    #exec(program)
    #print(finalState)