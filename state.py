class State:
    def __init__(self,expected_value,popularity,incidence,best_action = None):
        self.expected_value = expected_value
        self.best_action = best_action
        self.popularity = popularity
        self.incidence = incidence
        