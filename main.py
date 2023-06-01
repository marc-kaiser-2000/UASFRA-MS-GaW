import matplotlib.pyplot as plt
from action import *
from backward_dp import *

a1_cost = [
    [50, 5],
    [50, 1],
    [30, 1],
    [10, 3]
]
a2_cost = [
    [30, 1],
    [30, -1],
    [10, -1],
    [-10, -3]
]
a3_cost = [
    [30, 1],
    [10, -1],
    [-10, 3],
    [-30, 5]
]
a4_cost = [
    [-10, -3],
    [-30, -3],
    [-30, -5],
    [-50, -5]
]

actions = [
    Action(1, "Alles öffnen", a1_cost),
    Action(2, "Lockdown Light", a2_cost),
    Action(3, "Lockdown", a3_cost),
    Action(4, "Lockdown Ultra", a4_cost)
]

alg = Backwards_DP(actions)

# V* Liste mit den erwarteten Kosten
# Pi* Liste, welche die besten Aktionen enthält
V_stern, pi_stern = alg.select_best_strategie([100, 50])

print("Optimale erwartete Kosten V*: ")
for v in V_stern:
    print(str(v) + str(", "))

print("Optimale Strategie: ")
for best_action in pi_stern:
    best_action.print()

print("Finish Run 1")

V_stern, pi_stern = alg.select_best_strategie([100, 60])

print("Optimale erwartete Kosten V*: ")
for v in V_stern:
    print(str(v) + str(", "))

print("Optimale Strategie: ")
for best_action in pi_stern:
    best_action.print()

print("Finish Run 2")

fig, ax = plt.subplots()
x = [0, 0, 1, 1]
y = [0, 1, 1, 0]

ax.fill(x, y, "b")

x = [1, 1, 2, 2]
y = [0, 1, 1, 0]

ax.fill(x, y, "g")

x = [0, 0, 1, 1]
y = [1, 2, 2, 1]

ax.fill(x, y, "y")

x = [1, 1, 2, 2]
y = [1, 2, 2, 1]

ax.fill(x, y, "r")

plt.show()
