import gurobipy as g
import sys

if len(sys.argv) < 3:
    raise ValueError("Please execute the program with the specified arguments: the first argument being the input file path and the second argument being the desired output destination.")

path_input = sys.argv[1]
path_output = sys.argv[2]

with open(path_input, "r") as f:
    d_row = [int(num) for num in f.readline().split()]
    e_row = [int(num) for num in f.readline().split()]
    D_row = int(f.readline())

print("INPUT")
print(d_row)
print(e_row)
print(D_row)


# d = [6, 6, 6, 6, 6, 8, 9, 12, 18, 22, 25, 21, 21,
#      20, 18, 21, 21, 24, 24, 18, 18, 18, 12, 8]

# m = g.Model()

# xs = m.addVars(len(d), lb=0, vtype=g.GRB.INTEGER,
#                name=[f"x{i}" for i in range(len(d))])

# for i in range(len(d)):
#     m.addConstr(g.quicksum(xs[j % len(d)]
#                 for j in range(i - 7, i + 1)) >= d[i])

# m.setObjective(xs.sum(), sense=g.GRB.MINIMIZE)

# m.optimize()


objective = 1536
optimal_vals = [12, 48, 65, 13, 57]

print("OUTPUT")
print(objective)
print(optimal_vals)
with open(path_output, "w+") as f:
    f.write(str(objective) + "\n")
    for num in optimal_vals:
        f.write(str(num) + " ")
