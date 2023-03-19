import functools
from Leaf import Leaf
from graphviz import Digraph

class DFA_Node():
    def __init__(self, name, nodos, isDirect = False):
        self.name = name
        self.id = None
        self.transitions = []
        self.isMarked = False
        self.isFinal = False
        self.conjunto_nodos = nodos

        if not isDirect:
            self.CreateID(nodos)
        else:
            self.CreateID2(nodos)

    # Metodo para crear un ID unico para el nodo.
    def CreateID(self, nodos):
        a = [n.id for n in nodos]
        a.sort()
        a = [str(i) for i in a]
        self.id = ', '.join(a)

    # Metodo para crear ID unico para hoja de arbol sintactico.
    def CreateID2(self, nodos):
        a = [n for n in nodos]
        a.sort()
        a = [str(i) for i in a]
        self.id = ', '.join(a)

    # Metodo para marcar un estado que ya ha sido visitado.
    def Mark(self):
        self.isMarked = True

    # Metodo para definir un estado como de aceptacion.
    def isAcceptingState(self):
        self.isFinal = True

class Leaf():
    def __init__(self, name, position, is_operator, children, nullable):
        self.name = name
        self.position = position
        self.is_operator = is_operator
        self.children = children
        self.nullable = nullable
        self.first_pos = []
        self.last_pos = []
        self.follow_pos = []
        if self.name == 'ε':
            self.nullable = True
        self.AddFirstPos()
        self.AddLastPos()


    def GetName(self):
        name = f'{self.name} - {self.position}'
        return name

    def AddFirstPos(self):
        if self.is_operator:
            if self.name == '|':
                self.first_pos = self.children[0].first_pos + self.children[1].first_pos
            elif self.name == '.':
                if self.children[0].nullable:
                    self.first_pos = self.children[0].first_pos + self.children[1].first_pos
                else:
                    self.first_pos += self.children[0].first_pos
            elif self.name == '*':
                self.first_pos += self.children[0].first_pos
        else:
            if self.name != 'ε':
                self.first_pos.append(self.position)

    def AddLastPos(self):
        if self.is_operator:
            if self.name == '|':
                self.last_pos = self.children[0].last_pos + self.children[1].last_pos
            elif self.name == '.':
                if self.children[1].nullable:
                    self.last_pos = self.children[0].last_pos + self.children[1].last_pos
                else:
                    self.last_pos += self.children[1].last_pos
            elif self.name == '*':
                self.last_pos += self.children[0].last_pos
        else:
            if self.name != 'ε':
                self.last_pos.append(self.position)

