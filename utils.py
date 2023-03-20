from graphviz import Digraph
import postfixToNfa as nfaF
import RegexToDFA as dfaF
import NFAtoDFA as nfaDfaF
import MinDFA as minDFAF

def core_NFA(arbolFNA,int=0) :
    nodesRegex, corr = nfaF.regexToNodes(arbolFNA, 0)
    nfaT, corr = nfaF.treeToFNA(nodesRegex, corr, 0)
    return nfaT

def draw_fna(nfa):
    f = Digraph('NFA', filename='output/NFA', format='pdf')
    f.attr(rankdir='LR', size='8,5')
    
    f.attr('node', shape='doublecircle')
    for finalState in nfa.finalStates:
        f.node(str(finalState))
        
    f.attr('node', shape='circle')
    for initialState in nfa.initialState:
        f.node(str(initialState))

    f.attr('node', shape='none')
    f.node('')
    for initialState in nfa.initialState:
        f.edge('', str(initialState), label='')

    f.attr('node', shape='circle')
    for transicion in nfa.transiciones:
        f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

    f.view()

def core_DirectFDA (arbolFDA):
    regexSustNodes = dfaF.sustExp(arbolFDA)
    regexFDAnodes, _, x = dfaF.regexToNodes(regexSustNodes, 1, [])
    nodosHoja = dfaF.getLeafs(regexFDAnodes, [])
    nodoRoot, nodos = dfaF.definirNodosFDA(regexFDAnodes, 0, [])
    nodosFinales = nodosHoja + nodos
    positionsTable = dfaF.getNextPosition(nodosFinales, x)
    symbols = dfaF.directFDAsymbols(x)
    dStatesAFD, dTransAFD  = dfaF.directFDA(nodoRoot, symbols, positionsTable, x)
    finalPos = x[-1][1]
    DirectFDA = dfaF.directFDANodeConvert(dStatesAFD, dTransAFD, symbols, finalPos)
    return DirectFDA

def draw_dfa(dfa):
    f = Digraph('DFA', filename='output/DFA', format='pdf')
    f.attr(rankdir='LR', size='8,5')
    
    f.attr('node', shape='doublecircle')
    for finalState in dfa.finalStates:
        f.node(str(finalState))
        
    f.attr('node', shape='circle')
    for initialState in dfa.initialState:
        f.node(str(initialState))

    f.attr('node', shape='none')
    f.node('')
    for initialState in dfa.initialState:
        f.edge('', str(initialState), label='')

    f.attr('node', shape='circle')
    for transicion in dfa.transiciones:
        f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

    f.view()



def core_SubFDA(nfa):
    dStates, dTrans = nfaDfaF.nfaToDfa(nfa)
    fda = nfaDfaF.AFDnodeConvert(nfa, dStates, dTrans)
    return fda

def draw_dfaSub(dfa):
    f = Digraph('DFA', filename='output/DFA Subconjuntos', format='pdf')
    f.attr(rankdir='LR', size='8,5')
    
    f.attr('node', shape='doublecircle')
    for finalState in dfa.finalStates:
        f.node(str(finalState))
        
    f.attr('node', shape='circle')
    for initialState in dfa.initialState:
        f.node(str(initialState))

    f.attr('node', shape='none')
    f.node('')
    for initialState in dfa.initialState:
        f.edge('', str(initialState), label='')

    f.attr('node', shape='circle')
    for transicion in dfa.transiciones:
        f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

    f.view()

def core_minDFA(dfa):
    DFAstates = minDFAF.MinDFATranslate(dfa)
    minDFA = minDFAF.FDAMinimization(DFAstates, dfa)
    return minDFA

def draw_dfaMin(dfa):
    f = Digraph('DFA', filename='output/DFA Minimization', format='pdf')
    f.attr(rankdir='LR', size='8,5')
    
    f.attr('node', shape='doublecircle')
    for finalState in dfa.finalStates:
        f.node(str(finalState))
        
    f.attr('node', shape='circle')
    for initialState in dfa.initialState:
        f.node(str(initialState))

    f.attr('node', shape='none')
    f.node('')
    for initialState in dfa.initialState:
        f.edge('', str(initialState), label='')

    f.attr('node', shape='circle')
    for transicion in dfa.transiciones:
        f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

    f.view()