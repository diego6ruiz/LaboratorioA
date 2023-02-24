from infixToPostfix import *
from postfixToNfa import *


regex="ab*ab*"
postfix = to_postfix(insert_explicit_concat_operator(regex))
print(postfix)


initial_state, final_states, transitions = postfix_to_nfa(postfix)
print(initial_state, final_states, transitions)

print()
dot = to_dot(initial_state, final_states, transitions)
print(dot)