from graphviz import Digraph
import re

class Set:
    def __init__(self):
        self.elements = []

    def Intersection(self, leafs):
        intersection = Set()
        for elemento in self.elements:
            if elemento in leafs.elements:
                intersection.elements.append(elemento)
        return intersection

    def Union(self, leafs):
        union = Set()
        union.elements = self.elements + leafs.elements
        return union

    def Difference(self, leafs):
        diference = Set()
        for elemento in self.elements:
            if elemento not in leafs.elements:
                diference.elements.append(elemento)       
        return diference

    def addElement(self, elemento):
        self.elements.append(elemento)

    def rmElement(self, elemento):
        self.elements.remove(elemento)

    def update(self, leafs):
        for elemento in leafs.elements:
            if elemento not in self.elements:
                self.elements.append(elemento)

    def clr(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0
    
    def pop(self):
        return self.elements.pop()

    def Contains(self, elemento):
        return elemento in self.elements
    
    def rmDupe(self):
        self.elements = list(set(self.elements))

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return str(self.elements)


class Node:
    def __init__(self, symbol, leftLeaf=None, rightLeaf=None, number=None):
        self.symbol = symbol
        self.leftLeaf = leftLeaf
        self.rightLeaf = rightLeaf
        self.number = number
        self.nullable = False
        self.first_position  = Set()
        self.last_position  = Set()
        self.next_position  = Set()

    def __str__(self):
        return self.symbol
    
    def is_leaf(self):
        return self.leftLeaf is None and self.rightLeaf is None

class Tree:
    def __init__(self, expression):
        self.expression = expression
        self.node = None
        self.stack = []
        self.connections = []
    
    def build(self, filename="arbol"):
        for symbol in self.expression:
            if symbol == '*':
                self.create_node(symbol)
            elif symbol == '+':
                self.create_node(symbol)
            elif symbol == '?':
                self.create_node(symbol)
            elif symbol == '.':
                self.create_node(symbol)
            elif symbol == '|':
                self.create_node(symbol)
            else:
                self.create_node(symbol)

        self.node = self.stack.pop()
        self.toGraph(self.node, filename)

    def create_node(self, symbol):

        if symbol == '*':
            node = Node(symbol)
            node.leftLeaf = self.stack.pop()
            self.stack.append(node)
        elif symbol == '+':
            symbol_to_add = self.stack[-1]
        
            node = Node("•")
            node.leftLeaf = symbol_to_add
            node.rightLeaf = Node("*")
            node.rightLeaf.leftLeaf = self.stack.pop()
            
            self.stack.append(node)
        elif symbol == '?':
            symbol_to_add = self.stack.pop()

            node = Node("|")
            node.leftLeaf = symbol_to_add
            node.rightLeaf = Node("ε")

            self.stack.append(node)
        elif symbol == '•':
            node = Node(symbol)
            node.rightLeaf = self.stack.pop()
            node.leftLeaf = self.stack.pop()
            self.stack.append(node)
        elif symbol == '|':
            node = Node(symbol)
            node.rightLeaf = self.stack.pop()
            node.leftLeaf = self.stack.pop()
            self.stack.append(node)
        else:
            node = Node(symbol)
            self.stack.append(node)

    def toGraph(self, node, filename="arbol"):
        dot = Digraph(comment='Tree')
        self.GraphNode(node, dot)
        dot.render(filename, view=True)

    def GraphNode(self, node, dot):
        if node is None:
            return

        if(node.symbol == "|" or node.symbol == "•" or node.symbol == "*" or node.symbol == "+" or node.symbol == "?"):
            dot.node(str(id(node)), label=node.symbol)
        else:
            dot.node(str(id(node)), label=(node.symbol))


        if node.leftLeaf is not None:
            self.GraphNode(node.leftLeaf, dot)
            if (str(id(node)), str(id(node.leftLeaf))) not in self.connections:
                dot.edge(str(id(node)), str(id(node.leftLeaf)))
                self.connections.append((str(id(node)), str(id(node.leftLeaf))))

        if node.rightLeaf is not None:
            self.GraphNode(node.rightLeaf, dot)
            if (str(id(node)), str(id(node.rightLeaf))) not in self.connections:
                dot.edge(str(id(node)), str(id(node.rightLeaf)))
                self.connections.append((str(id(node)), str(id(node.rightLeaf))))
