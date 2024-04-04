#!/usr/bin/env python3
import gurobipy as g
import sys
import numpy as np

# Get input and output args
if len(sys.argv) < 3:
    raise ValueError("Please execute the program with the specified arguments: the first argument being the input file path and the second argument being the desired output destination.")

path_input = sys.argv[1]
path_output = sys.argv[2]


def calculate_distance(left, right):
    return np.sum(np.absolute(left - right))


def my_callback(model, where):
    # Callback is called when some event occur . The type of event is
    # distinguished using argument ’’ where ’ ’.
    # In this case , we want to perform something when an integer
    # solution is found , which corresponds to ’’ GRB . Callback . MIPSOL ’ ’.
    if where == g.GRB.Callback.MIPSOL:
        visited = np.zeros(n)
        cycles = []
        for i in range(n):
            if visited[i] == 1:
                continue
            else:
                cycle = []
                current_node = i
                while visited[current_node] != 1:
                    visited[current_node] = 1
                    cycle.append(current_node)
                    for j in range(n):
                        if model.cbGetSolution(x[current_node][j]) == 1:
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


with open(path_input, "r") as f:
    n, w, h = f.readline().split()
    n = int(n)
    w = int(w)
    h = int(h)

    data = []
    for i in range(n):
        line = f.readline().split()
        matrix = np.zeros((h*3, 2))
        for k in range(h):
            for j in range(w):
                if 0 == w-1:
                    matrix[k * 3][0] = int(line[k * w * 3 + j * 3])
                    matrix[k * 3 + 1][0] = int(line[k * w * 3 + j * 3 + 1])
                    matrix[k * 3 + 2][0] = int(line[k * w * 3 + j * 3 + 2])
                    matrix[k * 3][1] = matrix[k * 3][0]
                    matrix[k * 3 + 1][1] = matrix[k * 3 + 1][0]
                    matrix[k * 3 + 2][1] = matrix[k * 3 + 2][0]
                elif j == 0 or j == w-1:
                    if j == w-1:
                        y = 1
                    else:
                        y = 0
                    matrix[k*3][y] = int(line[k*w*3+j*3])
                    matrix[k*3+1][y] = int(line[k*w*3+j*3 + 1])
                    matrix[k*3+2][y] = int(line[k*w*3+j*3 + 2])
                else:
                    continue
        data.append(np.transpose(matrix))
dist_matrix = np.zeros((n+1, n+1))
np.set_printoptions(threshold=sys.maxsize)
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = calculate_distance(
                data[i][1], data[j][0])

m = g.Model()
m.Params.LazyConstraints = 1

n = len(dist_matrix)
x = ([[0 for i in range(n)] for j in range(n)])
for i in range(n):
    for j in range(n):
        if i != j:
            x[i][j] = m.addVar(vtype=g.GRB.BINARY)
        else:
            x[i][j] = m.addVar(vtype=g.GRB.BINARY, lb=0, ub=0)

for i in range(n):
    m.addConstr(g.quicksum(x[j][i] for j in range(n)) == 1)
    m.addConstr(g.quicksum(x[i][j] for j in range(n)) == 1)

optimal = 0
for i in range(n):
    for j in range(n):
        optimal += x[i][j] * dist_matrix[i][j]
m.setObjective(optimal, g.GRB.MINIMIZE)
m.optimize(my_callback)

visited_nodes_num = 0

line = n-1
ret = ""
while visited_nodes_num < n-1:
    for j in range(n):
        if x[line][j].x == 1:
            visited_nodes_num += 1
            line = j
            ret += str(j+1) + " "
            break
with open(path_output, "w+") as f:
    f.write(ret)
