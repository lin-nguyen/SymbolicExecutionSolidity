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
    def __init__ (self, branch, head,tail, symsLocal=None, symsParam = None, returnVar = None, name = None):
        self.branch= branch
        self.head = head
        self.tail = tail
        self.symsLocal = symsLocal
        self.symsParam = symsParam
        self.returnVar = returnVar  
        self.name = name


class Symbol: 
    def __init__(self, name, value, mType):
        self.name = name
        self.value = value
        self.mType = mType
class SymbolicExecution(BaseVisitor):
    global_envi = FullBranch([Branch([],[])], 0,1)
    syms = []
    def __init__ (self, ast): 
        self.ast = ast
    def printSym(self, lstSym): 
        print([(x.name, x.value, x.mType)for x in lstSym])
    def run(self): 
        
        return self.visit(self.ast,SymbolicExecution.global_envi)
        #self.printSym(self.syms)
        #self.printc(SymbolicExecution.global_envi.branch)
        
        
    def _mapCommasToNulls(self, children):
        if not children or len(children) == 0:
            return []
        values = []
        comma = True

        for el in children:
            if comma:
                if el.getText() == ',':
                    values.append(None)
                else:
                    values.append(el)
                    comma = False
            else:
                if el.getText() != ',':
                    raise Exception('expected comma')

                comma = True

        if comma:
            values.append(None)

        return values
    def _createNode(self, **kwargs):
        ## todo: add loc!
        return Node(**kwargs)
    def visit(self, ast, c):
        if ast is None:
            return None
        #elif isinstance(ast, list):
            #return self._visit_nodes(ast)
        #    return [super().visit(self,x,c) for x in ast  ]
        else:
            return super().visit(self,ast,c)
    def _visit_nodes(self, nodes):
        """
        modified version of visitChildren() that returns an array of results

        :param nodes:
        :return:
        """
        allresults = []
        result = self.defaultResult()
        for c in nodes:
            childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)
            allresults.append(result)
        return allresults
    # ********************************************************
    def visitSourceUnit(self, ast,c):
        #for x in range(0,len(ast)):
        #   self.visit(ast['children'][x],c) 
        listFunc =self.visit(ast['children'][1],c) 
        return listFunc
    def visitPragmaDirective(self, ast, c): 
        return None
    def visitContractDefinition(self, ast, c):
        #type, name, subNodes, baseContracts , kinds
        #return self.visit(ast['subNodes'], c)
        #print(ast['type'])
        #print([x['type'] for x in ast['subNodes']])
        listFunc = []
        for x in ast['subNodes']:
            if x['type'] == 'FunctionDefinition':
                
                newFunc = FullBranch([Branch([],[])], 0,1, [], [])
                self.visit(x, newFunc)
                listFunc.append(newFunc)
            else: 
                self.visit(x, c)
        return listFunc
    def printKeys(self, ast): 
        print([ x for x in ast.keys() ])
    def visitFunctionDefinition(self, ast,c):
        #'type', 'name', 'parameters', 
        #'returnParameters', 'body', 'visibility', 
        # 'modifiers', 'isConstructor', 'stateMutability'
        if ast.isConstructor == True: return self.visitFunctionDefinitionConstructor( ast,c)
        params = ast['parameters']['parameters']
        for x in params: 
            c.symsParam.append(Symbol(x['name'], None,x['typeName']['name']))
        self.printSym(c.symsParam)
        c.returnVar = ( ast['returnParameters']['parameters'][0]['name'])
        c.name = ast['name']
        self.visit(ast['body'], c)
    def visitFunctionCall(self, ast, c):
        name = ast['expression']['name']
        argu = [self.visit(x,c) for x in ast['arguments']]
        ret = name + '('
        if argu:
            for x in argu:
                ret+= x+','
            ret = ret[:-1]
        ret+=')'
        return ret
    def visitFunctionDefinitionConstructor(self, ast,c):        
        pass
    def visitStateVariableDeclaration(self, ast,c): 
        name = ast['variables'][0]['name']
        #iniVal = self.visit(ast['variables'][0]['initialValue'])
        expr= ast['variables'][0]['expression']
        mType =ast['variables'][0]['typeName']['name']
        if expr!=None: 
            expr= self.visit(ast['variables'][0]['expression'],c)
        if c.symsLocal==None: 
            self.syms.append(Symbol(name, expr,mType))
        else: 
            c.symsLocal.append(Symbol(name, expr,mType))
    
    def visitBlock(self, ast, c):
        #listKey: ['type', 'statements']
        lst=[]
        for x in ast['statements']:
            #print(x['type'])
            self.visit(x, c)
    def visitIfStatement(self, ast, c): 
        #listKey: ['type', 'condition', 'TrueBody', 'FalseBody']
        
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

    def visitExpressionStatement(self, ast, c): 
        left = self.visit(ast['expression']['left'],c)
        right= self.visit(ast['expression']['right'],c)
        op = ast['expression']['operator']

        for x in c.branch[c.head: c.tail]: 
            x.Stmts.append(left+op+right)
    def visitForStatement(self, ast, c): 
        #['type', 'initExpression', 'conditionExpression', 'loopExpression', 'body']
        name, initValue = self.visitForInit(ast["initExpression"],c)
        op, finalValue = self.visitCond(ast["conditionExpression"],c)
        step = self.visitStep(ast["loopExpression"],c)
        listStmts = self.visitBodyFor(ast['body'], c)
        lstStmts=''
        for x in listStmts:
            lstStmts += '\t\t'+x+'\n' 
        for x in c.branch[c.head: c.tail]: 
            x.Stmts.append("for "+ name + " in range(" +str(initValue)+ ','+ str(finalValue)+ ','
                            + str(step)+ "):\n"
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
    def visitExpression(self, ast, c): 
        op = ast['operator']; 
        symL = self.visit(ast['left'],c); 
        symR = self.visit(ast['right'],c)
        return symL+op+symR
        pass
    def visitIdentifier(self,ast,c):
        return ast['name']
    def visitNumberLiteral(self,ast,c): 
        return ast['number']
    def visitBooleanLiteral(self, ast,c):
        return str(ast['value'])