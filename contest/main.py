#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np

if len(sys.argv) < 3:
    print("ERROR: The script needs arguments with input and output path.")
    exit(1)

path_input = sys.argv[1]
path_output = sys.argv[2]

nodes_count = 0

with open(path_input, "r") as f:

    edge_count = int(f.readline())
    graph = []
    for i in range(edge_count):
        edge = f.readline().split()
        graph.append({
            "in": int(edge[0]) - 1,
            "out": int(edge[1]) - 1,
            "cost": int(edge[2])
        })

        if graph[i]["in"] > nodes_count:
            nodes_count = round(graph[i]["in"])
        if graph[i]["out"] > nodes_count:
            nodes_count = round(graph[i]["out"])

# print(graph, nodes_count)

nodes_count += 1

m = g.Model()

e = m.addVars(edge_count, vtype=g.GRB.BINARY, name="Existence")
t = m.addVars(nodes_count, vtype=g.GRB.INTEGER,
              lb=0, ub=nodes_count, name="Time")

for i in range(edge_count):
    print(graph[i]["out"])
    m.addConstr(e[i] * t[graph[i]["out"]] + 1 <= t[graph[i]["in"]])

m.setObjective(g.quicksum(graph[i]["cost"]*e[i]
               for i in range(edge_count)), g.GRB.MAXIMIZE)

m.optimize()

ret = ""
objective = 0
for i in range(edge_count):
    if round(e[i].X) == 0:
        ret += str(graph[i]["in"] + 1) + " " + str(graph[i]["out"] + 1) + "\n"
        objective += graph[i]["cost"]
with open(path_output, "w+") as f:
    f.write(str(objective) + "\n" + ret)
