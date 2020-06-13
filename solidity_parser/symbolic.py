#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# part of https://github.com/ConsenSys/python-solidity-parser
# derived from https://github.com/federicobond/solidity-parser-antlr/
#


from antlr4 import *
from solidity_parser.solidity_antlr4.SolidityLexer import SolidityLexer
from solidity_parser.solidity_antlr4.SolidityParser import SolidityParser
from solidity_parser.solidity_antlr4.SolidityVisitor import SolidityVisitor
class BaseVisitor:
    def visit(self, ob, ast, c): 
        return ast.accept(ob, ast,c)
    def visitSourceUnit(self,param):
        return None
class OR: 
    def __init__ (self , left, right): 
        self.left = left
        self.right = right
class Branch: 
    # condition is a list 
    # get all statement 
    def __init__(self, listCond, listStatement):
        self.Conds = listCond
        self.Stmts = listStatement
class FullBranch: 
    def __init__ (self, branch, head,tail, symsLocal=None, symsParam = None, returnVar = None, name = None, globalSym = []):
        self.branch= branch
        self.head = head
        self.tail = tail
        self.symsLocal = symsLocal
        self.symsParam = symsParam
        self.returnVar = returnVar  
        self.name = name
        self.globalSym = globalSym

class Symbol: 
    def __init__(self, name, value, mType):
        self.name = name
        self.value = value
        self.mType = mType
