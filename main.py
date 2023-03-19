import infixToPostfix as pos
from postfixToNfa import *
from funcs import *
from Tree import *
from Sim import *
from operators import *
from AugmentRegex import *


import sys

ABC = [letter for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#0123456789\u03B5']
IMAGES_DIRECTORY = '/output/'

inicio = 0
fin = 0

regex = input('Ingrese una expresion regular r: ')
if regex == '':
    regex = 'ε'

cadena = input('Ingrese una cadena w a ser validada: ')

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
    print('Regex:', regex)
    reg = pos.insert_explicit_concat_operator(regex)
    postfix = pos.to_postfix(reg)
    print('Postfix: ', postfix)

    tree = construir_arbol(postfix)
    print_arbol(tree, 'output/arbol')
    fna = construir_FNA_desde_arbol(tree)
    print(fna)
    g = generar_grafo_FNA(fna)
    
    
    
    #yesno = use_direct(regex, cadena)
    augmented_regex = augment_regex(postfix)
    #     (a.b*.a.b*).#
    print(augmented_regex)

