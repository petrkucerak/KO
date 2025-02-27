import gurobipy as g
import sys

# Parse arguments
if len(sys.argv) < 3:
    print("ERROR: You do not specify arguments correctly!")
    print("Use `optimal.py <PATH_INPUT_FILE> <PATH_OUTPUT_FILE>`\n")
    exit(1)

paths = {
    "input": sys.argv[1],
    "output": sys.argv[2]
}

# Load data
with open(paths["input"], "r") as f:
    locker_count, customer_count = map(int, f.readline().split())  # M, N
    order_count = list(map(int, f.readline().split()))  # n
    locker_height = list(map(int, f.readline().split()))
    orders = []
    for N in range(len(order_count)):
        line = list(map(int, f.readline().split()))
        price = []
        height = []
        for i in range(0, order_count[N]):
            if i % 2 == 1:
                price.append(line[i])
            else:
                height.append(line[i])
        order = {
            "bonus": line[0],
            "price": price,
            "height": height
        }
        orders.append(order)


# Solve by Gurobi model

m = g.Model()

# Create variable
good = {}
# good[i,k,n], where i = customer, k = item, n = locker
for i in range(customer_count):
    for k in range(order_count[i]):
        for n in range(locker_count):
            good[i, k, n] = m.addVar(
                vtype=g.GRB.BINARY, name=f"good_{i}_{k}_n")
bonus = m.addVars(locker_count, vtype=g.GRB.BINARY, name="bonus_price")


# Set objective: goal is maximize profit
m.setObjective(
    g.quicksum(
        good[i, k, n] * orders[i]["price"][k]
        for i in range(customer_count)
        for k in range(order_count[i])
        for n in range(locker_count)
    )
    +
    g.quicksum(
        bonus[i]*orders[i]["bonus"] for i in range(customer_count)
    ),
    g.GRB.MAXIMIZE
)

m.optimize()

# Print results
ret = 0
for order in orders:
    ret += sum(order["price"])

print(ret)
