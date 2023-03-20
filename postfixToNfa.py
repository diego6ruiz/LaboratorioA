import graphviz
from Nodo import Nodo


class NodoNFA:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.transitions = {}

    def es_hoja(self):
        return self.left is None and self.right is None


class State:
    ids = 0

    def __init__(self):
        self.id = State.ids
        State.ids += 1
        self.transiciones = {}
        self.epsilon_transitions = set()

    def add_trans(self, simbolo, estado):
        if simbolo in self.transiciones:
            if estado not in self.transiciones[simbolo]:
                # MAYBE cambiar .add(estado) por = estado
                self.transiciones[simbolo].add(estado)
        else:
            self.transiciones[simbolo] = {estado}

    def add_epsilon_trans(self, estado):
        self.epsilon_transitions.add(estado)

    def get_trans(self, simbolo):
        return self.transiciones.get(simbolo, set())

    def get_epsilon_trans(self):
        return self.epsilon_transitions

    def __str__(self):
        return f'{self.id}'


class FNA:
    def __init__(self, inicial, final):
        self.inicial = inicial
        self.final = final

    def match(self, cadena):
        estados_actuales = {self.inicial}
        for simbolo in cadena:
            nuevos_estados = set()
            for state in estados_actuales:
                nuevos_estados |= state.get_trans(simbolo)
                nuevos_estados |= state.get_epsilon_trans()
            estados_actuales = nuevos_estados
        return self.final in estados_actuales

    def __str__(self):
        visitados = set()
        nodos = [self.inicial]
        transiciones = []

        print('transiciones: \n')

        while nodos:
            nodo = nodos.pop()
            visitados.add(nodo)

            for simbolo, estados_destino in nodo.transiciones.items():
                for estado_destino in estados_destino:
                    transiciones.append((nodo, estado_destino, simbolo))
                    if estado_destino not in visitados:
                        nodos.append(estado_destino)

            for estado_destino in nodo.epsilon_transitions:
                transiciones.append((nodo, estado_destino, 'ε'))
                if estado_destino not in visitados:
                    nodos.append(estado_destino)

        transiciones_str = [
            f'{str(e1)} --{s}--> {str(e2)}' for e1, e2, s in transiciones]

        return '\n'.join(transiciones_str)



def construir_arbol(postfix):
    stack = []
    for c in postfix:
        if c == '*' or c == '?' or c == '+':
            child = stack.pop()
            node = NodoNFA(c, child)
            stack.append(node)
        elif c == '.' or c == '|':
            right_child = stack.pop()
            left_child = stack.pop()
            node = NodoNFA(c, left_child, right_child)
            stack.append(node)
        else:
            node = NodoNFA(c)
            stack.append(node)
    return stack[0]


def print_arbol(nodo, archivo):
    dot = graphviz.Digraph(comment='Árbol sintáctico')
    _agregar_nodo(dot, nodo)
    dot.render(archivo, view=True)


def _agregar_nodo(dot, nodo):
    if nodo is None:
        return
    _agregar_nodo(dot, nodo.left)
    _agregar_nodo(dot, nodo.right)
    dot.node(str(nodo), str(nodo.value))
    if nodo.left is not None:
        dot.edge(str(nodo), str(nodo.left))
    if nodo.right is not None:
        dot.edge(str(nodo), str(nodo.right))


def construir_FNA_desde_arbol(nodo):
    if nodo.value == '.':
        afn1 = construir_FNA_desde_arbol(nodo.left)
        afn2 = construir_FNA_desde_arbol(nodo.right)
        afn1.final.add_epsilon_trans(afn2.inicial)
        afn1.final = afn2.final
        return afn1
    elif nodo.value == '|':
        afn1 = construir_FNA_desde_arbol(nodo.left)
        afn2 = construir_FNA_desde_arbol(nodo.right)
        inicial = State()
        inicial.add_epsilon_trans(afn1.inicial)
        inicial.add_epsilon_trans(afn2.inicial)
        final = State()
        afn1.final.add_epsilon_trans(final)
        afn2.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    elif nodo.value == '*':
        fna = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_epsilon_trans(fna.inicial)
        inicial.add_epsilon_trans(final)
        fna.final.add_epsilon_trans(fna.inicial)
        fna.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    elif nodo.value == '+':
        afn1 = construir_FNA_desde_arbol(nodo.left)
        afn2 = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_trans(nodo.left.value, afn1.final)
        afn1.final.add_epsilon_trans(afn2.inicial)
        afn1.final.add_epsilon_trans(final)
        afn2.inicial.add_trans(nodo.left.value, afn2.final)
        afn2.final.add_epsilon_trans(afn2.inicial)
        afn2.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    elif nodo.value == '?':
        fna = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_epsilon_trans(fna.inicial)
        inicial.add_epsilon_trans(final)
        fna.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    else:
        estado_inicial = State()
        estado_final = State()
        estado_inicial.add_trans(nodo.value, estado_final)
        return FNA(estado_inicial, estado_final)


