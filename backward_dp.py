from state import *

class Backwards_DP:
    def __init__(self,actions):
        self.steps = 8
        self.actions = actions
        self.states = []
        self.create_states2()
        self.calc_expected_cost()
        print(self.states)
        

    def create_states(self):
        #TODO check if we need 8 or 9 timesteps
        for timesteps in range(8): 
            self.states.append([])
            for incidence in range(50):
                for popularity in range(10):
                    if timesteps == 0:
                        self.states[timesteps].append(State(incidence,popularity,True))
                    else:
                        self.states[timesteps].append(State(incidence,popularity,False))

    def create_states2(self):
        #TODO check if we need 8 or 9 timesteps
        #TODO check if we have to add incidence and treminal cost 
        for timesteps in range(8): 
            self.states.append([])
            for incidence in range(501):
                self.states[timesteps].append([])
                for popularity in range(101):
                    if timesteps == 0 and popularity < 50 :
                        self.states[timesteps][incidence].append(800 + incidence)
                    elif timesteps == 0:
                        self.states[timesteps][incidence].append(incidence)
                    else:
                        self.states[timesteps][incidence].append(0)

        print("Test")
    
    def calc_expected_cost(self):
        for timestep in range(1,8):

            for incidence in range(501): 
                for popularity in range(101):
                    
                    #TODO check if we can ignore states with 0 prob multiplication
                    min_action_cost = None
                    for action in self.actions:
                        succ_set = []
                        for cost in action.costs:
                            succ_incidence = 0
                            succ_popularity = 0

                            if incidence + cost[0] > 500:
                                succ_incidence = 500
                            else:
                                succ_incidence = incidence + cost[0] 

                            if popularity + cost[1] > 100:
                                succ_popularity = 100
                            else: 
                                succ_popularity = popularity + cost[1]

                            succ_set.append([succ_incidence, succ_popularity])


                        current_cost = 0
                        for succ in succ_set:

                            #current_cost += action.p * self.states[0][50][101]
                            current_cost += action.p * self.states[timestep-1][succ[0]][succ[1]]
                        
                        if min_action_cost == None or current_cost < min_action_cost:
                            min_action_cost = current_cost

                    self.states[timestep][incidence][popularity] = min_action_cost
        
        print("Test 2")