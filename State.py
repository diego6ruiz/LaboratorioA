class State:
    def __init__(self, id, type, AFN_states = None, token = None, productions = None):
        self.id = id
        self.type = type
        self.AFN_states = AFN_states
        self.token = token
        self.productions = productions

    def __str__(self):
        return (str(self.id)+ " " + self.type)