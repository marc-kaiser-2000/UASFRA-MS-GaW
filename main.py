from state import * 
from action import *
from backward_dp import *

a1_cost = [
    [50,5],
    [50,1],
    [30,1],
    [10,3]
]
a2_cost = [
    [30,1],
    [30,-1],
    [10,-1],
    [-10,-3]
]
a3_cost = [
    [30,1],
    [10,-1],
    [-10,3],
    [-30,5]
]
a4_cost = [
    [-10,-3],
    [-30,-3],
    [-30,-5],
    [-50,-5]
]


actions = [
    Action(1,"Alles öffnen",a1_cost),
    Action(2,"Lockdown Light",a2_cost),
    Action(3,"Lockdown",a3_cost),
    Action(4,"Lockdown Ultra",a4_cost)
]

alg = Backwards_DP(actions)

