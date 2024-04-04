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

    data = np.zeros((n,w,h,3))
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

print(np.sum(data[0,0]))
print(np.sum(data[0,w-1]))

dist_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            dist_matrix[i][j] = np.abs(np.sum(data[i,0]) - np.sum(data[j,w-1]))
print(dist_matrix)

# m = g.Model()
# m.Params.LazyConstraints = 1


# def my_callback(m, where):
#     # Callback is called when some event occur . The type of event is
#     # distinguished using argument ’’ where ’ ’.
#     # In this case , we want to perform something when an integer
#     # solution is found , which corresponds to ’’ GRB . Callback . MIPSOL ’ ’.
#     if where == g.GRB.Callback.MIPSOL:
#         # TODO : your code here ...
#         # Get the value of variable x [i , j ] from the solution .
#         # You may also pass a list of variables to the method .
#         value = m.cbGetSolution(x[i, j])
#         # Add lazy constraint to model .
#         m.cbLazy(...)


# m.optimize(my_callback)
