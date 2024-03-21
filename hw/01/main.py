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

week_duration = 168
day_duration = 24

x = m.addVars(week_duration, lb=0, vtype=g.GRB.INTEGER)
z = m.addVars(week_duration, lb=0, vtype=g.GRB.INTEGER)

for i in range(week_duration):
    if i < 120:
        q = d[i % 24]
    else:
        q = e[i % 24]

    m.addConstr(q - g.quicksum(x[j % week_duration]
                for j in range(i-7, i + 1)) <= z[i])
    m.addConstr(g.quicksum(x[j % week_duration]
                for j in range(i-7, i + 1)) - q <= z[i])
    m.addConstr(q - g.quicksum(x[j % week_duration]
                for j in range(i-7, i + 1)) <= D)


m.setObjective(g.quicksum(z), sense=g.GRB.MINIMIZE)

m.optimize()

# Print output
optimal_vals = [int(x[i].x) for i in x]
objective = int(m.getObjective().getValue())

print("OUTPUT")
print(objective)
print(optimal_vals)
with open(path_output, "w+") as f:
    f.write(str(objective) + "\n")
    for num in optimal_vals:
        f.write(str(num) + " ")
