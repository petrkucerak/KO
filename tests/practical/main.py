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
    width = int(metadata[0])            # N
    height = int(metadata[1])           # M
    max_dams = int(metadata[2])         # D
    max_single_dams = int(metadata[3])  # S
    rock_count = int(metadata[4])       # R

    # load river strength
    river_strength = f.readline().split()
    for i in range(width):
        river_strength[i] = int(river_strength[i])

    # load rock positions
    rock_positions = []
    for i in range(rock_count):
        line = f.readline().split()
        rock_positions.append({"x": int(line[0]), "y": int(line[1])})


m = g.Model()
# create the river model
river = np.zeros((height, width))
for y in range(height):
    for x in range(width):
        river[y, x] = river_strength[x]
for i in range(rock_count):
    river[rock_positions[i]["y"], rock_positions[i]["x"]] = 0

print(river)

power = m.addVars(height + 3, width, vtype=g.GRB.BINARY,
                  name="Existence of power turbine")

# limit count of power plats in all river
m.addConstr(power.sum() <= max_dams)

# limit count of power station for each row in the river
for y in range(height + 3):
    m.addConstr(g.quicksum(power[y, x]
                for x in range(width)) <= max_single_dams)

# set virtual power to zero
m.addConstr(power.sum(0, "*") == 0)
m.addConstr(power.sum(1, "*") == 0)
m.addConstr(power.sum(2, "*") == 0)


m.setObjective(g.quicksum(power[y+3, x] * river[y, x]
                          - power[y-1+3, x] * 3  # direction 1
                          - power[y-2+3, x] * 2  # direction 2
                          - power[y-3+3, x] * 1  # direction 3
                          for x in range(width) for y in range(height)),
               g.GRB.MAXIMIZE)

m.optimize()

power_output = 0
ret = ""

for y in range(height):
    for x in range(width):
        if round(power[y+3, x].x) == 1:
            ret += str(x) + " " + str(y) + "\n"
            power_output += river[y, x]
ret = str(round(power_output)) + "\n" + ret

print(ret)

with open(path_output, "w+") as f:
    f.write(ret)
