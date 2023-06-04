from Direct import *
from Tree import *
from State import *
from prettytable import PrettyTable

class SLR(Automaton):
    def __init__(self, tokens, productions, ignore, simulation, scanner1Tokens):
        self.terminals = tokens
        self.grammar = productions
        self.ignore = ignore
        self.symbols = Set()
        self.producciones = self.formatSLR()
        self.initialState = None
        self.states = Set()
        self.transitions = []
        self.finalStates = Set()
        self.start = None
        self.action_table = [[]]
        self.goto_table = [[]]
        self.contador = 0
        self.cadena = simulation.result
        self.listaTokens = scanner1Tokens

    def SLR(self,):
        for produccion in self.producciones:
            if produccion.split("=>")[0] not in self.terminals:
                produccion = produccion.split("=>")
                produccion[1] = " ." + produccion[1]
                produccion = produccion[0] + "=>" + produccion[1]
                self.start = produccion
                cerradura  = self.cerradura(produccion)
                self.initialState = State("\n".join(cerradura), "inicial", None, self.contador, self.cerradura(produccion))
                break

        self.states.addElement(self.initialState)
        self.contador += 1

        for estado in self.states.elements:
            for symbol in self.symbols.elements:
                siguiente = self.ir_a(estado, symbol)
                if siguiente != None:
                    if self.verificarRepetidos(siguiente) == False:
                        siguiente.token = self.contador
                        self.states.addElement(siguiente)
                        self.contador += 1

                        if siguiente.type == "final":
                            self.finalStates.addElement(siguiente)

                    else:
                        for estado1 in self.states.elements:
                            if siguiente.productions == estado1.productions:
                                siguiente.token = estado1.token

                    self.addTransition(estado, siguiente, symbol)

        #self.pruebas()
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


    def calcular_siguiente(self, simbolo, iter = 0):

        if iter > 100:
            return set()

        siguiente = set()
        if simbolo == list(self.grammar.keys())[0]:
            siguiente.add('$')
        for no_terminal in self.grammar:
            for produccion in self.grammar[no_terminal]:
                if simbolo in produccion:
                    lista = produccion.split()
                    simbolo_index = lista.index(simbolo)

                    if simbolo_index == len(lista) - 1:
                        if no_terminal != simbolo:
                            conjunto_siguiente = self.calcular_siguiente(no_terminal, iter + 1)
                            siguiente.update(conjunto_siguiente)
                    else:
                        siguiente_simbolo = lista[simbolo_index+1]
                        conjunto_primero = self.calcular_primero(siguiente_simbolo)
                        if 'ε' in conjunto_primero:
                            if no_terminal != simbolo:
                                conjunto_siguiente = self.calcular_siguiente(no_terminal, iter + 1)
                                siguiente.update(conjunto_siguiente)
                            conjunto_primero.remove('&')
                        siguiente.update(conjunto_primero)
        return siguiente

    def tabla(self):
        # obtener símbolos terminales y no terminales
        simbolos_terminales = self.terminals + ['$']
        simbolos_no_terminales = self.symbols.Difference(Set(simbolos_terminales))

        #quitar los que esten en ignore
        for s in simbolos_terminales:
            if s in self.ignore:
                simbolos_terminales.remove(s)

        # inicializar la tabla go_to como una matriz vacía
        go_to_table = [[None] * len(simbolos_no_terminales) for _ in range(self.states.__len__())]

        # llenar la tabla go_to
        for transicion in self.transitions:
            if transicion[2] in simbolos_no_terminales.elements:
                simbolo = simbolos_no_terminales.elements.index(transicion[2])

                if go_to_table[transicion[0].token][simbolo] is None:
                    go_to_table[transicion[0].token][simbolo] = transicion[1].token
                else:
                    raise Exception("Error en la tabla de go_to")

        self.goto_table = go_to_table

        # inicializar la tabla action como una matriz vacía
        action_table = [[None] * len(simbolos_terminales) for _ in range(self.states.__len__())]

        # llenar la tabla action con los shift
        for transicion in self.transitions:
            if transicion[2] in simbolos_terminales:
                simbolo = simbolos_terminales.index(transicion[2])

                if action_table[transicion[0].token][simbolo] is None:
                    action_table[transicion[0].token][simbolo] = "S" + (transicion[1].token).__str__()
                else:
                    raise Exception("Error en la tabla de accion")

        # llenar la tabla con accept
        for i in range(1, self.states.__len__()):
            estado = self.states.elements[i]
            for produccion in estado.productions:
                if produccion.replace(".", "").strip() == self.start.replace(".", "").strip():
                    simbolo = simbolos_terminales.index("$")

                    if action_table[estado.token][simbolo] is None:
                        action_table[estado.token][simbolo] = "ACCEPT"
                        i = self.states.__len__()
                    else:
                        raise Exception("Error en la tabla de accion")
                    break


        # Llenar la tabla con reduce
        for i in range(self.states.elements.__len__()):
            estado = self.states.elements[i]
            for produccion in estado.productions:
                if produccion.endswith('.'):
                    simbolos = produccion.split('=>')[0]
                    simbolos_no_espacios = simbolos.replace(' ', '')
                    follow = self.calcular_siguiente(simbolos_no_espacios)

                    for simbolo in follow:
                        if simbolo in simbolos_terminales:
                            simbolo_index = simbolos_terminales.index(simbolo)
                            if action_table[estado.token][simbolo_index] is None:
                                action_table[estado.token][simbolo_index] = "R" + self.buscarEstado(produccion).__str__()
                            else:
                                raise Exception("Error en la tabla de accion" + "[" + estado.token.__str__() + ", " + simbolo + "] = " + "(" + action_table[estado.token][simbolo_index] + ", " + "R" + self.buscarEstado(produccion).__str__() + ")")
                            
        self.action_table = action_table

        # Imprimir la tabla de Acción
        print("\nTabla de Acción:")
        headers = simbolos_terminales
        accion_table = PrettyTable(headers)
        for i in range(self.states.__len__()):
            accion_table.add_row(action_table[i])
        print(accion_table)

        # Imprimir la tabla de Goto
        print("\nTabla de Goto:")
        headers = simbolos_no_terminales.elements
        goto_table = PrettyTable(headers)
        for i in range(self.states.__len__()):
            goto_table.add_row(go_to_table[i])
        print(goto_table)

        self.terminals = simbolos_terminales
        self.non_terminals = simbolos_no_terminales.elements


    def buscarEstado(self, produccion):
        for i in range(self.initialState.productions.__len__()):
            p = self.initialState.productions[i]
            if produccion.replace(".", "").strip().replace(" ","") == p.replace(".", "").strip().replace(" ",""):
                return i

    def simulacion(self):
        stack = [self.initialState]  # Pila de estados
        input_symbols = self.parseCadena().split()  # Símbolos de entrada

        while True:
            state = stack[-1]  # Estado en la cima de la pila

            # Verificar si hay símbolos de entrada disponibles
            if input_symbols:
                symbol = input_symbols[0]  # Siguiente símbolo de entrada
            else:
                # No hay más símbolos de entrada, se asume un símbolo vacío ('$')
                symbol = '$'

            # Obtener la acción correspondiente al estado y símbolo actual
            action = self.action_table[state.token][self.terminals.index(symbol)]

            if action is None:  # Error
                # Llamar a la rutina de recuperación de errores
                print("Cadena NO aceptada")
                return "NO"

            if action.startswith("S"):  # Shift
                next_state = self.GetItem(int(action[1:]))
                stack.append(next_state)
                input_symbols = input_symbols[1:]  # Consumir el símbolo de entrada
            elif action.startswith("R"):  # Reduce
                production_index = int(action[1:])
                production = self.initialState.productions[production_index]
                lhs, rhs = production.split("=>")
                lhs = lhs.strip()
                rhs_symbols = rhs.strip().replace(".","").split()

                # Pop |rhs_symbols| symbols from the stack
                stack = stack[:-len(rhs_symbols)]

                # Get the new top state from the stack
                top_state = stack[-1]

                # Get the next state using GOTO table
                next_state = self.GetItem(self.goto_table[top_state.token][self.non_terminals.index(lhs)])

                stack.append(next_state)

            elif action == "ACCEPT":  # Aceptación
                print("Cadena aceptada")
                return "YES"
            else:
                # Llamar a la rutina de recuperación de errores
                print("Cadena NO aceptada")
                return "NO"

    def errorRecovery(self):
        # Implementar la rutina de recuperación de errores aquí
        print("Error recovery routine")
    
    def GetItem(self, token):
        for estado in self.states.elements:
            if estado.token == token:
                return estado
    
    def parseCadena(self):
        result = ""
        for tupla in self.cadena:
            if tupla[1].replace("#","") in self.listaTokens:
                result += (self.listaTokens[tupla[1].replace("#","")]).replace("return", "") + " "

        return result.strip()
