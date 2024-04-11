#!/usr/bin/env python3
import gurobipy as g
import sys
import numpy as np

num2str = ["a", "b", "c", "d", "e", "f", "g", "h"]

# Get input and output args
if len(sys.argv) < 3:
    raise ValueError("Please execute the program with the specified arguments: the first argument being the input file path and the second argument being the desired output destination.")

path_input = sys.argv[1]
path_output = sys.argv[2]

data = []

with open(path_input, "r") as f:
    rooks_count = int(f.readline())

    for i in range(rooks_count):
        line = f.readline()
        data.append({"x": line[0], "y": line[1]})
print(data)

m = g.Model()

chess_size = 8

chess_board = m.addVars(chess_size, chess_size, vtype=g.GRB.BINARY)

m.setObjective(g.quicksum(chess_board[i, j]
                          for j in range(chess_size) for i in range(chess_size)),
               g.GRB.MAXIMIZE)

m.optimize()

king_count = 0

ret = ""

for i in range(chess_size):
    for j in range(chess_size):
        if round(chess_board[i, j].X) == 1:
            king_count += 1
            ret += str(num2str[i]) + str(j) + "\n"

ret = str(king_count)+"\n" + ret
with open(path_output, "w+") as f:
    f.write(ret)
