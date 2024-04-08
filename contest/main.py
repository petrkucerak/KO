#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np

if len(sys.argv) < 3:
    print("ERROR: The script needs arguments with input and output path.")
    exit(1)

path_input = sys.argv[1]
path_output = sys.argv[2]

def contains_cycle(node):
    # for i in range(edge_count):
    #     if graph[i][2] >5: return True
    return False

nodes_count = 0

# Existuje li hrana, musi byt cas jejiho zavreni nizsi nez hrany zavrene po ni

with open(path_input, "r") as f:

    edge_count = int(f.readline())
    graph = np.zeros((edge_count, 3))
    for i in range(edge_count):
        edge = f.readline().split()
        graph[i] = [int(edge[0]), int(edge[1]), int(edge[2])]
        if graph[i][0] > nodes_count: nodes_count = round(graph[i][0])
        if graph[i][1] > nodes_count: nodes_count = round(graph[i][1])

m = g.Model()

e = m.addVars(edge_count, vtype=g.GRB.BINARY)

m.setObjective(g.quicksum(e[i]*graph[i][2] for i in range(edge_count)), g.GRB.MAXIMIZE)

m.optimize()

ret = ""
for i in range(edge_count):
    if round(e[i].X) == 0:
        ret += str(round(graph[i][0])) + " " + str(round(graph[i][1])) + "\n"
print(ret)
with open(path_output, "w+") as f:
    f.write(ret)