import copy
from Nodo import Nodo
    
def isUnmarked(d_states):
    for i in d_states:
        if i[1] == 0:
            return True
    return False

def getFirstUnmarked(d_states):
    for i in d_states:
        if i[1] == 0:
            return i
    return False

def getDstates( d_states):       
    return [the_state[0] for the_state in d_states]

def state_in_states( the_state, d_states):
    for d_state in d_states:
        if len(the_state) == len(d_state):
            keep = True
            for the_element in the_state:
                if the_element not in d_state:
                    keep = False
                    break
            if keep:
                return True
    return False

def return_state_in_states( the_state, d_states):
    for d_state in d_states:
        if len(the_state) == len(d_state[0]):
            keep = True
            for the_element in the_state:
                if the_element not in d_state[0]:
                    keep = False
                    break
            if keep:
                return d_state
    return False

def nfaToDfa(nfa):
    d_states = []
    d_tran = []
    counter = 0
    d_states.append([nfa.cerraduraE(nfa.initialState), 0, counter])
    while isUnmarked(d_states):
        estado_t = getFirstUnmarked(d_states)
        estado_t[1] = 1
        symbols = copy.deepcopy(nfa.symbols)
        if 'ε' in symbols:
            symbols.remove('ε')
        for simbolo in symbols:
            U = nfa.cerraduraE(nfa.move(estado_t[0], simbolo))
            d_only_states = getDstates(d_states)
            newState = []
            if U:
                if not state_in_states(U, d_only_states):
                    counter = counter + 1
                    newState = [U, 0, counter]
                    d_states.append([U, 0, counter])
                else:
                    newState = return_state_in_states(U, d_states)

                d_tran.append([estado_t[2], simbolo, newState[2]])

    return d_states, d_tran

def AFDnodeConvert( nfa, d_states, d_tran):
    nodo = Nodo('')

    symbols = copy.deepcopy(nfa.symbols)

    if 'ε' in symbols:
        symbols.remove('ε')
    nodo.symbols = symbols

    for state in d_states:
        nodo.states.append(state[2])

    for state in d_states:
        for initialState in nfa.initialState:
            if initialState in state[0]:
                nodo.initialState.append(state[2])

    for state in d_states:
        for estadoFinal in nfa.finalStates:
            if estadoFinal in state[0]:
                nodo.finalStates.append(state[2])

    nodo.transiciones = copy.deepcopy(d_tran)
    return nodo