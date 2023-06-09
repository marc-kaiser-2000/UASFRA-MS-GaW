import random
import state
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import numpy as np

class Backwards_DP:
    def __init__(self,actions):
        self.steps = 9
        self.actions = actions
        self.states = []
        self.create_states()
        self.calc_expected_cost()
        #print(self.states)
        

    def create_states(self):
        for timesteps in range(self.steps): 
            self.states.append([])
            for incidence in range(501):
                self.states[timesteps].append([])
                for popularity in range(101):
                    if timesteps == 0 and popularity < 50 :
                        self.states[timesteps][incidence].append(state.State(800 + incidence))
                    elif timesteps == 0:
                        self.states[timesteps][incidence].append(state.State(incidence))
                    else:
                        self.states[timesteps][incidence].append(state.State(0))

        
    
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
                            current_cost += action.p * self.states[timestep-1][succ[0]][succ[1]].expected_value
                        
                        if min_action_cost == None or current_cost < min_action_cost:
                            best_action = action
                            min_action_cost = current_cost

                    self.states[timestep][incidence][popularity].expected_value = min_action_cost
                    self.states[timestep][incidence][popularity].best_action = best_action

        
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
    
    def plot(self) -> None:
        """
        for timestep in range(self.steps-1):
            print("Plotting Step: " + str(timestep))
            fig, ax = plt.subplots()
            ax.set_xlabel('Incidence')
            ax.set_ylabel('Popularity')
            ax.set_title('Best action at T: '+ str(timestep))
            ax.set_xlim(0,501)
            ax.set_ylim(0,101)
            for incidence in range(501): 
                for popularity in range(101):
                    x = [incidence, incidence, incidence+1, incidence+1]
                    y = [popularity, popularity + 1, popularity + 1,popularity]


                    ax.fill(x, y,self.states[self.steps-timestep-1][incidence][popularity].best_action.color)
            first_patch = mpatches.Patch(color=self.actions[0].color, label=self.actions[0].name)
            second_patch = mpatches.Patch(color=self.actions[1].color, label=self.actions[1].name)
            third_path = mpatches.Patch(color=self.actions[2].color, label=self.actions[2].name)
            forth_patch = mpatches.Patch(color=self.actions[3].color, label=self.actions[3].name)
            plt.legend(handles=[first_patch, second_patch, third_path, forth_patch],loc="upper right")

            fig.savefig(".\\Results\\Figure_"+str(timestep)+".png")
        """
        
                 
        print("Plotting Step: " + str(self.steps-1))
        fig, ax = plt.subplots()
        ax.set_xlabel('Incidence')
        ax.set_ylabel('Popularity')
        ax.set_title('Terminal Cost at T: '+ str(self.steps-1))
        ax.set_xlim(0,501)
        ax.set_ylim(0,101)
        color_gradient = self.get_color_gradient("#0cad24","#fc0303",1301)
        for incidence in range(501): 
            for popularity in range(101):
                x = [incidence, incidence, incidence+1, incidence+1]
                y = [popularity, popularity + 1, popularity + 1,popularity]

                
                ax.fill(x, y,color_gradient[round(self.states[0][incidence][popularity].expected_value)])

        first_patch = mpatches.Patch(color="#0cad24", label="Terminal Cost of 0")
        second_patch = mpatches.Patch(color="#fc0303", label="Terminal Cost of 1300")

        plt.legend(handles=[first_patch, second_patch],loc="upper right")
        
        #cm = mcolors.LinearSegmentedColormap.from_list(name="TerminalCostMap",colors=color_gradient,N=1300)  
        #fig.colorbar(cm,ax=ax)
        fig.savefig(".\\Results\\Figure_"+str(self.steps-1)+".png")
        plt.show()

    def hex_to_RGB(self,hex_str):
        """ #FFFFFF -> [255,255,255]"""
        #Pass 16 to the integer function for change of base
        return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

    def get_color_gradient(self,c1, c2, n):
        """
        Given two hex colors, returns a color gradient
        with n colors.
        """
        assert n > 1
        c1_rgb = np.array(self.hex_to_RGB(c1))/255
        c2_rgb = np.array(self.hex_to_RGB(c2))/255
        mix_pcts = [x/(n-1) for x in range(n)]
        rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
        return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]
