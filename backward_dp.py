from state import *
import random

class Backwards_DP:
    def __init__(self,actions):
        self.steps = 9
        self.actions = actions
        self.states = []
        self.create_states()
        self.calc_expected_cost()
        #print(self.states)
        

    def create_states(self):
        #TODO In der Aufgabenstellung steht "acht Wochen vor der Wahl" ==> 8 oder 9 Zeitschritten inklusive des Terminalzustandes
        #TODO In der Aufgabenstellung steht "Kosten linear in Höhe des Inzidenzwertes ... zudem Terminalkosten in höhe von 800 an"
        #TODO werden die Terminlalkosten aus Inzidenz + 800 "Kosten" errechnet (Zeile 24)
        for timesteps in range(self.steps): 
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

        
    
    def calc_expected_cost(self):
        for timestep in range(1,self.steps):

            for incidence in range(501): 
                for popularity in range(101):
                    
                    min_action_cost = None
                    for action in self.actions:
                        succ_set = []
                        for cost in action.costs:
                            succ_incidence = 0
                            succ_popularity = 0

                            if incidence + cost[0] > 500:
                                succ_incidence = 500
                            elif incidence + cost[0] < 0:
                                succ_incidence = 0
                            else:
                                succ_incidence = incidence + cost[0] 

                            if popularity + cost[1] > 100:
                                succ_popularity = 100
                            elif popularity + cost[1] < 0:
                                succ_popularity = 0
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
        
    def select_best_strategie(self,start_state):
        v_stern = []
        pi_stern = []
        current_state = start_state

        for timestep in range(self.steps-1):
            v_timestep, best_action = self.select_best_action(current_state,timestep)
            v_stern.append(v_timestep)
            pi_stern.append(best_action)

            #TODO Wie soll das Zufallsexperiment nach der Aktionsauswahl abgebildet werden?
            #TODO Aktuell wird ein random Integer aus dem Intervall 0-3 ausgewält
            #TODO (Da es sich um ein diskretes Intervall handelt ist die Wsk. identisch)  
            rnd = random.randint(0,3)
            current_state[0]  =  current_state[0] + best_action.costs[rnd][0]
            current_state[1]  =  current_state[1] + best_action.costs[rnd][1]
        return v_stern, pi_stern

    def select_best_action(self,state,timestep):
        incidence = state[0]
        popularity = state[1]
        min_action_cost = None

        for action in self.actions:
            succ_set = []
            for cost in action.costs:
                succ_incidence = 0
                succ_popularity = 0

                if incidence + cost[0] > 500:
                    succ_incidence = 500
                elif incidence + cost[0] < 0:
                    succ_incidence = 0
                else:
                    succ_incidence = incidence + cost[0] 

                if popularity + cost[1] > 100:
                    succ_popularity = 100
                elif popularity + cost[1] < 0:
                    succ_popularity = 0
                else: 
                    succ_popularity = popularity + cost[1]

                succ_set.append([succ_incidence, succ_popularity])
            
                current_cost = 0
                for succ in succ_set:

                    #current_cost += action.p * self.states[0][50][101]
                    current_cost += action.p * self.states[timestep+1][succ[0]][succ[1]]
                
                if min_action_cost == None or current_cost < min_action_cost:
                    min_action_cost = current_cost
                    best_action = action

        return min_action_cost, best_action

