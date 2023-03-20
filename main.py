import infixToPostfix as pos
import postfixToNfa as nfa
import RegexToDFA as dfa
import NFAtoDFA as nfaDfa
from Sim import *
from AugmentRegex import *
import utils as diag
import Sim as sim


import sys

ABC = [letter for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#0123456789\u03B5']
IMAGES_DIRECTORY = '/output/'

inicio = 0
fin = 0

regex = input('Ingrese una reArray regular r: ')
if regex == '':
    regex = 'ε'

w = input('Ingrese una cadena w a ser validada: ')

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

    #prep
    arbolFNA, isValid, error = regexFormat('(' + regex + ')')
    arbolFDA, isValid, error = regexFormat('(' + regex + ')#')

    tree = nfa.construir_arbol(postfix)
    nfa.print_arbol(tree, 'output/arbol')
   
    #FNA 
    fna = diag.core_NFA(arbolFNA)
    diag.draw_fna(fna)
    isRegexLanguage = sim.NFASim(fna, w)
    if isRegexLanguage:
        isAccepted = 'SI'
    else:
        isAccepted = 'NO'
    print('FNA: La cadena '+w+' '+isAccepted+' es aceptada por el lenguaje de la expresion ' +reg)

    #FDA Direct
    DirectFDA = diag.core_DirectFDA(arbolFDA)
    diag.draw_dfa(DirectFDA)
    isRegexLanguage = sim.DFASim(DirectFDA, w)
    if isRegexLanguage:
        isAccepted = 'SI'
    else:
        isAccepted = 'NO'
    print('DIRECT DFA: La cadena '+w+' '+isAccepted+' es aceptada por el lenguaje de la expresion ' +reg)


    #DFA Subconjuntos
    SubFDA = diag.core_SubFDA(fna)
    diag.draw_dfaSub(SubFDA)
    isRegexLanguage = sim.DFASim(SubFDA, w)
    if isRegexLanguage:
        isAccepted = 'SI'
    else:
        isAccepted = 'NO'
    print('SUBCONJUNTOS DFA: La cadena '+w+' '+isAccepted+' es aceptada por el lenguaje de la expresion ' +reg)

    
    #DFA Minimizacion
    minDFA = diag.core_minDFA(SubFDA)
    diag.draw_dfaMin(minDFA)
    isRegexLanguage = sim.DFASim(minDFA, w)
    if isRegexLanguage:
        isAccepted = 'SI'
    else:
        isAccepted = 'NO'
    print('DFA MINIMIZADO: La cadena '+w+' '+isAccepted+' es aceptada por el lenguaje de la expresion ' +reg)