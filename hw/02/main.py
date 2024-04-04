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

    data = []
    for i in range(n):
        line = f.readline().split()

