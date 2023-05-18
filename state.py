class State:
    def __init__(self, incidence, popularity, is_terminal_state):
        self.incidence = incidence
        self.popularity = popularity
        self.is_terminal_state = is_terminal_state

    def get_cost(self):
        cost = 0

        if self.is_terminal_state:
            cost = 800
        cost = cost + self.incidence

        return cost
    
