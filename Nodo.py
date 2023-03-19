import copy

class Nodo:
    def __init__(self, regex):
        self.re = regex
        self.states = []
        self.symbols = [] 
        self.initialState = [] 
        self.finalStates = [] 
        self.transiciones = [] 

        self.hijos = []
        self.pos = None
        self.anulable = None
        self.first_position = []
        self.last_position = []
        self.typeNodo = None

    def transicionBase(self, correlativoEstado):
        finalState = correlativoEstado + 1

        self.symbols = [self.re]
        self.initialState = [correlativoEstado]
        self.finalStates = [finalState]
        self.states = [correlativoEstado, finalState]
        self.transiciones = [[
            correlativoEstado, 
            self.re, 
            finalState 
        ]]

        return finalState + 1

    def operacionesBase(self, corrPos):

        self.hijos = []

        if self.re == 'ε':
            self.pos = None
            corrPos = corrPos - 1
        else:
            self.pos = corrPos

        if self.re == 'ε':
            self.anulable = True
        else:
            self.anulable = False

        if self.re == 'ε':
            self.first_position = []
        else:
            self.first_position = [self.pos]

        if self.re == 'ε':
            self.last_position = []
        else:
            self.last_position = [self.pos]

        return corrPos + 1

    def transicionOrAFN(self, left, right, correlative):
        finalState = correlative + 1

        self.symbols = ['ε'] + left.symbols + right.symbols
        self.symbols = list(dict.fromkeys(self.symbols))

        self.initialState = [correlative]
        self.finalStates = [correlative+1]

        self.states = left.states + right.states + [correlative,correlative+1]
        self.states = list(dict.fromkeys(self.states))

        self.transiciones = left.transiciones + right.transiciones + [[
            self.initialState[0],
            'ε', 
            left.initialState[0]
        ]] + [[
            self.initialState[0],
            'ε', 
            right.initialState[0]
        ]] + [[
            left.finalStates[0],
            'ε', 
            self.finalStates[0]
        ]] + [[
            right.finalStates[0],
            'ε', 
            self.finalStates[0]
        ]]

        return finalState + 1

    def concatAFN(self, left, right, correlative):
        self.symbols = left.symbols + right.symbols
        self.symbols = list(dict.fromkeys(self.symbols))

        self.initialState = left.initialState
        self.finalStates = right.finalStates

        self.states = left.states + right.states
        self.states = list(dict.fromkeys(self.states))
        self.states.remove(left.finalStates[0])

        self.transiciones = left.transiciones + right.transiciones

        for i in self.transiciones:
            if i[2] == left.finalStates[0]:
                i[2] = right.initialState[0]

        return correlative

    def CerraduraAFN(self, nodo, correlative):
        finalState = correlative + 1

        self.symbols = ['ε'] + nodo.symbols
        self.symbols = list(dict.fromkeys(self.symbols))

        self.initialState = [correlative]
        self.finalStates = [correlative + 1]
        self.states = nodo.states + [correlative,correlative+1]
        self.transiciones = nodo.transiciones + [[
            self.initialState[0],
            'ε', 
            nodo.initialState[0]
        ]] + [[
            nodo.finalStates[0],
            'ε', 
            nodo.initialState[0]
        ]] + [[
            self.initialState[0],
            'ε',
            self.finalStates[0]
        ]] + [[
            nodo.finalStates[0],
            'ε', 
            self.finalStates[0]
        ]]

        return finalState + 1

    def CerraduraPositivaAFN(self, nodo, correlative):

        finalState = correlative + 1

        copyNodo = Nodo('')
        copyNodo.re = nodo.re
        copyNodo.symbols = copy.deepcopy(nodo.symbols)
        copyNodo.states = copy.deepcopy(nodo.states)
        copyNodo.initialState = copy.deepcopy(nodo.initialState)
        copyNodo.finalStates = copy.deepcopy(nodo.finalStates)
        copyNodo.transiciones = copy.deepcopy(nodo.transiciones)

        self.symbols = ['ε'] + nodo.symbols
        self.symbols = list(dict.fromkeys(self.symbols))

        self.initialState = [correlative]
        self.finalStates = [correlative + 1]
        self.states = nodo.states + [correlative,correlative+1]
        self.transiciones = nodo.transiciones + [[
            self.initialState[0],
            'ε', 
            nodo.initialState[0]
        ]] + [[
            nodo.finalStates[0],
            'ε', 
            nodo.initialState[0]
        ]] + [[
            self.initialState[0],
            'ε',
            self.finalStates[0]
        ]] + [[
            nodo.finalStates[0],
            'ε',
            self.finalStates[0]
        ]]


        extra = len(nodo.states)

        X = []
        Y = []

        for i in range(extra):
            X.append(copyNodo.states[i])
            Y.append(finalState + 1 + i)
            copyNodo.states[i] = finalState + 1 + i

        for j in range(len(nodo.transiciones)):
            s = X.index(nodo.transiciones[j][0])
            nodo.transiciones[j][0] = Y[s]

            s = X.index(nodo.transiciones[j][2])
            nodo.transiciones[j][2] = Y[s]

        s = X.index(copyNodo.initialState[0])
        copyNodo.initialState[0] = Y[s]

        s = X.index(copyNodo.finalStates[0])
        copyNodo.finalStates[0] = Y[s]

        self.symbols = self.symbols + copyNodo.symbols
        self.symbols = list(dict.fromkeys(self.symbols))

        self.initialState = self.initialState
        nodoFinal = self.finalStates[0]
        self.finalStates = copyNodo.finalStates

        self.states = self.states + copyNodo.states
        self.states = list(dict.fromkeys(self.states))
        self.states.remove(nodoFinal)

        self.transiciones = self.transiciones + copyNodo.transiciones

        for i in self.transiciones:
            if i[2] == nodoFinal:
                i[2] = copyNodo.initialState[0]

        return finalState + 1 + extra

    def transicionCerraduraInterogationAFN(self, nodo, correlative):

        nodoEpsilon = Nodo('ε')
        correlative = nodoEpsilon.transicionBase(correlative)
        finalState = correlative + 1

        self.symbols = ['ε'] + nodo.symbols + nodoEpsilon.symbols
        self.symbols = list(dict.fromkeys(self.symbols))


        self.initialState = [correlative]
        self.finalStates = [correlative+1]

        self.states = nodo.states + nodoEpsilon.states + [correlative,correlative+1]
        self.states = list(dict.fromkeys(self.states))

        self.transiciones = nodo.transiciones + nodoEpsilon.transiciones + [[
            self.initialState[0],
            'ε', 
            nodo.initialState[0]
        ]] + [[
            self.initialState[0],
            'ε', 
            nodoEpsilon.initialState[0]
        ]] + [[
            nodo.finalStates[0],
            'ε', 
            self.finalStates[0]
        ]] + [[
            nodoEpsilon.finalStates[0],
            'ε',
            self.finalStates[0]
        ]]

        return finalState + 1

    def cerraduraE(self, states):
        states = copy.deepcopy(states)
        conjuntoS = []
        for i in states:
            conjuntoS.append(i)
            siguienteEstado = i
            movimientosE = []
            for j in self.transiciones:
                if j[0] == siguienteEstado and j[1] == 'ε':
                    movimientosE.append(copy.deepcopy(j))
            
            while movimientosE:
                siguienteTransicion = movimientosE.pop()
                if siguienteTransicion[1] == 'ε':
                    conjuntoS.append(siguienteTransicion[2])
                    for k in self.transiciones:
                        if k[0] == siguienteTransicion[2] and (k[0] not in conjuntoS or k[2] not in conjuntoS):
                            movimientosE.append(k)
                
        conjuntoS = list(dict.fromkeys(conjuntoS))
        return conjuntoS

    def move(self, S, c):
        conjuntoM = []
        for state in S:
            for j in self.transiciones:
                if j[0] == state and j[1] == c:
                    conjuntoM.append(j[2])

        return conjuntoM

    def transicionOrAFD(self, left, right):
        if left.anulable or right.anulable:
            self.anulable = True
        else:
            self.anulable = False

        self.first_position = list(dict.fromkeys(left.first_position + right.first_position))

        self.last_position = list(dict.fromkeys(left.last_position + right.last_position))

        self.typeNodo = '|'

    def transicionConcatAFD(self, left, right):

        if left.anulable and right.anulable:
            self.anulable = True
        else:
            self.anulable = False

        if left.anulable:
            self.first_position = list(dict.fromkeys(left.first_position + right.first_position))
        else:
            self.first_position = left.first_position

        if right.anulable:
            self.last_position = list(dict.fromkeys(left.last_position + right.last_position))
        else:
            self.last_position = right.last_position
        

        self.typeNodo = '.'

        self.hijos = [left, right]

    def transicionCerraduraAFD(self, nodo):

        self.anulable = True

        self.first_position = nodo.first_position

        self.last_position = nodo.last_position

        self.typeNodo = '*'