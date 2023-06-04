class ScannerYapar:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.ignore = []
        self.productions = {}
        self.variablesYalex = []

    def scan(self, variables):
        
        for key, value in variables.items():
            self.variablesYalex.append(value.replace("return","").replace(" ","").strip())

        with open(self.filename, 'r') as f:
            content = f.read()

        is_parsing_tokens = False
        token = ''
        production = ''
        inComment = False
        comentario = ''

        for symbol in content:

            if production == '/*':
                inComment = True
                production = ''
                continue

            if inComment:
                comentario += symbol
                if comentario.__contains__('*/'):
                    inComment = False
                    comentario = ''
                continue

            if "IGNORE" in production:
                token = production
                production = ''
                is_parsing_tokens = True

            if is_parsing_tokens:
                if symbol == '%':
                    is_parsing_tokens = False
                elif symbol == '\n':
                    if 'token' in token:
                        token = token.split(' ', 1)[1]
                        if " " in token:
                            for t in token.split(" "):
                                t = t.strip()
                                if (t.strip() in self.variablesYalex):
                                    self.tokens.append(t)
                                else:
                                    raise Exception('El token no esta definido en Yalex', t)
                                
                        else:
                            if (token.strip() in self.variablesYalex):
                                self.tokens.append(token.strip())
                            else:
                                raise Exception('El token no esta definido en Yalex', token)

                        token = ''
                        is_parsing_tokens = False

                    elif 'IGNORE' in token:
                        token = token.replace("IGNORE", "").strip()
                        self.ignore.append(token)
                        token = ''
                        is_parsing_tokens = False


                    else:
                        raise Exception('Error en la sintaxis de declaracion del token', token)
                    
                else:
                    token += symbol

            else:
                if symbol == ";":
                    production = production.split(':')
                    lhs = production[0].strip()
                    rhs = [p.strip() for p in production[1].split("|")]
                    self.productions[lhs] = rhs if len(rhs) > 1 else [rhs[0]]
                    production = ''
                    
                else:
                    if symbol == '%':
                        is_parsing_tokens = True
                    elif symbol == '\n' or symbol == '\t':
                        pass
                    else:
                        production += symbol
        return (self.tokens, self.productions, self.ignore)