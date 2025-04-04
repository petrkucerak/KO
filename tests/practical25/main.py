#!/usr/bin/env python3
import gurobipy as g
import sys
import numpy as np

# Get input and output args
if len(sys.argv) < 3:
    raise ValueError("Please execute the program with the specified arguments: the first argument being the input file path and the second argument being the desired output destination.")

path_input = sys.argv[1]
path_output = sys.argv[2]


with open(path_input, "r") as f:
    # load metadata
    metadata = f.readline().split()
    M = int(metadata[0])  # number of machines
    P = int(metadata[1])  # number of possible machine placements
    C = int(metadata[2])  # number of complementary pairs
    U = int(metadata[3])  # minimum popularity fro guys or ladies

    # load t - machine types
    machine_types = list(map(int, f.readline().split()))
    # load n - required number of machine types
    machine_types_require = list(map(int, f.readline().split()))
    # load s - size of machine
    machine_sizes = list(map(int, f.readline().split()))
    # load d - place dimensions
    place_dimension = list(map(int, f.readline().split()))
    # load l - popularity of machine m with ladies
    machine_popularity_l = list(map(int, f.readline().split()))
    # load g - popularity of machine m with guys
    machine_popularity_g = list(map(int, f.readline().split()))

    machine_types_0 = []
    for m in range(M):
        if machine_types[m] == 0:
            machine_types_0.append(m)

    machine_types_1 = []
    for m in range(M):
        if machine_types[m] == 1:
            machine_types_1.append(m)

    machine_types_2 = []
    for m in range(M):
        if machine_types[m] == 2:
            machine_types_2.append(m)

    # load complementary pairs
    pairs = []
    for i in range(C):
        pair = list(map(int, f.readline().split()))
        pairs.append(pair)

    # Testing print
    print("machine_types: ", machine_types)
    print("machine_types_require: ", machine_types_require)
    print("machine_sizes: ", machine_sizes)
    print("place_dimension: ", place_dimension)
    print("machine_popularity_l: ", machine_popularity_l)
    print("machine_popularity_g: ", machine_popularity_g)
    print("pairs: ", pairs)


mod = g.Model("Gym Placement")

# Create variables
board = mod.addVars(M, P, vtype=g.GRB.BINARY)


# Add constrains
# 1. each machine can be used once - means that sum of p should be max 1
for p in range(P):
    mod.addConstr(
        g.quicksum(
            board[m, p]
            for m in range(M)
        ) <= 1
    )

# 2. each place is occupied by at most one machine
for m in range(M):
    mod.addConstr(
        g.quicksum(
            board[m, p]
            for p in range(P)
        ) <= 1
    )

# 3. the gym should provide enough machines of each type
# (for each type t there must be at least n_t machines)
mod.addConstr(
    g.quicksum(
        board[machine_types_0[m], p]
        for m in range(len(machine_types_0))
        for p in range(P)
    ) >= machine_types_require[0]
)
mod.addConstr(
    g.quicksum(
        board[machine_types_1[m], p]
        for m in range(len(machine_types_1))
        for p in range(P)
    ) >= machine_types_require[1]
)
mod.addConstr(
    g.quicksum(
        board[machine_types_2[m], p]
        for m in range(len(machine_types_2))
        for p in range(P)
    ) >= machine_types_require[2]
)

# 4. position
for m in range(M):
    for p in range(P):
        mod.addConstr(
            board[m, p] * machine_sizes[m] <= place_dimension[p]
        )


# Set objective
mod.setObjective(
    g.quicksum(
        board[m, p] * machine_popularity_l[m] +     # ladies popularity
        board[m, p] * machine_popularity_g[m]       # guys popularity
        for p in range(P)
        for m in range(M)
    ),
    g.GRB.MAXIMIZE
)

mod.optimize()

if mod.Status == g.GRB.Status.INFEASIBLE:
    ret = "-1"
else:
    ret = f"{int(mod.objVal)}\n"
    for m in range(M):
        pos = -1
        for p in range(P):
            if board[m, p].x > 0.5:
                pos = p
        ret += f"{pos} "
with open(path_output, "w+") as f:
    f.write(ret)
