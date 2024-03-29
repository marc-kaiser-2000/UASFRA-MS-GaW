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
        self.succ_states = []
        self.create_states()
        self.calc_expected_cost()
        self.reelection_prop = 0
        
        

    def create_states(self):
        for timesteps in range(self.steps): 
            self.states.append([])
            for incidence in range(501):
                self.states[timesteps].append([])
                for popularity in range(101):
                    if timesteps == 0 and popularity < 50 :
                        self.states[timesteps][incidence].append(state.State(800 + incidence,popularity,incidence))
                    elif timesteps == 0:
                        self.states[timesteps][incidence].append(state.State(incidence,popularity,incidence))
                    else:
                        self.states[timesteps][incidence].append(state.State(0,popularity,incidence))

        
    
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

                            current_cost += action.p * (incidence+self.states[timestep-1][succ[0]][succ[1]].expected_value)

                        if min_action_cost == None or current_cost < min_action_cost:
                            best_action = action
                            min_action_cost = current_cost

                    self.states[timestep][incidence][popularity].expected_value = min_action_cost
                    self.states[timestep][incidence][popularity].best_action = best_action


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
                    #current_cost += action.p * self.states[timestep+1][succ[0]][succ[1]]
                    current_cost += action.p * (incidence+self.states[timestep-1][succ[0]][succ[1]].expected_value)
                
                if min_action_cost == None or current_cost < min_action_cost:
                    min_action_cost = current_cost
                    best_action = action

        return min_action_cost, best_action
    
    def calc_successors(self,start)-> None:
        
        self.succ_states.append([self.states[self.steps-1][start[0]][start[1]]])

        for timestep in range(self.steps):
            if timestep != 0:
                self.succ_states.append([])

                for state in self.succ_states[timestep-1] :
                    for cost in state.best_action.costs : 

                        if state.incidence + cost[0] > 500:
                            succ_incidence = 500
                        elif state.incidence + cost[0] < 0:
                            succ_incidence = 0
                        else:
                            succ_incidence = state.incidence + cost[0] 

                        if state.popularity + cost[1] > 100:
                            succ_popularity = 100
                        elif state.popularity + cost[1] < 0:
                            succ_popularity = 0
                        else: 
                            succ_popularity = state.popularity + cost[1]

                        self.succ_states[timestep].append(self.states[self.steps-timestep-1][succ_incidence][succ_popularity])

    def calc_reelection_prop(self) -> None: 
        reelected_states = 0
        total_states = 0
        for state in self.succ_states[-1]:
            total_states += 1 
            if state.popularity >= 50: 
                reelected_states += 1
        
        self.reelection_prop = reelected_states / total_states
        print("Reelected States: " + str(reelected_states))
        print("Total States: " + str(total_states))
        print("Quotient: " + str(self.reelection_prop))
    
    def plot_bestaction(self) -> None:
        
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


                    ax.fill(x, y,self.states[self.steps-timestep-1][incidence][popularity].best_action.color,alpha=0.5)

               
            for visited in self.succ_states[timestep]:
                x = [visited.incidence,visited.incidence +1]
                y = [visited.popularity,visited.popularity +1]
                ax.plot(x,y,"black")
                x = [visited.incidence,visited.incidence +1]
                y = [visited.popularity +1,visited.popularity]
                ax.plot(x,y,"black")
        


            first_patch = mpatches.Patch(color=self.actions[0].color, label=self.actions[0].name)
            second_patch = mpatches.Patch(color=self.actions[1].color, label=self.actions[1].name)
            third_path = mpatches.Patch(color=self.actions[2].color, label=self.actions[2].name)
            forth_patch = mpatches.Patch(color=self.actions[3].color, label=self.actions[3].name)
            plt.legend(handles=[first_patch, second_patch, third_path, forth_patch],loc="upper right")

            fig.savefig(".\\Results\\State_"+str(self.succ_states[0][0].incidence)+"_"+str(self.succ_states[0][0].popularity)+"_Figure_"+str(timestep)+"_Best_Action.png")
        
        
        
    
    def plot_vpistar(self) -> None:
        self.calc_reelection_prop()
       

        print("Plotting Step: " + str(self.steps-1))
        fig, ax = plt.subplots()
        ax.set_xlabel('Incidence')
        ax.set_ylabel('Popularity')
        ax.set_title('Terminal Cost at T: '+ str(self.steps-1) + ' ; Reelection Prob: ' + str(self.reelection_prop))
        ax.set_xlim(0,501)
        ax.set_ylim(0,101)
        
        color_gradient = self.get_color_gradient("#0cad24","#fc0303",1301)
        for incidence in range(501): 
            for popularity in range(101):
                x = [incidence, incidence, incidence+1, incidence+1]
                y = [popularity, popularity + 1, popularity + 1,popularity]

                
                #ax.fill(x, y,color_gradient[round(self.states[0][incidence][popularity].expected_value)],alpha=0.5)
                #ax.fill(x, y,color_gradient[round(self.states[0][incidence][popularity].expected_value)])
                #Changed
                expected_value = round(self.states[0][incidence][popularity].expected_value)
                if expected_value > 1300:
                    expected_value = 1300
                ax.fill(x, y,color_gradient[expected_value])


        for visited in self.succ_states[self.steps-1]:
            x = [visited.incidence,visited.incidence +1]
            y = [visited.popularity,visited.popularity +1]
            ax.plot(x,y,"black")
            x = [visited.incidence,visited.incidence +1]
            y = [visited.popularity +1,visited.popularity]
            ax.plot(x,y,"black")

        first_patch = mpatches.Patch(color="#0cad24", label="Terminal Cost of 0")
        second_patch = mpatches.Patch(color="#fc0303", label="Terminal Cost of 1300")

        plt.legend(handles=[first_patch, second_patch],loc="upper right")
        
        #cm = mcolors.LinearSegmentedColormap.from_list(name="TerminalCostMap",colors=color_gradient,N=1300)  
        #fig.colorbar(cm,ax=ax)
        fig.savefig(".\\Results\\State_"+str(self.succ_states[0][0].incidence)+"_"+str(self.succ_states[0][0].popularity)+"_Figure_"+str(self.steps-1)+"_Expected_Cost.png")
        
        for timestep in range(self.steps-1):
            #color_gradient = self.get_color_gradient("#0cad24","#fc0303",801+(self.steps-timestep)*500)
            print("Plotting Step: " + str(timestep))
            fig, ax = plt.subplots()
            ax.set_xlabel('Incidence')
            ax.set_ylabel('Popularity')
            ax.set_title('Expected Cost for PI* at T: '+ str(timestep))
            ax.set_xlim(0,501)
            ax.set_ylim(0,101)
            for incidence in range(501): 
                for popularity in range(101):
                    x = [incidence, incidence, incidence+1, incidence+1]
                    y = [popularity, popularity + 1, popularity + 1,popularity]
                    #ax.fill(x, y,color_gradient[round(self.states[self.steps-timestep-1][incidence][popularity].expected_value)],alpha=0.5)
                    #ax.fill(x, y,color_gradient[round(self.states[self.steps-timestep-1][incidence][popularity].expected_value)])
                    expected_value = round(self.states[self.steps-timestep-1][incidence][popularity].expected_value)
                    if expected_value > 1300:
                        expected_value = 1300
                    ax.fill(x, y,color_gradient[expected_value])

            for visited in self.succ_states[timestep]:
                x = [visited.incidence,visited.incidence +1]
                y = [visited.popularity,visited.popularity +1]
                ax.plot(x,y,"black")
                x = [visited.incidence,visited.incidence +1]
                y = [visited.popularity +1,visited.popularity]
                ax.plot(x,y,"black")
            
            first_patch = mpatches.Patch(color="#0cad24", label="Expected Cost of 0")
            second_patch = mpatches.Patch(color="#fc0303", label="Expected Cost of 1300")

            plt.legend(handles=[first_patch, second_patch],loc="upper right")

            fig.savefig(".\\Results\\State_"+str(self.succ_states[0][0].incidence)+"_"+str(self.succ_states[0][0].popularity)+"_Figure_"+str(timestep)+"_Expected_Cost.png")
        

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
