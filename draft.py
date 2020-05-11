class ObjectifyContractVisitor(object):

    def __init__(self, node):
        self._node = node
        self.name = node.name

        self.dependencies = []
        self.stateVars = {}
        self.names = {}
        self.enums = {}
        self.structs = {}
        self.mappings = {}
        self.events = {}
        self.modifiers = {}
        self.functions = {}
        self.constructor = None
        self.inherited_names = {}


    def visitEnumDefinition(self, _node):
        self.enums[_node.name]=_node
        self.names[_node.name]=_node

    def visitStructDefinition(self, _node):
        self.structs[_node.name]=_node
        self.names[_node.name]=_node

    def visitConstructorDefinition(self, _node):
        self.constructor = _node


    def visitStateVariableDeclaration(self, _node):

        class VarDecVisitor(object):

            def __init__(self, current_contract):
                self._current_contract = current_contract

            def visitVariableDeclaration(self, __node):
                self._current_contract.stateVars[__node.name] = __node
                self._current_contract.names[__node.name] = __node

        visit(_node, VarDecVisitor(self))

    def visitEventDefinition(self, _node):

        class EventFunctionVisitor(object):
            def __init__(self, node):
                self.arguments = {}
                self.declarations = {}
                self._node = node

            def visitVariableDeclaration(self, __node):
                self.arguments[__node.name] = __node
                self.declarations[__node.name] = __node

        current_function = EventFunctionVisitor(_node)
        visit(_node, current_function)
        self.names[_node.name] = current_function
        self.events[_node.name] = current_function


    def visitFunctionDefinition(self, _node, _definition_type=None):

        class FunctionObject(object):

            def __init__(self, node):
                self._node = node
                if(node.type=="FunctionDefinition"):
                    self.visibility = node.visibility
                    self.stateMutability = node.stateMutability
                self.arguments = {}
                self.returns = {}
                self.declarations = {}
                self.identifiers = []

        class FunctionArgumentVisitor(object):

            def __init__(self):
                self.parameters = {}

            def visitParameter(self, __node):
                self.parameters[__node.name] = __node

        class VarDecVisitor(object):

            def __init__(self):
                self.variable_declarations = {}

            def visitVariableDeclaration(self, __node):
                self.variable_declarations[__node.name] = __node

        class IdentifierDecVisitor(object):

            def __init__(self):
                self.idents = []

            def visitIdentifier(self, __node):
                self.idents.append(__node)

            def visitAssemblyCall(self, __node):
                self.idents.append(__node)


        current_function = FunctionObject(_node)
        self.names[_node.name] = current_function
        if _definition_type=="ModifierDefinition":
            self.modifiers[_node.name] = current_function
        else:
            self.functions[_node.name] = current_function

        ## get parameters
        funcargvisitor = FunctionArgumentVisitor()
        visit(_node.parameters, funcargvisitor)
        current_function.arguments = funcargvisitor.parameters
        current_function.declarations.update(current_function.arguments)


        ## get returnParams
        if _node.get("returnParameters"):
            # because modifiers dont
            funcargvisitor = FunctionArgumentVisitor()
            visit(_node.returnParameters, funcargvisitor)
            current_function.returns = funcargvisitor.parameters
            current_function.declarations.update(current_function.returns)


        ## get vardecs in body
        vardecs = VarDecVisitor()
        visit(_node.body, vardecs)
        current_function.declarations.update(vardecs.variable_declarations)

        ## get all identifiers
        idents = IdentifierDecVisitor()
        visit(_node, idents)
        current_function.identifiers = idents

    def visitModifierDefinition(self, _node):
        return self.visitFunctionDefinition(_node, "ModifierDefinition")


class ObjectifySourceUnitVisitor(object):

    def __init__(self, node):
        self._node = node
        self.imports = []
        self.pragmas = []
        self.contracts = {}

        self._current_contract = None

    def visitPragmaDirective(self, node):
        self.pragmas.append(node)

    def visitImportDirective(self, node):
        self.imports.append(node)

    def visitContractDefinition(self, node):
        self.contracts[node.name] = ObjectifyContractVisitor(node)
        self._current_contract = self.contracts[node.name]

        # subparse the contracts //slightly inefficient but more readable :)
        visit(node, self.contracts[node.name])