def insert_explicit_concat_operator(exp):
    output = ''

    for i in range(len(exp)):
        token = exp[i]
        output += token
        if token == '(' or token == '|':
            continue
        if i < len(exp) - 1:
            lookahead = exp[i + 1]
            if lookahead == '*' or lookahead == '?' or lookahead == '+' or lookahead == '|' or lookahead == ')':
                continue
            output += '.'
    return output

def peek(stack):
    return stack[-1] if len(stack) else None


operator_precedence = {
    '|': 0,
    '.': 1,
    '?': 2,
    '*': 2,
    '+': 2,
    '^': 3
}

def to_postfix(exp):
    output = ''
    operator_stack = []

    for token in exp:
        if token == '.' or token == '|' or token == '*' or token == '?' or token == '+':
            while operator_stack and peek(operator_stack) != '(' \
                    and operator_precedence[peek(operator_stack)] >= operator_precedence[token]:
                output += operator_stack.pop()

            operator_stack.append(token)
        elif token == '(' or token == ')':
            if token == '(':
                operator_stack.append(token)
            else:
                while peek(operator_stack) != '(':
                    output += operator_stack.pop()
                operator_stack.pop()
        else:
            output += token

    while operator_stack:
        output += operator_stack.pop()

    return output