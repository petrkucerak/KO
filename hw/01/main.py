import gurobipy as g

d = [6, 6, 6, 6, 6, 8, 9, 12, 18, 22, 25, 21, 21,
     20, 18, 21, 21, 24, 24, 18, 18, 18, 12, 8]

m = g.Model()

xs = m.addVars(len(d), lb=0, vtype=g.GRB.INTEGER,
               name=[f"x{i}" for i in range(len(d))])

for i in range(len(d)):
    m.addConstr(g.quicksum(xs[j % len(d)]
                for j in range(i - 7, i + 1)) >= d[i])

m.setObjective(xs.sum(), sense=g.GRB.MINIMIZE)

m.optimize()
