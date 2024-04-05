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
    n, w, h = f.readline().split()
    n = int(n)
    w = int(w)
    h = int(h)

    data = np.zeros((n, w, h, 3))
    for i in range(n):
        line = f.readline().split()
        for col in range(w):
            for row in range(h):
                data[i, col, row] = [
                    int(line[col*h + row]),
                    int(line[col*h + row + 1]),
                    int(line[col*h + row + 2])
                ]
    # print(data)

dist_matrix = np.zeros((n + 1, n + 1))
np.set_printoptions(threshold=sys.maxsize)
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = np.abs(
                np.sum(np.abs(data[i, 0] - data[j, w-1])))
# print(dist_matrix)

m = g.Model()
m.Params.LazyConstraints = 1

len = len(dist_matrix)
x = ([[0 for i in range(len)] for j in range(len)])
for i in range(len):
    for j in range(len):
        if i != j:
            x[i][j] = m.addVar(vtype=g.GRB.BINARY)
        else:
            # for diagonal direction
            x[i][j] = m.addVar(vtype=g.GRB.BINARY, lb=0, ub=0)

for i in range(len):
    m.addConstr(g.quicksum(x[j][i] for j in range(len)) == 1)
    m.addConstr(g.quicksum(x[i][j] for j in range(len)) == 1)

m.setObjective(g.quicksum(x[i][j]*dist_matrix[i][j]
               for j in range(len) for i in range(len)), g.GRB.MINIMIZE)


def my_callback(m, where):
    # Callback is called when some event occur. The type of event is
    # distinguished using argument ’’ where ’ ’.
    # In this case, we want to perform something when an integer
    # solution is found, which corresponds to ’’ GRB.Callback.MIPSOL ’ ’.
    if where == g.GRB.Callback.MIPSOL:
        visited = np.zeros(n)
        cycles = []
        for i in range(n):
            if visited[i] == 1:
                continue
            else:
                cycle = []
                curr_node = i
                while visited[curr_node] != 1:
                    visited[curr_node] = 1
                    cycle.append(curr_node)
                    for j in range(n):
                        if m.cbGetSolution(x[curr_node][j]) == 1:
                            curr_node = j
                            break
                cycles.append(cycle)
        if len(cycles) > 1:
            max_len = np.inf
            cycle_to_block = None
            for c in cycles:
                if len(c) < max_len:
                    cycle_to_block = c
                    max_len = len(c)
            m.cbLazy(g.quicksum(
                x[i][j] for i in cycle_to_block for j in cycle_to_block if i != j) <= len(cycle_to_block)-1)


m.optimize(my_callback)

for i in x:
    print([int(np.abs(i[j].x)) for j in range(n)])

ret = ""
with open(path_output, "w+") as f:
    f.write(ret)