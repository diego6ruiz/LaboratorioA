import copy
from Nodo import Nodo

def isOperator(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False

def orFDA(nodos, auxNod):
    nodo = Nodo('')
    nodo.transicionOrFDA(nodos[0], auxNod)
    return nodo

def concatFDA(nodos, auxNod):
    nodo = Nodo('')
    nodo.transicionConcatFDA(nodos[0], auxNod)
    return nodo

def cerraduraFDA(nodos):
    nodo = Nodo('')
    nodo.transicionCerraduraFDA(nodos[0])
    return nodo

def sustExp(re):
    for nodo in range(len(re)):
        if type(re[nodo]) == list:
            sustExp(re[nodo])
        else:
            if isOperator(re[nodo]):
                if re[nodo] == '?':
                    re.pop()
                    nodoAnterior = re.pop()
                    re.append(copy.deepcopy(nodoAnterior))
                    re.append('|')
                    re.append('ε')
                elif re[nodo] == '+':
                    re.pop()
                    nodoAnterior = re.pop()
                    re.append([copy.deepcopy(nodoAnterior), '*'])
                    re.append(copy.deepcopy(nodoAnterior))

    return re

def regexToNodes(re, corr, attatch):
    
    for nodo in range(len(re)):
        if type(re[nodo]) == list:
            _, corr, _ = regexToNodes(re[nodo], corr, attatch)
        else:
            if not isOperator(re[nodo]):
                nuevoNodo = Nodo(re[nodo])
                corr = nuevoNodo.operacionesBase(corr)
                re[nodo] = nuevoNodo
                if nuevoNodo.re != 'ε':
                    attatch.append([nuevoNodo.re, corr - 1])

    return re, corr, attatch

def getLeafs(nodesRegex, le):
    leafs = le

    for nodo in nodesRegex:
        if type(nodo) == list:
            getLeafs(nodo, leafs)
        else:
            if not isOperator(nodo):
                leafs.append(nodo)

    return leafs

def definirNodosFDA(re, contadorExp, nodosProcess):
    nodesCounter = contadorExp
    processedNodesCounter = nodosProcess
    nodos = []
    operador = ''

    for nodo in range(len(re)):
        if type(re[nodo]) == list:
            nodo, _ = definirNodosFDA(re[nodo], 0, processedNodesCounter)
            if nodesCounter > 0:
                if nodesCounter > 0 and nodesCounter < 2 and operador != '|':
                    nodoNuevo = concatFDA(nodos, nodo)
                    processedNodesCounter.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    nodesCounter = 1

                elif nodesCounter > 0 and nodesCounter < 2 and operador == '|':
                    nodoNuevo = orFDA(nodos, nodo)
                    processedNodesCounter.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    nodesCounter = 1
                    operador = ''
            else:
                nodos.append(nodo)
                nodesCounter = nodesCounter + 1
        else:
            if nodesCounter > 0:
                if (re[nodo] == '*') and nodesCounter == 1:
                    if re[nodo] == '*':
                        nodoNuevo = cerraduraFDA(nodos)
                        processedNodesCounter.append(nodoNuevo)
                        nodos = [nodoNuevo]
                        nodesCounter = 1
                elif not isOperator(re[nodo]) and (nodesCounter < 2 and nodesCounter > 0)  and operador != '|':
                    nodoNuevo = concatFDA(nodos, re[nodo])
                    processedNodesCounter.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    nodesCounter = 1
                else:
                    if not isOperator(re[nodo]) and (nodesCounter < 2 and nodesCounter > 0) and operador == '|':
                        nodoNuevo= orFDA(nodos, re[nodo])
                        processedNodesCounter.append(nodoNuevo)
                        nodos = [nodoNuevo]
                        nodesCounter = 1
                        operador = ''
                    else:
                        operador = '|'
            else:
                nodos.append(re[nodo])
                nodesCounter = nodesCounter + 1

    return nodos[0], processedNodesCounter

def getNextPosition(nodos, posiciones):
    positionsTable = {}

    for posicion in posiciones:
        positionsTable[posicion[1]] = []

    for nodo in nodos:
        if (nodo.typeNodo == '.') or (nodo.typeNodo == '*'):
            if nodo.typeNodo == '*':
                for pos in nodo.last_position:
                    for posi in nodo.first_position:
                        positionsTable[pos].append(posi)
            elif nodo.typeNodo == '.':
                c1 = nodo.hijos[0]
                c2 = nodo.hijos[1]
                for pos in c1.last_position:
                    for posi in c2.first_position:
                        positionsTable[pos].append(posi)

    for key in positionsTable:
        positionsTable[key] = list(dict.fromkeys(positionsTable[key]))

    return positionsTable

def directFDAsymbols(attatch):
    symbols = []
    for simbolo in attatch:
        symbols.append(simbolo[0])

    symbols = list(dict.fromkeys(symbols))
    symbols.remove('#')

    return symbols

def isUnmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return True
    return False

def getFirstUnmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return i
    return False

def getDstates(Dstates):
    states = []
    for estado in Dstates:
        states.append(estado[0])

    return states

def state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate):
            keep = True
            for elemento in estado:
                if elemento not in Dstate:
                    keep = False
                    break
            if keep:
                return True
    return False

def return_state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate[0]):
            keep = True
            for elemento in estado:
                if elemento not in Dstate[0]:
                    keep = False
                    break
            if keep:
                return Dstate
    return False

def fetchPositions(S, simbolo, attatch):
    busqueda = []

    for posicion in S[0]:
        for correspondencia in attatch:
            if (correspondencia[1] == posicion) and (correspondencia[0] == simbolo):
                busqueda.append(posicion)

    return busqueda

def directFDA(nodoRoot, symbols, getNextPosition, attatch):
    Dstates = []
    Dtran = []
    contador = 0
    Dstates.append([nodoRoot.first_position, 0, contador])
    while isUnmarked(Dstates):
        estadoS = getFirstUnmarked(Dstates)
        estadoS[1] = 1
        if 'ε' in symbols:
            symbols.remove('ε')
        for simbolo in symbols:
            posiciones = fetchPositions(estadoS, simbolo, attatch)
            U = []
            for posicion in posiciones:
                U = U + copy.deepcopy(getNextPosition[posicion])
            U = list(dict.fromkeys(U))

            DOnlyStates = getDstates(Dstates)
            nuevoEstado = []
            if U:
                if not state_in_states(U, DOnlyStates):
                    contador = contador + 1
                    nuevoEstado = [U, 0, contador]
                    Dstates.append([U, 0, contador])
                else:
                    nuevoEstado = return_state_in_states(U, Dstates)

                Dtran.append([estadoS[2], simbolo, nuevoEstado[2]])

    return Dstates, Dtran

def directFDANodeConvert(Dstates, Dtran, symbols, posicionFinal):
    nodo = Nodo('')
    simbol = copy.deepcopy(symbols)
    if 'ε' in simbol:
        simbol.remove('ε')
    nodo.symbols = simbol
    for estado in Dstates:
        nodo.states.append(estado[2])
    nodo.initialState.append(Dstates[0][2])
    for estado in Dstates:
        if posicionFinal in estado[0]:
            nodo.finalStates.append(estado[2])
    nodo.transiciones = copy.deepcopy(Dtran)
    return nodo