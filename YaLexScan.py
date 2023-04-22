class Simbolo:
    def __init__(self, c_id):
        self.id = self.toAscii(c_id)
        self.c_id = c_id

    def __str__(self):
        return str(self.id)
    
    def toAscii(self, c_id):
        if(c_id == "\\s"):
           return 32
        elif(c_id == "\\n"):
            return 10
        elif(c_id == "\\t"):
            return 9
        else:
            return ord(c_id)

class Scanner:
    def __init__(self, filename):
        self.filename = filename
        self.variables = {}
        self.tokens = {}
        self.ruleTokens = False
        self.finalReg = ""
        self.alphabet = [chr(i) for i in range(256)]
        self.NumAlphabet = [str(i) for i in range(256)] #ASCII string
        self.operadores = ["|", "*", "+", "?", "(", ")", "•"]
        
    def scan(self):

        word=""
        ruleTokens = []
        functions = []

        with open(self.filename, 'r') as f:
            lines = f.readlines()

        activeRule = False

        for l in lines:
            if activeRule:
                if l == "|":
                    if word.strip() != "":
                        ruleTokens.append(word.strip())
                        word = ""
                else:
                    word += l
                    if "{" in word and "}" in word:
                        word = word.strip()
                        ruleTokens.append(word)
                        word = ""
                    elif "(*" in word and "*)" in word:
                        word = ""

            else:
                word += l

                if "\n" in word:
                    if word:
                        if "let" in word:
                            index = word.index("let") + len("let") 
                            print(word[index])
                            if word[index] == " ":
                                functions.append(word[index:].strip())
                            else:
                                raise Exception("Error en la declaracion de variables " + word)

                        elif "rule" in word:
                            index = word.index("rule") + len("rule")
                            if word[index] == " ":
                                activeRule = True
                            else:
                                raise Exception("Error en la declaracion de reglas " + word)

                        word = ""
                        
        for rule in ruleTokens:
            if not rule == "|" :
                temporary_word = ""
                temporary_fun = ""
                fun = False
            
                for symbol in rule:

                    if symbol != "'" and symbol != "|":
                        if symbol == "{":
                            fun = True
                        elif symbol == "}":
                            temporary_fun += symbol
                            break
                        
                        if fun:
                            temporary_fun += symbol
                        else:
                            temporary_word += symbol

                if "(*" in temporary_word and "*)" in temporary_word:
                    start_index = temporary_word.index("(*")
                    end_index = temporary_word.index("*)", start_index) + 2
                    temporary_word = temporary_word[:start_index] + temporary_word[end_index:]
                            
                if "(*" in temporary_fun and "*)" in temporary_fun:
                    start_index = temporary_fun.index("(*")
                    end_index = temporary_fun.index("*)", start_index) + 2
                    temporary_fun = temporary_fun[:start_index] + temporary_fun[end_index:]

                self.tokens[temporary_word.strip()] = temporary_fun.replace("{", "").replace("}","").strip()


        for function in functions:
            key_value = function.split('=')
            key = key_value[0].strip()
            value = key_value[1].strip()

            self.variables[key] = value
            
        self.convertRegex()

        self.addConcatenation()

        for key, value in self.variables.items():
            self.variables[key] = self.recursiveSerach(value) 
        for key, value in self.tokens.items():
            agregar = ""

            if key in self.variables.keys():
                agregar += self.variables[key]
            else:
                simbol = ""
                if len(key) > 1:
                    for i in key:
                        if i != "'" and i != '"' and i != " ":
                            simbol += str(Simbolo(i)) + "•"
                    agregar += simbol[:-1] 

                else:
                    agregar += str(Simbolo(key))

            #agregar .#funcion
            self.finalReg += agregar + '•"#' + key.replace('"',"") + '"|'

        self.finalReg = self.finalReg[:-1]



    def convertRegex(self):
        for key, value in self.variables.items():
            if "[" in value:
                first = value.find('[')
                last = value.find(']')
                inside = value[first+1:last]
                before = value[:first+1]
                after = value[last:]

                if inside.startswith ('"') and inside.endswith ('"'):
                    
                    first1 = inside.find('"')
                    last1 = inside.rfind('"')
                    inside1 = inside[first1+1:last1]

                    temp = ""
                    tempFinal = ""
                    contador = 0
                    while contador < len(inside1):
                        temp += inside1[contador]

                        if temp =="\\":
                            if inside1[contador+1] == "s":
                                tempFinal += str(ord(" ")) + "|"
                                temp = ""
                                contador += 2

                            elif inside1[contador+1] == "t":
                                tempFinal += str(ord("\t")) + "|"
                                temp = ""
                                contador += 2

                            elif inside1[contador+1] == "n":
                                tempFinal += str(ord("\n")) + "|"
                                temp = ""
                                contador += 2

                        else:

                            if temp in self.alphabet:
                                continue
                            else:
                                tempFinal += str(ord(temp[:-1])) + "|"
                                temp = ""
                                contador += 1
                    self.variables[key] = before + tempFinal[:-1] + after
                    
                else:
                    open = False
                    enComillas = ""
                    tempFinal = []
                    for i, x in enumerate(inside):
                        if x == "'":
                            if open:
                                if enComillas == "\\s":
                                    tempFinal.append(str(ord(" ")))
                                    enComillas = ""
                                elif enComillas == "\\t":
                                    tempFinal.append(str(ord("\t")))
                                    enComillas = ""
                                elif enComillas == "\\n":
                                    tempFinal.append(str(ord("\n")))
                                    enComillas = ""
                                else:
                                    tempFinal.append(str(ord(enComillas)))
                                    enComillas = ""

                            open = not open

                        else:
                            if not open:
                                tempFinal.append(x)
                            else:
                                enComillas+= x

                    if "-" in tempFinal:
                        rango = ""
                        for i, x in enumerate(tempFinal):
                            if x == "-":
                                for j in range(int(tempFinal[i-1]), int(tempFinal[i+1])+1):
                                    rango += str(j) + "|"

                        self.variables[key] = before+ rango[:-1] + after

                    else:
                        self.variables[key] = before +  "|".join(tempFinal) +after


    def recursiveSerach(self, value):
        if(value.startswith('[')) and (value.endswith(']')):
            return value.replace('[','(').replace(']',')')
        if value in self.variables.keys():
            return self.variables[value]
        if value in self.operadores:
            return value
        if value in self.alphabet:
            return str(ord(value))
        if value in self.NumAlphabet:
            return value
        else:
            if '(' in value:
                first = value.find('(')
                last = value.find(')')

                inside = value[first+1:last]
                inside = self.recursiveSerach(inside)

                before = value[:first]
                before = self.recursiveSerach(before)

                after = value[last+1:]
                after = self.recursiveSerach(after)
                
                return before + "(" + inside + ")" + after
            
            if '[' in value:    

                first = value.find('[')
                last = value.find(']')

                inside = value[first+1:last]

                before = value[:first]
                before = self.recursiveSerach(before)

                after = value[last+1:]
                after = self.recursiveSerach(after)
                
                return before + "(" + inside + ")" + after


            elif "|" in value:
                first = value.find('|')

                left = value[:first]
                left = self.recursiveSerach(left)

                right = value[first+1:]
                right = self.recursiveSerach(right)

                return left + "|" + right
            
            
            elif '•' in value:
                first = value.find('•')

                left = value[:first]
                left = self.recursiveSerach(left)

                right = value[first+1:]
                right = self.recursiveSerach(right)

                return left + "•" + right
            
            if '+' in value:
                return(self.recursiveSerach(value.split('+')[0]) + "+")
            
            elif '?' in value:
                return(self.recursiveSerach(value.split('?')[0]) + "?")

            elif '*' in value:
                return(self.recursiveSerach(value.split('*')[0]) + "*")

            else:

                if value == "":
                    return value     
            
                elif "'" in value:
                    return (self.recursiveSerach(value.replace("'", "")))
                
                else:
                    raise Exception("Variable not found: " + value + "")
                
    def addConcatenation(self):
        for key, value in self.variables.items():
            if not value.startswith('['):
                expresiones = []
                temp = ""
                for i, x in enumerate(value):
                    if x == "+" or x == "*" or x == "?"  or x == "|" or x == "(" or x == ")" or x == "." or x == "[" or x == "]" :
                        if(temp != ""):
                            expresiones.append(temp)
                            temp = ""
                        expresiones.append(x)
                    else:
                        temp += x

                if(temp != ""):
                    expresiones.append(temp)

                new_expr = []
                for i, token in enumerate(expresiones):
                    if i > 0:
                        if token in self.variables.keys() and expresiones[i-1] in self.variables.keys():
                            new_expr.append("•")
                        elif token in self.variables.keys() and expresiones[i-1] == ')':
                            new_expr.append("•")
                        elif token == '(' and expresiones[i-1] in self.variables.keys():
                            new_expr.append("•")
                        elif token == '(' and expresiones[i-1] == ')':
                            new_expr.append("•")
                        elif expresiones[i-1] == '?' and (token in self.variables.keys() or token == '(' or token == '['):
                            new_expr.append("•")
                        elif expresiones[i-1] == '*' and (token in self.variables.keys() or token == '(' or token == '['):
                            new_expr.append("•")
                        elif expresiones[i-1] == '+' and (token in self.variables.keys() or token == '(' or token == '['):
                            new_expr.append("•")
                        elif token == "[" and (expresiones[i-1].replace("'","") in self.alphabet):
                            new_expr.append("•")
                        elif token in self.variables.keys() and expresiones[i-1] in self.alphabet and expresiones[i-1] not in self.operadores:
                            new_expr.append("•")
                        
                    new_expr.append(token)
                self.variables[key] = ''.join(new_expr)