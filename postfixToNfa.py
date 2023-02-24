class State:
    def __init__(self, isEnd=False, transition=None, epsilonTransitions=None):
        if transition is None:
            transition = {}
        if epsilonTransitions is None:
            epsilonTransitions = []
        self.isEnd = isEnd
        self.transition = transition
        self.epsilonTransitions = epsilonTransitions

    def __str__(self):
        transition_str = ", ".join(f"{char} -> {state}" for char, state in self.transition.items())
        epsilon_str = ", ".join(str(state) for state in self.epsilonTransitions)
        return f"State(transition={{ {transition_str} }}, epsilon={{ {epsilon_str} }}, isEnd={self.isEnd})"




def postfix_to_nfa(postfix):
    stack = []
    state_counter = 0

    for char in postfix:
        if char == '.':
            # Pop the top two NFAs from the stack
            nfa2 = stack.pop()
            nfa1 = stack.pop()

            # Add epsilon transitions from nfa1's final state to nfa2's initial state
            for state in nfa1['final']:
                nfa1['transitions'].append((state, None, nfa2['initial']))

            # Combine the NFAs into a new NFA
            new_nfa = {
                'initial': nfa1['initial'],
                'final': nfa2['final'],
                'transitions': nfa1['transitions'] + nfa2['transitions']
            }

            # Push the new NFA onto the stack
            stack.append(new_nfa)

        elif char == '|':
            # Pop the top two NFAs from the stack
            nfa2 = stack.pop()
            nfa1 = stack.pop()

            # Create a new initial and final state and add epsilon transitions to the initial states of nfa1 and nfa2
            initial_state = state_counter
            state_counter += 1
            final_state = state_counter
            state_counter += 1
            nfa = {
                'initial': initial_state,
                'final': [final_state],
                'transitions': [(initial_state, None, nfa1['initial']), (initial_state, None, nfa2['initial'])] + nfa1['transitions'] + nfa2['transitions'] + [(state, None, final_state) for state in nfa1['final']] + [(state, None, final_state) for state in nfa2['final']]
            }

            # Push the new NFA onto the stack
            stack.append(nfa)

        elif char == '*':
            # Pop the top NFA from the stack
            nfa1 = stack.pop()

            # Create a new initial state and add epsilon transitions to nfa1's initial state and final states
            initial_state = state_counter
            state_counter += 1
            nfa = {
                'initial': initial_state,
                'final': nfa1['final'] + [initial_state],
                'transitions': [(initial_state, None, nfa1['initial']), (initial_state, None, state_counter)] + nfa1['transitions']
            }

            # Push the new NFA onto the stack
            stack.append(nfa)

        else:
            # Create a new initial and final state and add a transition between them
            initial_state = state_counter
            state_counter += 1
            final_state = state_counter
            state_counter += 1
            nfa = {
                'initial': initial_state,
                'final': [final_state],
                'transitions': [(initial_state, char, final_state)]
            }

            # Push the new NFA onto the stack
            stack.append(nfa)

    # The final NFA is the only element left on the stack
    final_nfa = stack.pop()
    # Return the NFA's components as separate iterables
    return final_nfa['initial'], final_nfa['final'], final_nfa['transitions']



def to_dot(initial_state, final_states, transitions):
    min_state = min(min(t[0], t[2]) for t in transitions)

    dot_graph = 'digraph {\n\trankdir=LR;\n'

    for state in set([t[0] for t in transitions] + [t[2] for t in transitions]):
        state -= min_state
        shape = 'doublecircle' if state in final_states else 'circle'
        dot_graph += f'\t{state} [shape={shape}];\n'

    for transition in transitions:
        source_state, input_symbol, target_state = transition
        source_state -= min_state
        target_state -= min_state
        label = 'ε' if input_symbol is None else input_symbol
        dot_graph += f'\t{source_state} -> {target_state} [label="{label}"];\n'

    initial_state -= min_state
    dot_graph += f'\tstart [shape=none,label=""];\n\tstart -> {initial_state};\n'

    dot_graph += '}'

    return dot_graph