epsilon = 'ε'
class DFA():
    def __init__(self, regex):
        # variable defining
        self.count = 0
        self.rounds = 1
        self.states = []
        self.symbols = []
        self.transitions = []
        self.acc_states = []
        self.init_state = None
        self.nodes = [] # Array that contains leaves
        self.root = None
        self.id = 0
        self.final_state = None
        self.follow_pos = {}

        #1. If n is a cat-node with left child c1 and right child c2 and i is a position in lastpos(c1), then all positions in firstpos(c2) are in followpos(i).
        # 2. If n is a star-node and i is a position in lastpos(n), then all positions in firstpos(n) are in followpos(i).
        # 3. Now that we have seen the rules for computing firstpos and lastpos, we now proceed to calculate the values of the same for the syntax tree of the given regular expression (a|b)*abb#.
        
        # Se procesa la expresion 
        print(regex)
        self.build_tree(regex)

        for n in self.nodes:
            if n.name == '#':
                self.final_state = n.position
                break

        self.calculate_followpow()
        self.create_dfa()
    
    # Implementacion de la creacion del arbol sintactico
    def build_tree(self, regex):
        my_stack = []
        my_ops = []
        try:
            for character in regex:
                if self.is_char_symbol(character):
                    my_stack.append(character)
                elif character == '(':
                    my_ops.append(character)
                elif character == ')':
                    last_in = self.peek_stack(my_ops)
                    while last_in is not None and last_in != '(':
                        my_root = self.operate(my_ops, my_stack)
                        my_stack.append(my_root)
                        last_in = self.peek_stack(my_ops)
                    my_ops.pop()
                else:
                    last_in = self.peek_stack(my_ops)
                    while last_in is not None and last_in not in '()' and self.preceding_operator(last_in, character):
                        my_root = self.operate(my_ops, my_stack)
                        my_stack.append(my_root)
                        last_in = self.peek_stack(my_ops)
                    my_ops.append(character)

            while self.peek_stack(my_ops) is not None:
                my_root = self.operate(my_ops, my_stack)
                my_stack.append(my_root)
            self.root = my_stack.pop()
        except:
            print("error de sintaxis")


    def peek_stack(self, stack):
        if stack:
            return stack[-1] #Last element
        else:
            return None
        
        # Implementacion de las operaciones del arbol sintactico
    def operate(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = '@'

        if right not in self.symbols and right != epsilon and right != '@' and right != '#':
            self.symbols.append(right)

        if operator != '*' and operator != '+' and operator != '?':
            left = values.pop()

            if left not in self.symbols and left != epsilon and left != '@' and left != '#':
                self.symbols.append(left)

        if operator == '|': 
            return self.or_operation(left, right)
        elif operator == '.': 
            return self.concatenation(left, right)
        elif operator == '*': 
            return self.kleene_closure(right)

    # Operacion kleen
    def kleene_closure(self, leaf):
        operator = '*'
        try: 
            if isinstance(leaf, Leaf):
                root = Leaf(operator, None, True, [leaf], True)
                self.nodes += [root]
                return root

            else:
                id_left = None
                if leaf != epsilon:
                    id_left = self.get_id()

                left_leaf = Leaf(leaf, id_left, False, [], False)
                root = Leaf(operator, None, True, [left_leaf], True)
                self.nodes += [left_leaf, root]

                return root
        except:
            print("Error en operacion *")

    # Operacion OR
    def or_operation(self, left, right):
        operator = '|'
        try:
            if isinstance(left, Leaf) and isinstance(right, Leaf):
                root = Leaf(operator, None, True, [left, right], left.nullable or right.nullable)
                self.nodes += [root]
                return root

            elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
                id_left = None
                id_right = None
                if left != epsilon:
                    id_left = self.get_id()
                if right != epsilon:
                    id_right = self.get_id()

                left_leaf = Leaf(left, id_left, False, [], False)
                right_leaf = Leaf(right, id_right, False, [], False)
                root = Leaf(operator, None, True, [left_leaf, right_leaf], left_leaf.nullable or right_leaf.nullable)

                self.nodes += [left_leaf, right_leaf, root]

                return root

            elif isinstance(left, Leaf) and not isinstance(right, Leaf):
                id_right = None
                if right != epsilon:
                    id_right = self.get_id()
                
                right_leaf = Leaf(right, id_right, False, [], False)
                root = Leaf(operator, None, True, [left, right_leaf], left.nullable or right_leaf.nullable)

                self.nodes += [right_leaf, root]
                return root

            elif not isinstance(left, Leaf) and isinstance(right, Leaf):
                id_left = None
                if left != epsilon:
                    id_left = self.get_id()
                
                left_leaf = Leaf(left, id_left, False, [], False)
                root = Leaf(operator, None, True, [left_leaf, right], left_leaf.nullable or right.nullable)

                self.nodes += [left_leaf, root]
                return root
        except:
            print("Error en operacion or ")

    # Operacion concatenacion
    def concatenation(self, left, right):
        operator = '.'
        try:
            if isinstance(left, Leaf) and isinstance(right, Leaf):
                root = Leaf(operator, None, True, [left, right], left.nullable and right.nullable)
                self.nodes += [root]
                return root

            elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
                id_left = None
                id_right = None
                if left != epsilon:
                    id_left = self.get_id()
                if right != epsilon:
                    id_right = self.get_id()

                left_leaf = Leaf(left, id_left, False, [], False)
                right_leaf = Leaf(right, id_right, False, [], False)
                root = Leaf(operator, None, True, [left_leaf, right_leaf], left_leaf.nullable and right_leaf.nullable)

                self.nodes += [left_leaf, right_leaf, root]
                return root

            elif isinstance(left, Leaf) and not isinstance(right, Leaf):
                id_right = None
                if right != epsilon:
                    id_right = self.get_id()
                
                right_leaf = Leaf(right, id_right, False, [], False)
                root = Leaf(operator, None, True, [left, right_leaf], left.nullable and right_leaf.nullable)

                self.nodes += [right_leaf, root]
                return root
            
            elif not isinstance(left, Leaf) and isinstance(right, Leaf):
                id_left = None
                if left != epsilon:
                    id_left = self.get_id()
                
                left_leaf = Leaf(left, id_left, False, [], False)
                root = Leaf(operator, None, True, [left_leaf, right], left_leaf.nullable and right.nullable)

                self.nodes += [left_leaf, root]
                return root
        except:
            print("Error en concatenacion")
        
    # Implementacion de Move para la simulacion
    def simulate_move(self, Nodo, symbol):
        move = None
        for i in self.transitions:
            if i[0] == Nodo and i[1] == symbol:
                move = i[2]

        return move
    
    # Crea las transiciones del grafo
    def create_transitions(self):
        f = {}
        for t in self.transitions:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    # Genera los nodos y transiciones para el AFD
    def create_dfa(self):
        try:
            startNode0 = self.root.first_pos
            startNode0_automata = DFA_Node(self.get_name(), startNode0, True)
            self.states.append(startNode0_automata)
            self.init_state = startNode0_automata.name

            if self.final_state in [u for u in startNode0_automata.conjunto_nodos]:
                self.acc_states.append(startNode0_automata.name)

            while not self.state_is_marked():
                T = self.state_is_unmarked()
                
                T.Mark()

                for s in self.symbols:
                    fp = []
                    
                    for u in T.conjunto_nodos:
                        if self.get_leaf(u).name == s:
                            fp += self.follow_pos[u]
                    fp = {a for a in fp}
                    fp = [a for a in fp]
                    if len(fp) == 0:
                        continue

                    U = DFA_Node(self.get_name(), fp, True)

                    if U.id not in [n.id for n in self.states]:
                        if self.final_state in [u for u in U.conjunto_nodos]:
                            self.acc_states.append(U.name)
                        
                        self.states.append(U)
                        self.transitions.append((T.name, s, U.name))
                    else:
                        self.count -= 1
                        for estado in self.states:
                            if U.id == estado.id:
                                self.transitions.append((T.name, s, estado.name))
        except:
            print("Syntax error")

    def get_leaf(self, name):
        for n in self.nodes:
            if n.position == name:
                return n

    def state_is_unmarked(self):
        for n in self.states:
            if not n.isMarked:
                return n

    def get_name(self):
        if self.count == 0:
            self.count += 1
            return 'S' # Starting node!

        available_letters = ' ABCDEFGHIJKLMNOPQRTUVWXYZ'
        name = available_letters[self.count]
        self.count += 1

        if self.count == len(available_letters):
            self.rounds += 1
            self.count = 0

        return name * self.rounds

    def calculate_followpow(self):
        for n in self.nodes:
            if not n.is_operator and not n.nullable:
                self.add_followpos(n.position, [])

        for n in self.nodes:
            if n.name == '.':
                c1, c2 = [*n.children]

                for i in c1.last_pos:
                    self.add_followpos(i, c2.first_pos)

            elif n.name == '*':
                for i in n.last_pos:
                    self.add_followpos(i, n.first_pos)                

    # Revisa si existe algun estado desmarcado
    def state_is_marked(self):
        marks = [n.isMarked for n in self.states]
        return functools.reduce(lambda a, b: a and b, marks)

    # Agrega un followpos
    def add_followpos(self, pos, val):
        if pos not in self.follow_pos.keys():
            self.follow_pos[pos] = []

        self.follow_pos[pos] += val
        self.follow_pos[pos] = {i for i in self.follow_pos[pos]}
        self.follow_pos[pos] = [i for i in self.follow_pos[pos]]
    
    # Verifica que esten dando una letra i numero
    def is_char_symbol(self, character):
        symbols = 'ε'+'abcdefghijklmnopqrstuvwxyz0123456789#'
        return symbols.find(character) != -1

    # Obtiene el ID del nodo
    def get_id(self):
        self.id = self.id + 1
        return self.id

    # Obtiene la precedencia entre dos operadores
    def preceding_operator(self, op1, op2):
        order = ['|','.','*']
        if order.index(op1) >= order.index(op2):
            return True
        else:
            return False
    
        # Simulacion de AFD
    def simulate_string(self, exp):
        start = self.init_state
        for e in exp:
            start = self.simulate_move(start, e)
            if start == None:
                return 'no'
        if start in self.acc_states:
            return 'yes'
        
    def draw(self):
        # Crea un objeto Digraph de graphviz
        dot = Digraph('G', filename='output/DFA', format='pdf')
        
        # Agrega los estados
        for state in self.states:
            if state == self.init_state:
                dot.node(str(state), shape='point')
            elif state in self.acc_states:
                dot.node(str(state), shape='doublecircle')
            else:
                dot.node(str(state), shape='circle')
        
        # Agrega las transiciones
        for transition in self.transitions:
            dot.edge(str(transition[0]), str(transition[2]), label=transition[1])
        
        # Renderiza la imagen
        dot.render(view=True)