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
    print("Load data")

m = g.Model()

# chess_board = m.addVars(chess_size, chess_size, vtype=g.GRB.BINARY)

# for i in range(2, chess_size - 2):
#     for j in range(2, chess_size - 2):
#         m.addConstr(
#             chess_board[i, j]  # main
#             + chess_board[i - 2, j - 1] + chess_board[i - 1, j - 2]
#             + chess_board[i - 2, j + 1] + chess_board[i + 1, j - 2]
#             + chess_board[i + 2, j - 1] + chess_board[i - 1, j + 2]
#             + chess_board[i + 2, j + 1] + chess_board[i + 1, j + 2]
#             <= 1)


# m.setObjective(chess_board.sum(), g.GRB.MAXIMIZE)

m.optimize()


king_count = 0
ret = ""

# for i in range(2, chess_size - 2):
#     for j in range(2, chess_size - 2):
#         if round(chess_board[i, j].x) == 1:
#             king_count += 1
#             ret += str(num2str[i-2]) + str(j-2+1) + "\n"

# ret = str(king_count)+"\n" + ret
# with open(path_output, "w+") as f:
#     f.write(ret)
