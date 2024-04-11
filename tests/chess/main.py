#!/usr/bin/env python3
import gurobipy as g
import sys
import numpy as np

num2str = ["a", "b", "c", "d", "e", "f", "g", "h"]


def print_chess_board(chess_board):
    for i in range(2, chess_size-2):
        for j in range(2, chess_size-2):
            print(str(round(chess_board[i, j].X)), end=' ')
        print()


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

# add virtual margins
chess_size = 8 + 2 + 2

chess_board = m.addVars(chess_size, chess_size, vtype=g.GRB.BINARY)

for i in range(2, chess_size - 2):
    for j in range(2, chess_size - 2):
        m.addConstr(
            chess_board[i, j]  # main
            + chess_board[i - 2, j - 1] + chess_board[i - 1, j - 2]
            + chess_board[i - 2, j + 1] + chess_board[i + 1, j - 2]
            + chess_board[i + 2, j - 1] + chess_board[i - 1, j + 2]
            + chess_board[i + 2, j + 1] + chess_board[i + 1, j + 2]
            <= 1)

# set 0 to imagine borders
m.addConstr(chess_board.sum(0, "*") == 0)
m.addConstr(chess_board.sum(1, "*") == 0)
m.addConstr(chess_board.sum("*", 0) == 0)
m.addConstr(chess_board.sum("*", 1) == 0)
m.addConstr(chess_board.sum(chess_size - 1, "*") == 0)
m.addConstr(chess_board.sum(chess_size - 2, "*") == 0)
m.addConstr(chess_board.sum("*", chess_size - 1) == 0)
m.addConstr(chess_board.sum("*", chess_size - 2) == 0)


m.setObjective(chess_board.sum(), g.GRB.MAXIMIZE)

m.optimize()

print_chess_board(chess_board=chess_board)

king_count = 0

ret = ""

for i in range(2, chess_size - 2):
    for j in range(2, chess_size - 2):
        if round(chess_board[i, j].x) == 1:
            king_count += 1
            ret += str(num2str[i-2]) + str(j-2+1) + "\n"

ret = str(king_count)+"\n" + ret
with open(path_output, "w+") as f:
    f.write(ret)