def generar_grafo_FNA(fna):
    visitados = set()
    nodos = [fna.inicial]
    nodos_finales = {fna.final}
    transiciones = []



    g = graphviz.Digraph('FNA', filename=('output/fna'), format='pdf')
    g.attr(rankdir='LR', size='8,5')

    while nodos:
        nodo = nodos.pop()
        visitados.add(nodo)

        if nodo in nodos_finales:
            nodo_attrs = {'peripheries': '2', 'color': 'red'}
        elif nodo == fna.inicial:
            nodo_attrs = {'color': 'blue'}
        else:
            nodo_attrs = {}

        g.node(str(nodo), label=str(nodo), **nodo_attrs)

        for simbolo, estados_destino in nodo.transiciones.items():
            for estado_destino in estados_destino:
                transiciones.append((nodo, estado_destino, simbolo))
                if estado_destino not in visitados:
                    nodos.append(estado_destino)

        for estado_destino in nodo.epsilon_transitions:
            transiciones.append((nodo, estado_destino, 'ε'))
            if estado_destino not in visitados:
                nodos.append(estado_destino)

    for e1, e2, s in transiciones:
        g.edge(str(e1), str(e2), label=s)

    g.view()

def isOperator(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False

def orFNA(nodos, auxNod, corr):
    nodo = Nodo('')
    corr = nodo.transicionOrFNA(nodos[0], auxNod, corr)
    return nodo, corr

def concatFNA(nodos, auxNod, corr):
    nodo = Nodo('')
    corr = nodo.transicionConcatFNA(nodos[0], auxNod, corr)
    return nodo, corr

def cerraduraFNA(nodos, corr):
    nodo = Nodo('')
    corr = nodo.transicionCerraduraFNA(nodos[0], corr)
    return nodo, corr

def cerraduraPositivaFNA(nodos, corr):
    nodo = Nodo('')
    corr = nodo.transicionCerraduraPositivaFNA(nodos[0], corr)
    return nodo, corr

def cerraduraInterogationFNA(nodos, corr):
    nodo = Nodo('')
    corr = nodo.transicionCerraduraInterogationFNA(nodos[0], corr)
    return nodo, corr

def regexToNodes(reArray, corr):
    for nodo in range(len(reArray)):
        if type(reArray[nodo]) == list:
            _, corr = regexToNodes(reArray[nodo], corr)
        else:
            if not isOperator(reArray[nodo]):
                nuevoNodo = Nodo(reArray[nodo])
                corr = nuevoNodo.transicionBase(corr)
                reArray[nodo] = nuevoNodo
    return reArray, corr

def treeToFNA(reArray, corr, nodeCounter):
    nodos = []
    op = ''

    for nodo in range(len(reArray)):
        if type(reArray[nodo]) == list:
            nodo, corr = treeToFNA(reArray[nodo], corr, 0)

            if nodeCounter > 0:
                if nodeCounter > 0 and nodeCounter < 2 and op != '|':
                    nodoNuevo, corr = concatFNA(nodos, nodo, corr)
                    nodos = [nodoNuevo]
                    nodeCounter = 1

                elif nodeCounter > 0 and nodeCounter < 2 and op == '|':
                    nodoNuevo, corr = orFNA(nodos, nodo, corr)
                    nodos = [nodoNuevo]
                    nodeCounter = 1
                    op = ''
            else:
                nodos.append(nodo)
                nodeCounter += 1
        else:
            if nodeCounter > 0:
                if (reArray[nodo] == '+' or reArray[nodo] == '*' or reArray[nodo] == '?') and nodeCounter == 1:
                    if reArray[nodo] == '*':
                        nodoNuevo, corr = cerraduraFNA(nodos, corr)
                        nodos = [nodoNuevo]
                        nodeCounter = 1

                    if reArray[nodo] == '+':
                        nodoNuevo, corr = cerraduraPositivaFNA(nodos, corr)
                        nodos = [nodoNuevo]
                        nodeCounter = 1

                    if reArray[nodo] == '?':
                        nodoNuevo, corr = cerraduraInterogationFNA(nodos, corr)
                        nodos = [nodoNuevo]
                        nodeCounter = 1

                elif not isOperator(reArray[nodo]) and (nodeCounter < 2 and nodeCounter > 0)  and op != '|':
                    nodoNuevo, corr = concatFNA(nodos, reArray[nodo], corr)
                    nodos = [nodoNuevo]
                    nodeCounter = 1
                else:
                    if not isOperator(reArray[nodo]) and (nodeCounter < 2 and nodeCounter > 0) and op == '|':
                        nodoNuevo, corr = orFNA(nodos, reArray[nodo], corr)
                        nodos = [nodoNuevo]
                        nodeCounter = 1
                        op = ''
                    else:
                        op = '|'
            else:
                nodos.append(reArray[nodo])
                nodeCounter = nodeCounter + 1

    return nodos[0], corr    