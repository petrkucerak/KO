#!/usr/bin/env python3
import gurobipy as g
import sys
import numpy as np


def my_callback(model, where):
    # Callback is called when some event occur. The type of event is
    # distinguished using argument ’’ where ’ ’.
    # In this case, we want to perform something when an integer
    # solution is found, which corresponds to ’’ GRB.Callback.MIPSOL ’ ’.
    if where == g.GRB.Callback.MIPSOL:
        visited = np.zeros(x_len)
        cycles = []
        for i in range(x_len):
            if visited[i] == 1:
                continue
            else:
                cycle = []
                current_node = i
                while visited[current_node] != 1:
                    visited[current_node] = 1
                    cycle.append(current_node)
                    for j in range(x_len):
                        if round(model.cbGetSolution(x[current_node][j])) == 1:
                            current_node = j
                            break
                cycles.append(cycle)
        if len(cycles) > 1:
            max_len = np.inf
            cycle_to_block = None
            for c in cycles:
                if len(c) < max_len:
                    cycle_to_block = c
                    max_len = len(c)
            model.cbLazy(g.quicksum(
                x[i][j] for i in cycle_to_block for j in cycle_to_block if i != j) <= len(cycle_to_block)-1)


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

    data = np.zeros((n, 2, h * 3))
    for i in range(n):
        line = f.readline().split()
        for row in range(h):
            # get first col
            data[i, 0, row*3 + 0] = int(line[row*w*3 + 0 + 0])
            data[i, 0, row*3 + 1] = int(line[row*w*3 + 0 + 1])
            data[i, 0, row*3 + 2] = int(line[row*w*3 + 0 + 2])
            # get last col
            data[i, 1, row*3 + 0] = int(line[row*w*3 + w*3-1 - 2])
            data[i, 1, row*3 + 1] = int(line[row*w*3 + w*3-1 - 1])
            data[i, 1, row*3 + 2] = int(line[row*w*3 + w*3-1 - 0])
    # print(data)

dist_matrix = np.zeros((n + 1, n + 1))
np.set_printoptions(threshold=sys.maxsize)
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = np.abs(
                np.sum(np.abs(data[i, 0] - data[j, 1])))
dist_matrix = np.transpose(dist_matrix)
# print(data)
# print(dist_matrix)

m = g.Model()
m.Params.LazyConstraints = 1

x_len = len(dist_matrix)
x = ([[0 for i in range(x_len)] for j in range(x_len)])
for i in range(x_len):
    for j in range(x_len):
        if i != j:
            x[i][j] = m.addVar(vtype=g.GRB.BINARY)
        else:
            # for diagonal direction
            x[i][j] = m.addVar(vtype=g.GRB.BINARY, lb=0, ub=0)

for i in range(x_len):
    m.addConstr(g.quicksum(x[j][i] for j in range(x_len)) == 1)
    m.addConstr(g.quicksum(x[i][j] for j in range(x_len)) == 1)

m.setObjective(g.quicksum(x[i][j]*dist_matrix[i][j]
               for j in range(x_len) for i in range(x_len)), g.GRB.MINIMIZE)
m.optimize(my_callback)

# for i in x:
#     print([int(np.abs(i[j].x)) for j in range(x_len)])

ret = ""
line = x_len - 1  # start from dummy stripe
visited_nodes_num = 0
while visited_nodes_num < x_len-1:
    for j in range(x_len):
        if round(x[line][j].x) == 1:
            visited_nodes_num += 1
            line = j
            ret += str(j+1) + " "
            break
with open(path_output, "w+") as f:
    f.write(ret)
