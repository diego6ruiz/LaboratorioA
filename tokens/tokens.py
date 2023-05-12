def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[1].replace("#","") 
		if token == 'ws':
			return None
		elif token == 'id':
			return ID
		elif token == 'number':
			return NUMBER
		elif token == ';':
			return SEMICOLON
		elif token == ':=':
			return ASSIGNOP
		elif token == '<':
			return LT
		elif token == '=':
			return EQ
		elif token == '+':
			return PLUS
		elif token == '-':
			return MINUS
		elif token == '*':
			return TIMES
		elif token == '/':
			return DIV
		elif token == '(':
			return LPAREN
		elif token == ')':
			return RPAREN
		else: 
			print("Error sintactico")