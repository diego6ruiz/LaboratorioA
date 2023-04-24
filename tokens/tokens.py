def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[1].replace("#","") 
		if token == 'ws':
			return None
		else: 
			print("Error sintactico")		elif token == 'id':
			return ID
		else: 
			print("Error sintactico")		elif token == 'number':
			return NUMBER
		else: 
			print("Error sintactico")		elif token == ';':
			return SEMICOLON
		else: 
			print("Error sintactico")		elif token == ':=':
			return ASSIGNOP
		else: 
			print("Error sintactico")		elif token == '<':
			return LT
		else: 
			print("Error sintactico")		elif token == '=':
			return EQ
		else: 
			print("Error sintactico")		elif token == '+':
			return PLUS
		else: 
			print("Error sintactico")		elif token == '-':
			return MINUS
		else: 
			print("Error sintactico")		elif token == '*':
			return TIMES
		else: 
			print("Error sintactico")		elif token == '/':
			return DIV
		else: 
			print("Error sintactico")		elif token == '(':
			return LPAREN
		else: 
			print("Error sintactico")		elif token == ')':
			return RPAREN
		else: 
			print("Error sintactico")