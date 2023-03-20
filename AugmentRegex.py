import math


def augment_regex(postfix):
    final_regex = '(' + postfix + ')#'
    return final_regex

def isOperator(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False

def regexFormat(re):
    isValid = True
    error = ''
    re = re.replace(' ', '')


    if '||' in re:
        error = 'No puede tener 2 "|" juntos' 
        return [], False, error

    if ('(|' in re) or ('(*' in re) or ('(?' in re) or ('(+' in re):
        error = 'No se puede encontrar un op despues de parentesis'
        return [], False, error
    
    if isOperator(re[0]):
        error = 'No se puede encontrar un op al principio del regex'
        return [], False, error

    if re[-1] == '|':
        error = 'No se puede encontrar un "|" al final del regex'
        return [], False, error

    if '|)' in re:
        error = 'No se puede encontrar un "|" antes de cerrar parentesis'
        return [], False, error

    reArray = []
    for caracterExpresion in re:
        reArray.append(caracterExpresion)

    numParenthesis = 0
    reArray = ["("] + reArray + [")"]
    tempLeft = []
    tempRight = []

  
    while ("(" in reArray) or (")" in reArray):
        while "(" in reArray:
            numParenthesis += 1
            indice = reArray.index('(')
            tempLeft = tempLeft + reArray[:indice+1]
            reArray = reArray[indice+1:]

        while ")" in reArray:
            if numParenthesis > 0:
                numParenthesis -= 1
                indice = reArray.index(')')
                tempRight = reArray[indice:] + tempRight
                reArray = reArray[:indice]
            else:
                error = 'Parentesis desbalanceados'
                return [], False, error


        while ('+' in reArray) or ('?' in reArray) or ('*' in reArray):
 
            andOp = []
            kleeneOp = []
            questionOp = []

            orden = []
            primero = None
            infinite = math.inf

            if '+' in reArray:
                andOp = ['+', reArray.index('+')]
            if '*' in reArray:
                kleeneOp = ['*', reArray.index('*')]
            if '?' in reArray:
                questionOp = ['?', reArray.index('?')]

            if andOp:
                orden.append(andOp)
            if kleeneOp:
                orden.append(kleeneOp)
            if questionOp:
                orden.append(questionOp)

            for i in orden:
                if i[1] < infinite:
                    infinite = i[1]
                    primero = i[0]

            index = reArray.index(primero)
            try:
                separationChar = reArray.pop(index-1)
                op = reArray.pop(index-1)

                sep1 = reArray[:index-1]
                sep2 = reArray[index-1:]

                if not sep1:
                    sep1 = [separationChar, op]
                    reArray = [sep1] + sep2
                else:
                    sep1.append([separationChar, op])
                    reArray = sep1 + sep2
            except IndexError:
                error = 'Error en reArray'
                isValid = False
                return [], isValid, error

        while isConcat(reArray):

            reArray = concatGroup(reArray)

        while '|' in reArray:

            index = reArray.index('|')
            try:
                separationChar = reArray.pop(index-1)
                op = reArray.pop(index-1)
                separationChar2 = reArray.pop(index-1)

                sep1 = reArray[:index-1]
                sep2 = reArray[index-1:]

                if not sep1:
                    sep1 = [separationChar, op, separationChar2]
                    reArray = [sep1] + sep2
                else:
                    sep1.append([separationChar, op, separationChar2])
                    reArray = sep1 + sep2
            except IndexError:
                error = 'Error en reArray'
                isValid = False
                return [], isValid, error

        if ("(" in tempLeft) and (")" in tempRight):
            if "(" in tempLeft:
                tempLeft.pop(-1)
            if ")" in tempRight:
                tempRight.pop(0)
            reArray = tempLeft + [reArray] + tempRight
            tempLeft = []
            tempRight = []
        else:
            error = 'Parentesis desbalanceados o incorrectos'
            isValid = False
            return [], isValid, error

    return reArray, isValid, error


def isConcat(reArray):
    concat = False
    for x in range(len(reArray) -1 ):
        if not isOperator(reArray[x]):
            if not isOperator(reArray[x + 1]):
                concat = True
                break

    return concat

def concatGroup(reArray):
    separation = []
    toNext = False
    for i in range(len(reArray)):  
        if toNext == False:  
            if i != (len(reArray) - 1):
                if (not isOperator(reArray[i])) and (not isOperator(reArray[i + 1])):
                    separation.append([reArray[i], reArray[i + 1]])
                    toNext = True
                else:
                    separation.append(reArray[i])
            else:
                separation.append(reArray[i])
                return separation
        else:
            if i != (len(reArray) - 1): 
                separation.append(reArray[i + 1])
            else:
                return separation
    return separation