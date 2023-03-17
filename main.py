#from infixToPostfix import *
#from postfixToNfa import *

'''/
/regex="ab*ab*"
/postfix = to_postfix(insert_explicit_concat_operator(regex))
/print(postfix)
/
/
/initial_state, final_states, transitions = postfix_to_nfa(postfix)
/print(initial_state, final_states, transitions)
/
/print()
/dot = to_dot(initial_state, final_states, transitions)
/print(dot)
'''

import infixToPostfix as pos
from postfixToNfa import *
import sys


inicio = 0
fin = 0

regex = input('Ingrese la Expresion regular: ')
if regex == '':
    regex = 'ε'

for caracter in regex:
    if caracter == '(':
        inicio += 1
    if caracter == ')':
        fin += 1

if inicio > fin or fin > inicio:
    print('\nVERIFIQUE LOS PARENTESIS. \nHAY ', inicio,
          'PARENTESIS INICIALES Y ', fin, 'PARENTESIS FINALES.')
    sys.exit()
else:
    print('Expresion Infix:', regex)
    concatRegex = pos.insert_explicit_concat_operator(regex)
    print('Expresion con el operador de concatenacion: ', concatRegex)
    postfix = pos.to_postfix(concatRegex)
    print('Expresion Postfix: ', postfix)


    tree = construir_arbol(postfix)
    print_arbol(tree, 'output/arbol sintactico')
    fna = construir_FNA_desde_arbol(tree)
    print(fna)
    g = generar_grafo_FNA(fna,1)


    