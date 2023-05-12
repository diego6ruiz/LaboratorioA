from Tree import *
from State import *
from graphviz import Digraph

class Automaton:
    def __init__(self):
        self.states = Set()
        self.finalStates = Set()
        self.symbols = Set()
        self.initialState = None
        self.transitions = []
        self.tokens = []

    def addState(self, estado):
        self.states.addElement(estado)

    def addFinalState(self, estado):
        self.finalStates.addElement(estado)

    def addSymbol(self, simbolo):
        self.symbols.addElement(simbolo)

    def addTransition(self, origen, destino, simbolo):
        self.transitions.append((origen, destino, simbolo))

    def setSingleFinalState(self, estado):
        self.finalStates.Clear()
        self.finalStates.addElement(estado)

    def toString(self):
        #for estado in self.states.elements:
            #print(estado)
        #for transition in self.transitions:
            #print(transition[0], " -> ", transition[1], " -> ", transition[2])
        #print(self.initialState)
        #for estado_final in self.finalStates.elements:
            #print(estado_final)
        print()
           
    def toGraph(self,automaton, name):
        g = Digraph('AFN', filename=name)
        g.attr(rankdir='LR')

        for state in automaton.states.elements:
            if state.type == 'inicial':
                g.node(str(state.id), shape='circle')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final_inicial':
                g.node(str(state.id), shape='doublecircle')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final':
                g.node(str(state.id), shape='doublecircle')
            else:
                g.node(str(state.id), shape='circle')
                

        for transition in automaton.transitions:
            g.edge(str(transition[0].id), str(transition[1].id), label=transition[2])

        g.view()

    
    def epsilonClosure(self, estado):
        visited = Set()
        stack = [estado]
        result = Set()

        while stack:
            estado = stack.pop(0)
            if estado in visited.elements:
                continue
            visited.addElement(estado)
            result.addElement(estado)

            for transicion in self.transitions:
                if transicion[0].id == estado.id:
                    if (transicion[2] == 'ε' and transicion[1].id != estado.id and transicion[1] not in visited.elements):
                        stack.append(transicion[1])

        return result
    
    def move(self, states, symbol):

        move = Set()
        for state in states.elements:
            for transition in self.transitions:
                if transition[0].id == state.id and transition[2] == symbol:
                    move.addElement(transition[1])
        return move



