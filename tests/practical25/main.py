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
    M = int(metadata[0]) # number of machines
    P = int(metadata[1]) # number of possible machine placements
    C = int(metadata[2]) # number of complementary pairs
    U = int(metadata[3]) # minimum popularity fro guys or ladies
    
    # load t - machine types
    machine_types = list(map(int, f.readline().split()))
    # load n - required number of machine types
    machine_types_require = list(map(int, f.readline().split()))
    # load s - size of machine
    machine_sizes = list(map(int, f.readline().split()))
    # load d - place dimensions
    place_dimension = list(map(int, f.readline().split()))
    # load l - popularity of machine m with ladies
    machine_popularity_l = list(map(int, f.readline().split()))
    # load g - popularity of machine m with guys
    machine_popularity_g = list(map(int, f.readline().split()))
    
    # load complementary pairs
    pairs = []
    for i in range(C):
        pair = list(map(int, f.readline().split()))
        pairs.append(pair)
        
    print(pairs)
        




# m = g.Model()
# # create the river model

# m.optimize()

ret = ""
with open(path_output, "w+") as f:
    f.write(ret)
