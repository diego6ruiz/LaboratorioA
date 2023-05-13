def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[1].replace("#","") 
		if token == 'ws':
			return None
		elif token == 'id':
			return ID
		else: 
			print("Error sintactico")