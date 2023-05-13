from Nodo import Nodo
from Tree import *

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

class Simulation:
    def __init__(self, automaton, input):
        self.automaton = automaton
        self.input = input
        self.result = []
        self.cadena = ""
        self.position = 0

        self.directSimulation()
        print(self.result)
    
    def simulation(self):
        afn = False
        for transition in self.automaton.transitions:
            if transition[2] == 'ε':
                afn = True
                break
            
        current_states = Set()
        current_states.addElement(self.automaton.initialState)
        if afn:
            for state in self.automaton.epsilonClosure(self.automaton.initialState).elements:
                if self.stateAlreadyExists(state, current_states) is None:
                    current_states.addElement(state)

        for symbol in self.input:
            next_states = Set()
            for state in current_states.elements:
                for transition in self.automaton.transitions:
                    if transition[0].id == state.id and chr(int(transition[2])) == symbol:
                        if self.stateAlreadyExists(transition[1], next_states) is None:
                            next_states.addElement(transition[1])

            if next_states.IsEmpty():
                print("Error lexico")
                return False
            
            if afn:
                for state in next_states.elements:
                    for epsilon_state in self.automaton.epsilonClosure(state).elements:
                        if self.stateAlreadyExists(epsilon_state, next_states) is None:
                            next_states.addElement(epsilon_state)
                        
            if next_states.IsEmpty():
                return False
            
            current_states = next_states

            self.cadena += symbol

        for state in current_states.elements:
            if state in self.automaton.finalStates.elements:
                print(self.cadena, state.token)
                return True
        
        print("Error lexico")
        return False
    
    def stateAlreadyExists(self, state, states):
        for element in states.elements:
            if element.id == state.id:
                return element
        return None       


    def directSimulation(self):

        current_states = Set()
        current_states.addElement(self.automaton.initialState)

        if self.position == len(self.input) -1:
            return

        for i in range (self.position, len(self.input)):

            next_states = Set()
            for state in current_states.elements:
                for transition in self.automaton.transitions:
                    if transition[0].id == state.id and chr(int(transition[2])) == self.input[i]:
                        if self.stateAlreadyExists(transition[1], next_states) is None:
                            next_states.addElement(transition[1])
                    
            if next_states.isEmpty():
                if self.cadena == "":
                    self.result.append((self.input[i], "Error Lexico"))

                    self.position = i + 1
                    self.cadena = ""
                    self.directSimulation()
                break
            
            else:      
                current_states = next_states
                self.cadena += self.input[i]

        for state in current_states.elements:
            if state in self.automaton.finalStates.elements:

                if state.token == "#":
                    self.result.append((self.cadena, None))
                else:
                    self.result.append((self.cadena, state.token))
                self.position = i
                self.cadena = ""
                self.directSimulation()