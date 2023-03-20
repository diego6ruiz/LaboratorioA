import copy
import itertools
from Nodo import Nodo
    
def getKey(dic, val):
    for key, value in dic.items():
         if val == value:
             return key
    return "There is no key"

def MinDFATranslate(afd):
    previousK = []
    currentK = []
    transiciones = copy.deepcopy(afd.transiciones)
    symbols = copy.deepcopy(afd.symbols)
    nonFinalStates = []
    finalStates = []
    
    for state in afd.states:
        nonFinalStates.append(state) if state not in afd.finalStates else finalStates.append(state)
            
    currentK.append(copy.deepcopy(finalStates))
    currentK.append(copy.deepcopy(nonFinalStates))
    y = True
    while currentK != previousK:
        if y:
            y = False
            previousK = copy.deepcopy(currentK)
        for particion in range(len(currentK)):
            combinaciones = itertools.combinations(currentK[particion], 2)
            dist = []
            for combinacion in combinaciones:
                if (combinacion[0] not in dist) and (combinacion[1] not in dist):
                    for symbol in symbols:
                        estadoF1 = None
                        estadoF2 = None
                        for transicion in transiciones:
                            if (transicion[0] == combinacion[0]) and (transicion[1] == symbol):
                                estadoF1 = transicion[2]
                            if (transicion[0] == combinacion[1]) and (transicion[1] == symbol):
                                estadoF2 = transicion[2]
                        if (estadoF1 != None) and (estadoF2 != None):
                            for particion2 in previousK:
                                if (estadoF1 in particion2) and (estadoF2 not in particion2):
                                    dist.append(combinacion[1])
                            else:
                                estadoF1 = None
                                estadoF2 = None
            previousK = copy.deepcopy(currentK)
            final = []
            for state in currentK[particion]:
                if state not in dist:
                    final.append(state)
            currentK[particion] = final
            if dist:
                currentK.append(dist)
    return currentK

def FDAMinimization(Mstates, afd):
    dictFDAMin = {}
    counter = 0
    nodo = Nodo('')
    nodo.symbols = copy.deepcopy(afd.symbols)
    
    for estadoAFDM in Mstates:
        dictFDAMin[counter] = estadoAFDM
        nodo.states.append(counter)
        counter = counter + 1
        
    for estadoAFDM in Mstates:
        for initialState in afd.initialState:
            if initialState in estadoAFDM:
                state = getKey(dictFDAMin, estadoAFDM)
                nodo.initialState.append(state)
                
    for estadoAFDM in Mstates:
        for finalState in afd.finalStates:
            if finalState in estadoAFDM:
                state = getKey(dictFDAMin, estadoAFDM)
                nodo.finalStates.append(state)
                
    for estadoAFDM in Mstates:
        for transicion in afd.transiciones:
            if transicion[0] in estadoAFDM:
                for estadoAFDM2 in Mstates:
                    if transicion[2] in estadoAFDM2: 
                        estadoI = getKey(dictFDAMin, estadoAFDM)
                        estadoF = getKey(dictFDAMin, estadoAFDM2)
                        if [estadoI, transicion[1], estadoF] not in nodo.transiciones:
                            nodo.transiciones.append([estadoI, transicion[1], estadoF])   
    return nodo