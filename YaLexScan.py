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
        self.rule_tokens = False
        self.finalReg = ""
        self.alphabet = [chr(i) for i in range(256)]
        self.NumAlphabet = [str(i) for i in range(256)] #ASCII string
        self.operadores = ["|", "*", "+", "?", "(", ")", "•"]
        
    def scan(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        for line in lines:  
            #Obviar comentarios 
            if "(*" in line and "*)" not in line:
                    raise Exception("Falta cierre de comentario: " + line)
            elif "*)" in line and "(*" not in line:
                raise Exception("Falta apertura de comentario: " + line)
            if not line.strip():
                continue

            #Si encuentra un let, guardar la palabra siguiente como llave de diccionario y su valor
            if 'let' in line:
                key_value = line.split('=')
                key = key_value[0].strip().split()[1]
                value = key_value[1].strip()

                # Verificar si tiene brackets
                if '[' in value and ']' not in value:
                    raise Exception("Falta bracket de cierre: " + line)
                elif ']' in value and '[' not in value:
                    raise Exception("Falta bracket de apertura: " + line)

                self.variables[key] = value
                continue

            if 'rule tokens' in line:
                self.rule_tokens = True
                continue
            if self.rule_tokens:

                #Verificar si tiene curly brackets
                if '{' in value and '}' not in value:
                    raise Exception("Falta curly bracket de cierre: " + line)
                elif '}' in value and '{' not in value:
                    raise Exception("Falta curly bracket de apertura: " + line)

                temporary_word = ""
                temporary_fun = ""
                fun = False
                in_comment = False

                for i, x in enumerate(line):

                    #Chequear si estamos en codigo comentado
                    if x == "(" and i < len(line) - 1 and line[i+1] == "*":
                        in_comment = True
                    elif x == "*" and i < len(line) - 1 and line[i+1] == ")":
                        in_comment = False
                        continue
                    if in_comment:
                        continue

                    if x != " "  and x != "\t" and x != "\n" and x != "'" and x != "|":
                        if x == "{":
                            fun = True
                        elif x == "}":
                            temporary_fun += x
                            break
                        
                        if fun:
                            temporary_fun += x
                        else:
                            temporary_word += x

                self.tokens[temporary_word] = temporary_fun

        #Convertir a reg con concatenacion
        self.convertRegex()
        self.addConcatenation()

        for key, value in self.variables.items():
            self.variables[key] = self.recursiveSerach(value) 
       
        for key, value in self.tokens.items():
            if key in self.variables.keys():
                self.finalReg += self.variables[key] + "|"
            else:
                simbol = ""
                if len(key) > 1:
                    for i in key:
                        if i != "'" and i != '"' and i != " ":
                            simbol += str(Simbolo(i)) + "•"
                    self.finalReg += simbol[:-1] + "|"

                else:
                    self.finalReg += str(Simbolo(key)) + "|"
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