class Direct():
    def __init__(self):
        self.counter = 1
        self.table = []
        self.automata = Automaton()

    def Direct(self, postfix_expression):

        postfix_expression.append("#")
        postfix_expression.append("•")

        tree = Tree(postfix_expression)
        tree.build("arbol_direct")
               
        direct = self.directAfd(tree.node)
        direct.toString()
        direct.toGraph(direct, "Direct")

        return direct
    
    def directAfd(self, node):
        self.numberNodes(node)
        self.checkNullable(node)
        self.checkFirstPos(node)
        self.checkLastPos(node)
        self.checkFollowPos(node)

        self.addSymbols(node)

        counter = 0

        # initstate  es first_position del nodo raiz
        final = False
        for element in node.first_position.elements:
            if "#" in element.symbol:
                final = True
        
        if final:
            initstate = State(counter, 'final_inicial',  node.first_position, node.symbol)
            self.automata.finalStates.addElement(initstate)
        else:
            initstate = State(counter,"inicial", node.first_position)

        self.automata.states.addElement(initstate)
        self.automata.initialState = initstate
        counter += 1

        for state in self.automata.states.elements:
            for symbol in self.automata.symbols.elements:
                union = Set()
                for element in state.AFN_states.elements:
                    if symbol == element.symbol:
                        union = union.Union(element.next_position)
                        union = self.clearDuplicates(union)

                if not union.isEmpty():
                    rmDupe = self.stateAlreadyExists(union)

                    if rmDupe is None:

                        final = False
                        token = None

                        for element in union.elements:
                            if "#" in element.symbol:
                                final = True
                                token = element.symbol
                                self.automata.tokens.append(token)

                        if final:
                            new_state = State(counter, 'final', union, token)
                            self.automata.finalStates.addElement(new_state)

                        else:                     
                            new_state = State(counter, 'normal', union)

                        self.automata.states.addElement(new_state)
                        union = Set()
                        counter += 1    

                        self.automata.addTransition(state, new_state, symbol)

                    else:
                        self.automata.addTransition(state, rmDupe, symbol)

        return self.automata
    
    def clearDuplicates(self, set):
        new_set = Set()
        for element in set.elements:
            if not new_set.Contains(element):
                new_set.addElement(element)
        return new_set
                    

    def stateAlreadyExists(self, state):
        for element in self.automata.states.elements:
            if len(state.elements) == len(element.AFN_states.elements):
                if len(state.Difference(element.AFN_states).elements) == 0:
                    return element
        return None       


    def numberNodes(self, node):

        if node.is_leaf():
            if node.symbol != 'ε':
                node.number = self.counter
                self.table.append(node)
                self.counter += 1
        else:
            if (node.leftLeaf != None):
                self.numberNodes(node.leftLeaf)
            if (node.rightLeaf != None):
                self.numberNodes(node.rightLeaf)

    def checkNullable(self, node):
        if node.is_leaf():
            node.nullable = node.symbol == 'ε'
        else:
            if node.symbol == '*':
                self.checkNullable(node.leftLeaf)
                node.nullable = True
                
            elif node.symbol == '+':
                self.checkNullable(node.leftLeaf)
                node.nullable = True
                
            elif node.symbol == '?':
                self.checkNullable(node.leftLeaf)
                node.nullable = True
                
            elif node.symbol == '•':
                self.checkNullable(node.leftLeaf)
                self.checkNullable(node.rightLeaf)

                if node.leftLeaf.nullable and node.rightLeaf.nullable:
                    node.nullable = True
                else:
                    node.nullable = False

            elif node.symbol == '|':
                self.checkNullable(node.leftLeaf)
                self.checkNullable(node.rightLeaf)

                if node.leftLeaf.nullable or node.rightLeaf.nullable:
                    node.nullable = True
                else:
                    node.nullable = False

    def checkFirstPos(self, node):
        if node.is_leaf():
            if node.symbol == 'ε':
                node.first_position = Set()
            else:
                node.first_position.addElement(node)

        else:
            if node.symbol == '*':
                self.checkFirstPos(node.leftLeaf)
                node.first_position = node.leftLeaf.first_position
                
            elif node.symbol == '+':
                self.checkFirstPos(node.leftLeaf)
                node.first_position = node.leftLeaf.first_position
            
            elif node.symbol == '?':
                self.checkFirstPos(node.leftLeaf)
                node.first_position = node.leftLeaf.first_position

            elif node.symbol == '•':
                self.checkFirstPos(node.leftLeaf)
                self.checkFirstPos(node.rightLeaf)

                if node.leftLeaf.nullable:
                    node.first_position = node.leftLeaf.first_position.Union(node.rightLeaf.first_position)
                else:
                    node.first_position = node.leftLeaf.first_position
            elif node.symbol == '|':
                self.checkFirstPos(node.leftLeaf)
                self.checkFirstPos(node.rightLeaf)

                node.first_position = node.leftLeaf.first_position.Union(node.rightLeaf.first_position)

    def checkLastPos(self, node):
        if node.is_leaf():
            if node.symbol == 'ε':
                node.last_position = Set()
            else:
                node.last_position.addElement(node)
        else:
            if node.symbol == '*':
                self.checkLastPos(node.leftLeaf)
                node.last_position = node.leftLeaf.last_position

            elif node.symbol == '+':
                self.checkLastPos(node.leftLeaf)
                node.last_position = node.leftLeaf.last_position

            elif node.symbol == '?':
                self.checkLastPos(node.leftLeaf)
                node.last_position = node.leftLeaf.last_position

            elif node.symbol == '•':
                self.checkLastPos(node.leftLeaf)
                self.checkLastPos(node.rightLeaf)

                if node.rightLeaf.nullable:
                    node.last_position = node.leftLeaf.last_position.Union(node.rightLeaf.last_position)
                else:
                    node.last_position = node.rightLeaf.last_position
            elif node.symbol == '|':
                self.checkLastPos(node.leftLeaf)
                self.checkLastPos(node.rightLeaf)

                node.last_position = node.leftLeaf.last_position.Union(node.rightLeaf.last_position)


    def checkFollowPos(self,node):
        if node.symbol == "•":
            first_pos_right = node.rightLeaf.first_position
            last_pos_left = node.leftLeaf.last_position

            for i in last_pos_left.elements:
                for j in first_pos_right.elements:
                    find_node = self.FindNode(i.number)
                    if(self.nodeAlreadyExists(find_node.next_position, j) == False):
                        find_node.next_position.addElement(j)

            self.checkFollowPos(node.leftLeaf)
            self.checkFollowPos(node.rightLeaf)

        if node.symbol == "*":
            first_pos = node.first_position
            last_pos = node.last_position

            for i in last_pos.elements:
                for j in first_pos.elements:
                    find_node = self.FindNode(i.number)
                    if(self.nodeAlreadyExists(find_node.next_position, j) == False):
                        find_node.next_position.addElement(j)

            self.checkFollowPos(node.leftLeaf)

        if node.symbol == "|":
            self.checkFollowPos(node.leftLeaf)
            self.checkFollowPos(node.rightLeaf)


    def FindNode(self, number):
        for i in self.table:
            if i.number == number:
                return i
            
    def addSymbols(self, node):
        if node.is_leaf():
            if node.symbol != 'ε' and '#' not in node.symbol:
                if node.symbol not in self.automata.symbols.elements:
                    self.automata.symbols.addElement(node.symbol)
        else:
            if (node.leftLeaf != None):
                self.addSymbols(node.leftLeaf)
            if (node.rightLeaf != None):
                self.addSymbols(node.rightLeaf)

    def nodeAlreadyExists(self, nodes, node):
        for element in nodes.elements:
            if element == node:
                return True
        return False

