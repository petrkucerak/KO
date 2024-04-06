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

print(graph)
