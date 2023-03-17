import graphviz


class Nodo:
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
            node = Nodo(c, child)
            stack.append(node)
        elif c == '.' or c == '|':
            right_child = stack.pop()
            left_child = stack.pop()
            node = Nodo(c, left_child, right_child)
            stack.append(node)
        else:
            node = Nodo(c)
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
        afn = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_epsilon_trans(afn.inicial)
        inicial.add_epsilon_trans(final)
        afn.final.add_epsilon_trans(afn.inicial)
        afn.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    elif nodo.value == '+':
        afn1 = construir_FNA_desde_arbol(nodo.left)
        afn2 = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_trans(nodo.left.value, afn1.final)
        # inicial.add_epsilon_trans(afn1.inicial)
        afn1.final.add_epsilon_trans(afn2.inicial)
        afn1.final.add_epsilon_trans(final)
        afn2.inicial.add_trans(nodo.left.value, afn2.final)
        afn2.final.add_epsilon_trans(afn2.inicial)
        afn2.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    elif nodo.value == '?':
        afn = construir_FNA_desde_arbol(nodo.left)
        inicial = State()
        final = State()
        inicial.add_epsilon_trans(afn.inicial)
        inicial.add_epsilon_trans(final)
        afn.final.add_epsilon_trans(final)
        return FNA(inicial, final)
    else:
        estado_inicial = State()
        estado_final = State()
        estado_inicial.add_trans(nodo.value, estado_final)
        return FNA(estado_inicial, estado_final)


def generar_grafo_FNA(afn, x):
    visitados = set()
    nodos = [afn.inicial]
    nodos_finales = {afn.final}
    transiciones = []

    if x==1:
        name='fna'
    elif x==2:
        name='dfa'

    g = graphviz.Digraph('FNA', filename=('output/'+name), format='pdf')
    g.attr(rankdir='LR', size='8,5')

    while nodos:
        nodo = nodos.pop()
        visitados.add(nodo)

        if nodo in nodos_finales:
            # Doble círculo si es estado final
            nodo_attrs = {'peripheries': '2', 'color': 'red'}
        elif nodo == afn.inicial:
            nodo_attrs = {'color': 'blue'}  # Color rojo si es estado inicial
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
