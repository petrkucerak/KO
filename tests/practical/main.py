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
    # load metadata
    metadata = f.readline().split()
    width = int(metadata[0])            # N
    height = int(metadata[1])           # M
    max_dams = int(metadata[2])         # D
    max_single_dams = int(metadata[3])  # S
    rock_count = int(metadata[4])       # R

    # load river strength
    river_strength = f.readline().split()
    for i in range(width):
        river_strength[i] = int(river_strength[i])

    # load rock positions
    rock_positions = []
    for i in range(rock_count):
        line = f.readline().split()
        rock_positions.append({"x": int(line[0]), "y": int(line[1])})
    


# m = g.Model()


# king_count = 0
# ret = ""
