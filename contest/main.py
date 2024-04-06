#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np

if len(sys.argv) < 3:
    print("ERROR: The script needs arguments with input and output path.")
    exit(1)

path_input = sys.argv[1]
path_output = sys.argv[2]

with open(path_input, "r") as f:

    edge_count = int(f.readline())
    graph = np.zeros((edge_count, 3))
    for i in range(edge_count):
        edge = f.readline().split()
        graph[i] = [int(edge[0]), int(edge[1]), int(edge[2])]

m = g.Model()

c = m.addVars(edge_count, vtype=g.GRB.BINARY)

m.setObjective(g.quicksum(c[i]*graph[i][2] for i in range(edge_count)), g.GRB.MINIMIZE)

m.optimize()

ret = ""
for i in range(edge_count):
    if round(c[i].X) == 0:
        ret += str(round(graph[i][0])) + " " + str(round(graph[i][1])) + "\n"
print(ret)