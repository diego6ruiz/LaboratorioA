from Nodo import Nodo

def NFASim(nfa, w):
    S = nfa.cerraduraE(nfa.initialState)
    for c in w:
        S = nfa.cerraduraE(nfa.move(S, c))

    inter = set.intersection(set(S), set(nfa.finalStates))
    inter = list(inter)

    if inter:
        return True
    else:
        return False

def DFASim(dfa, w):
    s = dfa.initialState
    for c in w:
        s = dfa.move(s, c)

    inter = set.intersection(set(s), set(dfa.finalStates))
    inter = list(inter)

    if inter:
        return True
    else:
        return False