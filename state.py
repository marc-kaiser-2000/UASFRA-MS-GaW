class State:
    def __init__(self,expected_value,best_action = None):
        self.expected_value = expected_value
        self.best_action = best_action
        