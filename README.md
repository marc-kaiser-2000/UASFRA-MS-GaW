# Backwards Dynamic Programming 

This programm implements the Backwards Dynamic Programming Algorithm on a synthetic task. \
Given a president / agent who has upcoming elections in $|t| = 8$ timesteps.
The state of the agent $s$ can be described through a tupel composed from popularity $(b \in [0,100])$ and incidence $(i \in [0,500])$. Hence $s$ can be defined as $s = (i,b)$.
\
\
The goal of the president is to be reelected in $8$ weeks while keeping the incidence as low as possible. Therefore he needs to have a popularity greater 50%. The president has at each point in time a total of $4$ possible acitons. These are:

 + $a_1$: No Lockdown
 + $a_2$: Lockdown light
 + $a_3$: Lockdown
 + $a_4$: Lockdown ultra

 Each of these actions has a non-deterministic effect on the state of the agent. 
 A single action can have four different effects with each a 25% chance. 
 The effects are shown in the following table.


|Actions|   |   |   |   |
|---|---|---|---|---|
|$a_1$|+50/+5|+50/+1|+30/+1|+10/+3|
|$a_2$|+30/+1|+30/-1|+10/-1|-10/-3|
|$a_3$|+30/+1|+10/-1|-10/-3|-30/-5|
|$a_4$|-10/-3|-30/-3|-30/-5|-50/-5|

Given the upper table and starting state $s_0=(100,50)$, the agent has to select the optimal solution at each point in time $t$. The direct cost of the agent are linear to the incidence $i$. He receives additional terminal costs of $800$, if his popularity is smaller than $50$.
The optimal action and expected costs were calculated with the Backwards Dynamic Programming Algorithm. Furthermore we provided the probability to be reelected under the optimal strategy $\pi^*$.\
\
The results can be found in the "Results" directory. In there two pictures for each point in time $t$ are generated. The pictures are named after the following convention:\
\
State_[Incidence $i$ of Start State]_[Popularity $b$ of Start State]_Figure\_[Timestamp $t$ at current state]\_[Best_Action/Expected Cost].png\
\
Be aware that $t$ increases, contrary to the literature.

# How to run
Install the required packages

    pip install -r requirements.txt

Run "main.py". Be aware that plotting the individual steps takes some time.


