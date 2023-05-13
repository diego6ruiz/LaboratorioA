from Direct import *
from Tree import *
from State import *

class SLR(Automaton):
    def __init__(self, tokens, productions):
        self.terminals = tokens
        self.grammar = productions
        self.symbols = Set()
        self.producciones = self.formatSLR()
        self.initialState = None
        self.states = Set()
        self.transitions = []
        self.finalStates = Set()
        self.start = None

    def SLR(self,):
        for produccion in self.producciones:
            if produccion.split("=>")[0] not in self.terminals:
                produccion = produccion.split("=>")
                produccion[1] = " ." + produccion[1]
                produccion = produccion[0] + "=>" + produccion[1]
                self.start = produccion
                cerradura  = self.cerradura(produccion)
                self.initialState = State("\n".join(cerradura), "inicial", None, None, self.cerradura(produccion))
                break

        self.states.addElement(self.initialState)

        for estado in self.states.elements:
            for symbol in self.symbols.elements:
                siguiente = self.ir_a(estado, symbol)
                if siguiente != None:
                    if self.verificarRepetidos(siguiente) == False:
                        self.states.addElement(siguiente)
                        if siguiente.type == "final":
                            self.finalStates.addElement(siguiente)
                    self.addTransition(estado, siguiente, symbol)

        self.pruebas()
        self.toString()
        self.toGraph(self, "SLR")


    def ir_a(self,estado,simbolo):
        producciones = []
        for produccion in estado.productions:

            if produccion.split("=>")[1].split(".")[1].split().__len__() > 0:
                if produccion.split("=>")[1].split(".")[1].split()[0].strip() == simbolo:
                    antes, despues = produccion.split(".")
                    despues = despues.split()
                    if len(despues) == 1:
                        produccion = antes + " " + despues[0] + " ."
                    else:
                        produccion = antes + " " + despues[0] + " . " + " ".join(despues[1:])
                    producciones.append(produccion)
            
        for produccion in producciones:
            if produccion.split(".")[1].split().__len__() > 0:
                right_part = produccion.split(".")[1].split()[0].strip()
                if right_part not in self.terminals and right_part != "=>":
                    cerradura = self.cerradura(produccion)
                    for produccion in cerradura:
                        if produccion not in producciones:
                            producciones.append(produccion)

        if len(producciones) > 0:
            for produccion in producciones:
                if produccion.replace(".", "").strip() == self.start.replace(".", "").strip():
                    right_part_InitState = self.start.split(".")[1].split()[0].strip()
                    left_part_produccion = produccion.split(".")[0].split()[-1].strip()

                    if right_part_InitState == left_part_produccion:
                        return State("\n".join(producciones), "final", None, None, producciones)
            else:
                return State("\n".join(producciones), "normal", None, None, producciones)
        else:
            return None

    def cerradura(self,produccion):
        producciones = []
        producciones.append(produccion)

        for produccion1 in producciones:
            for produccion2 in self.producciones:
                term1 = produccion1.split("=>")[1].split(".")[1].split()[0].strip()
                term2 = produccion2.split("=>")[0].strip()
                if term1 == term2:
                    produccion2 = produccion2.split("=>")
                    produccion2[1] = " ." + produccion2[1]
                    produccion2 = produccion2[0] + "=>" + produccion2[1]
                    
                    if produccion2 not in producciones:
                        producciones.append(produccion2)
        return producciones


    def formatSLR(self):
        grammar_array = []

        key = list(self.grammar.keys())[0]
        grammar_array.append(key + "'" + ' => ' + key)

        self.symbols.addElement(key)

        for nonterminal, productions in self.grammar.items():
            for production in productions:
                for word in production.split(' '):
                    if word not in self.symbols.elements:
                        self.symbols.addElement(word)
                grammar_array.append(nonterminal + ' => ' + production)
        return grammar_array
    
    def verificarRepetidos(self, siguiente):
        for estado in self.states.elements:
            if siguiente.productions == estado.productions:
                return True
        return False
    
    def pruebas(self):
        for simbolo in self.symbols.elements:
            primero = self.calcular_primero(simbolo)
            siguiente = self.calcular_siguiente(simbolo)
            print("Primero de " + simbolo + ": " + str(primero))
            print("Siguiente de " + simbolo + ": " + str(siguiente))
            

    def calcular_primero(self, simbolo):
        primero = set()
        if simbolo in self.terminals:
            primero.add(simbolo)
            return primero
        for produccion in self.grammar[simbolo]:
            primer_simbolo = produccion.split()[0]
            if primer_simbolo in self.terminals:
                primero.add(primer_simbolo)
            elif primer_simbolo != simbolo:
                conjunto_primero = self.calcular_primero(primer_simbolo)
                primero.update(conjunto_primero)
            else:
                continue
        return primero


    def calcular_siguiente(self, simbolo):
        siguiente = set()
        if simbolo == self.start.split()[0]:
            siguiente.add('$')
        for no_terminal in self.grammar:
            for produccion in self.grammar[no_terminal]:
                if simbolo in produccion:
                    lista = produccion.split()
                    simbolo_index = lista.index(simbolo)

                    if simbolo_index == len(lista) - 1:
                        if no_terminal != simbolo:
                            conjunto_siguiente = self.calcular_siguiente(no_terminal)
                            siguiente.update(conjunto_siguiente)
                    else:
                        siguiente_simbolo = lista[simbolo_index+1]
                        conjunto_primero = self.calcular_primero(siguiente_simbolo)
                        if 'ε' in conjunto_primero:
                            if no_terminal != simbolo:
                                conjunto_siguiente = self.calcular_siguiente(no_terminal)
                                siguiente.update(conjunto_siguiente)
                            conjunto_primero.remove('&')
                        siguiente.update(conjunto_primero)
        return siguiente