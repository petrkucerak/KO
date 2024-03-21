import gurobipy as g
import sys

# Get input and output args
if len(sys.argv) < 3:
    raise ValueError("Please execute the program with the specified arguments: the first argument being the input file path and the second argument being the desired output destination.")

path_input = sys.argv[1]
path_output = sys.argv[2]

# Load variables
with open(path_input, "r") as f:
    d = [int(num) for num in f.readline().split()]
    e = [int(num) for num in f.readline().split()]
    D = int(f.readline())

print("INPUT")
print(d)
print(e)
print(D)

# Optimalization
m = g.Model()

xs = m.addVars(len(d), lb=0, vtype=g.GRB.INTEGER,
               name=[f"x{i}" for i in range(len(d))])

for i in range(len(d)):
    m.addConstr(g.quicksum(xs[j % len(d)]
                for j in range(i - 7, i + 1)) >= d[i])

m.setObjective(xs.sum(), sense=g.GRB.MINIMIZE)

m.optimize()

# Print output
optimal_vals = [int(xs[x].x) for x in xs]
objective = int(m.getObjective().getValue())

print("OUTPUT")
print(objective)
print(optimal_vals)
with open(path_output, "w+") as f:
    f.write(str(objective) + "\n")
    for num in optimal_vals:
        f.write(str(num) + " ")
