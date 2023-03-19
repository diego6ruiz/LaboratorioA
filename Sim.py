from operators import *

def AFD_SIM(transitions, cadena, final_char, alphabet, tree):
    dot = graphviz.Digraph(comment="AFD", format='pdf')
    dot.attr(rankdir="LR")

    for key in transitions.keys():
        states = key.replace("[","")
        states = states.replace("]","")
        states = states.replace(" ","")
        states = states.split(",")
        if str(tree.right.value) in states:
            dot.node(transitions[key]["name"], transitions[key]["name"], shape='doublecircle')
        else:
            dot.node(transitions[key]["name"], transitions[key]["name"])
    for key, v in transitions.items():
        for c in alphabet:
            if v["name"] != None and v[c] != None:
                dot.edge(v["name"], v[c], c)
    dot.render(directory='output', filename='AFD-direct')
    current_state = "S0"
    for char in cadena:
        llave = ""
        for key, v in transitions.items():
            if v["name"] == current_state and v[char] != None:
                llave = key
            elif v["name"] == current_state and v[char] == None:
                return False
        current_state = transitions[llave][char]
    for key, v in transitions.items():
        if v["name"] == current_state:
            states = key.replace("[","")
            states = states.replace("]","")
            states = states.replace(" ","")
            states = states.split(",")
            if final_char in states:
                return True
            else:
                return False