class SymbolicExecution(BaseVisitor):
    global_envi = (FullBranch([Branch([],[])], 0,1), 1, 
                    [('address','self'),('require', 'self')]) # scope = số lần tab
    syms = []
    def __init__ (self, ast, file ): 
        self.ast = ast
        self.file = file
    def printSym(self, lstSym): 
        print([(x.name, x.value, x.mType)for x in lstSym])
    def run(self): 
        
        return self.visit(self.ast,SymbolicExecution.global_envi)
        #self.printSym(self.syms)
        #self.printc(SymbolicExecution.global_envi.branch)

    def visit(self, ast, c):
        if ast is None:
            return None
        #elif isinstance(ast, list):
            #return self._visit_nodes(ast)
        #    return [super().visit(self,x,c) for x in ast  ]
        else:
            return super().visit(self,ast,c)

    # ********************************************************
    def visitSourceUnit(self, ast,c):
        #for x in range(0,len(ast)):
        #   self.visit(ast['children'][x],c) 
        # children[0]: pragma 1
        # children[1]: contract Ownable
        # children[2]: pragma 2
        # children[3]: contract BookStoreInit
        # children[4]: pragma 3
        # children[5]: contract BookStore
        # getAll nameFunction
        listF = c[2]+ self.getNameFunc(ast)
        [self.visit(x,(c[0], c[1], listF )) for x in ast['children']]
        #return listFunc
    def getNameFunc(self, ast): 
        lst=[]
        for x in ast['children']: 
            if x['type']=='ContractDefinition':
                nodes = x['subNodes']
                for node in nodes:
                    if node['type']=='FunctionDefinition':
                        if node['name']: 
                            lst.append((node['name'], 'self'))
        return lst                    
    def visitPragmaDirective(self, ast, c): 
        return None
    def visitContractDefinition(self, ast, c):
        #type, name, subNodes, baseContracts , kinds
        #return self.visit(ast['subNodes'], c)
        #print(ast['type'])
        #print([x['type'] for x in ast['subNodes']])
        #print(ast)
        # some type :StateVariableDeclaration , 
        # EventDefinition, FunctionDefinition, ModifierDefinition
        # InheritanceSpecifier
        InheritanceSpecifier = [x.baseName.namePath for x in ast.baseContracts] 
        baseClass= ''
        if InheritanceSpecifier: 
            baseClass = '('
            for x in InheritanceSpecifier: baseClass+= str (x) +','
            baseClass = baseClass[:-1] + ')'
        else: 
            baseClass = '(base)'
        # header class 
        self.file.write("class " + ast.name +baseClass+":\n")    
        for x in ast['subNodes']:
            newFunc = (FullBranch([Branch([],[])], 0,1, [], [], globalSym=['ownerToOrderList'])
                            ,1
                            ,c[2]
                            ,ast.name)    
            self.visit(x, newFunc)
              
        
    def visitModifierDefinition(self, ast, c): 
        pass
    def visitEventDefinition(self, ast, c):
        pass 
    def printKeys(self, ast): 
        print([ x for x in ast.keys() ])
    def visitFunctionDefinition(self, ast,c):
        #'type', 'name', 'parameters', 
        #'returnParameters', 'body', 'visibility', 
        # 'modifiers', 'isConstructor', 'stateMutability'
        '''for x in params: 
            c.symsParam.append(Symbol(x['name'], None,x['typeName']['name']))
        self.printSym(c.symsParam)
        
        c.returnVar = ( ast['returnParameters']['parameters'][0]['name'])
        c.name = ast['name']
        '''
        if ast['isConstructor'] == True: return self.visitFunctionDefinitionConstructor( ast,c)
        params = ast['parameters']['parameters']
        Name = ast['name']
        params = ast['parameters']['parameters']
        param = [self.visit(x, c) for x in params]
        listArgu = ""
        if param: 
            for x in param: 
                listArgu+= ','+ x
        self.file.write('\tdef '+ Name +   '(self'+ listArgu+ '):\n')
        if(Name =='SendToken'): self.file.write('\t\tsendtoken(_token,_quantity)\n')
        self.visit(ast['body'],(c[0], c[1]+1, c[2], c[3]))
        

    def visitFunctionCall(self, ast, c):
        name = self.visit(ast['expression'],c)
        
        if name == []: return '[]'
        else: 
            argu = [self.visit(x,c) for x in ast['arguments']]
        ret = name + '('
        if argu:
            for x in argu:
                ret+= x+','
            ret = ret[:-1]
        ret+=')'
        if (name,'self') in c[2]:
            return 'self.'+ret    
        return ret
    def visitNewExpression(self, ast,c): 
        return self.visit(ast['typeName'], c )
    def visitArrayTypeName(self, ast, c): 
        return []
    def visitFunctionDefinitionConstructor(self, ast,c):  
        params = ast['parameters']['parameters']
        param = [self.visit(x, c) for x in params]
        listArgu = ""
        if param: 
            for x in param: 
                listArgu+= ','+ x
        self.file.write('\tdef __init__(self'+ listArgu+ '):\n')
        self.visit(ast['body'],(c[0], c[1]+1, c[2], c[3]))
    def visitParameter(self, ast, c): 
        return ast['name'] 

    def visitStateVariableDeclaration(self, ast,c): 
        
        name = ast['variables'][0]['name']

        iniVal = self.visit(ast['initialValue'],c)
        if iniVal ==None: iniVal = 'None'
        '''print( iniVal)
        expr= ast['variables'][0]['expression']
        mType =ast['variables'][0]['typeName']['name']
        if expr!=None: 
            expr= self.visit(ast['variables'][0]['expression'],c)
        if c.symsLocal==None: 
            self.syms.append(Symbol(name, expr,mType))
        else: 
            c.symsLocal.append(Symbol(name, expr,mType))
            '''
        if name not in c[0].globalSym: 

            c[2].insert(0,(name, c[3])) 
            self.file.write(self.Scope(c[1])+name+'='+ iniVal+ '\n')
        return name, iniVal
    def visitVariableDeclarationStatement(self, ast, c):
        name = ast['variables'][0]['name']
        iniVal = self.visit(ast['initialValue'],c)
        if iniVal ==None: iniVal = 'None'
        if name not in c[0].globalSym: 
            c[2].insert(0,(name, 'self'))
            self.file.write(self.Scope(c[1])+ 'self.'+name+'='+ iniVal+ '\n')
        return name, iniVal
    def visitBlock(self, ast, c):
        #listKey: ['type', 'statements']
        lst=[]
        for x in ast['statements']:
            
            stmt = self.visit(x, c)
    def visitReturnStatement(self, ast,c):
        stmt = self.visit(ast['children'],c)
        
        self.file.write(self.Scope(c[1])+ 'return '+ stmt + '\n')
    def visitIfStatement(self, ast, c): 
        #listKey: ['type', 'condition', 'TrueBody', 'FalseBody']
        '''
        cond = self.visit(ast['condition'],c)
        lstBranch = c.branch; tail= c.tail;head = c.head; length= tail-head
        if (ast['FalseBody']!=None):
            for x in range(head, tail):
                lstBranch.insert(tail, Branch(list(lstBranch[x].Conds), list(lstBranch[x].Stmts)))
                #update head and tail 
                head2 = tail
                tail2 = head2+length
            for x in lstBranch[head2:tail2]:
                x.Conds.append((cond, False))
            self.visit( ast['FalseBody'],FullBranch(lstBranch,head2,tail2))
            
        for x in lstBranch[head:tail]:
            x.Conds.append((cond, True))
        self.visit(ast['TrueBody'],FullBranch(lstBranch, head, tail))
        #merge 2 branch
        c.head = head; 
        c.tail = tail2 if (ast['FalseBody']!=None) else tail
        '''
        cond = self.visit(ast['condition'],c)
        self.file.write(self.Scope(c[1])+ 'if '+ cond + ':\n')
        self.visit(ast['TrueBody'], (c[0], c[1]+1, c[2], c[3]))
        if ast['FalseBody']: 
            self.file.write(self.Scope(c[1])+ 'else' + ':\n')
            self.visit(ast['FalseBody'],(c[0], c[1]+1, c[2], c[3]))
    def visitEmitStatement(self, ast, c): 
        pass
    def visitExpressionStatement(self, ast, c): 
        '''
            for x in c.branch[c.head: c.tail]: 
                x.Stmts.append(left+op+right)
        '''
        stmt = self.visit(ast['expression'],c)
        self.file.write(self.Scope(c[1])+stmt+'\n')
    def visitBinaryOperation(self, ast,c):
        left = self.visit(ast['left'],c)
        right= self.visit(ast['right'],c)

        op = ast['operator']
        if op=='&&': op=' and '
        if op=='||': op=' or '
        return left+op+right
    def visitUnaryOperation(self, ast,c):
        sub= self.visit(ast['subExpression'],c)
        op = ast['operator']
        if op=='!': op=' not '
        if op=='++': op='+=1' ; return sub+op
        return op+sub
    def visitElementaryTypeNameExpression(self, ast, c): 
        return ast['typeName']['name']
    def Scope(self, scope): 
        tab = ''
        for x in range(0, scope): 
            tab+='\t'
        return tab
    def visitMemberAccess(self, ast,c): 
        if ast['memberName']=='transfer':
            return 'self.address('+self.visit(ast['expression'],c)+')'+'.'+ast['memberName']
        return self.visit(ast['expression'],c)+'.'+ast['memberName']
    def visitIndexAccess(self, ast, c):
        return self.visit(ast['base'], c)+'['+ self.visit(ast['index'], c) +']'
    def visitForStatement(self, ast, c): 
        #['type', 'initExpression', 'conditionExpression', 'loopExpression', 'body']
        name, initValue = self.visitForInit(ast["initExpression"],c)
        op, finalValue = self.visitCond(ast["conditionExpression"],c)
        step = self.visitStep(ast["loopExpression"],c)
        listStmts = self.visitBodyFor(ast['body'], c)
        lstStmts=''
        for x in listStmts:
            lstStmts += x+';' 
        for x in c.branch[c.head: c.tail]: 
            x.Stmts.append("for "+ name + " in range(" +str(initValue)+ ','+ str(finalValue)+ ','
                            + str(step)+ "):"
                            + lstStmts
                            )
    def visitBodyFor(self, ast, c): 
        stmts = [self.visitStatementFor(x,c) for x in ast['statements']] 
        return stmts
    def visitStatementFor(self, ast,c):
        left = self.visit(ast['expression']['left'],c)
        right= self.visit(ast['expression']['right'],c)
        op = ast['expression']['operator']
        return left+op+right    
    def visitForInit(self, ast,c):
        name =  ast['variables'][0]['name']
        initValue = ast['initialValue']['number']
        return name, initValue
    def visitCond(self, ast, c):
        op = ast['operator']
        finalValue = self.visit(ast['right'],c)
        return op, finalValue
    def visitStep(self, ast, c):
        if ast['expression']['operator']=='++':
            return 1

    def printc(self, c): 
        for x in c: 
            print(x.Conds,x.Stmts)
            print('\n')
    def visitIdentifier(self,ast,c):
        for x in c[2]: 
            name = x[0]
            Type = x[1]
            if ast['name'] == name: 
                return Type +'.'+ ast['name']
        return ast['name']
    def visitNumberLiteral(self,ast,c): 
        if ast['number'][:2]=='0x': return '"'+ast['number']+'"'
        return ast['number']
    def visitBooleanLiteral(self, ast,c):
        return str(ast['value'])
    def visitStringLiteral(self, ast,c):
        return "'"+ ast['value']+"'"
    