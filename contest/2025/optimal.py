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
    for N in range(customer_count):
        line = list(map(int, f.readline().split()))
        price = []
        height = []
        for i in range(1, len(line)):
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


# Test sum
print(
    "TEST SUM WITHOUT BONUS",
    sum(sum(orders[i]["price"]) for i in range(customer_count))
)

print(
    "TEST SUM WITHT BONUS",
    sum(sum(orders[i]["price"]) for i in range(customer_count)) +
    sum(orders[i]["bonus"] for i in range(customer_count))
)


# Solve by Gurobi model

m = g.Model("TurkeyBox")

# CREATE VARIABLES
# kam je zpozi umisteno
r = {}  # r[i, k, l]
# i ... customer
# k ... order
# l ... locker
for i in range(customer_count):
    for k in range(order_count[i]):
        for l in range(locker_count):
            r[i, k, l] = m.addVar(
                vtype=g.GRB.BINARY,
                name=f"raster_{i}_{k}_{l}"
            )
b = m.addVars(customer_count, vtype=g.GRB.BINARY, name="Bonus is earned")


# CREATE CONSTRAINS
# 1) Single customer per locker
for l in range(locker_count):
    for i in range(customer_count):  # customer i
        for j in range(i+1, customer_count):  # customer j
            m.addConstr(
                g.quicksum(r[i, k, l] for k in range(order_count[i])) *
                g.quicksum(r[j, k, l] for k in range(order_count[j])) == 0,
                name=f"singe_customer_{i}_{j}_{l}"
            )


# 2) Locker is not overfilled
for l in range(locker_count):
    m.addConstr(
        g.quicksum(
            orders[i]["height"][k] * r[i, k, l]
            for i in range(customer_count)
            for k in range(order_count[i])
        ) <= locker_height[l],
        name=f"capacity_{l}"
    )


# 3) Get bonus from customer
for i in range(customer_count):
    m.addConstr(
        g.quicksum(
            r[i, k, l]
            for k in range(order_count[i])
            for l in range(locker_count)
        ) == order_count[i] * b[i],
        name=f"bonus_{i}"
    )


# CREATE OBJECTIVE
# maximize the profit
m.setObjective(
    # sum of placed goods
    g.quicksum(
        r[i, k, l] * orders[i]["price"][k]
        for i in range(customer_count)
        for k in range(order_count[i])
        for l in range(locker_count)
    ) +
    # bonus for complete whole orders
    g.quicksum(
        b[i] * orders[i]["bonus"]
        for i in range(customer_count)
    ),
    g.GRB.MAXIMIZE

)


# Solve the model
m.optimize()

# Print results
with open(paths["output"], 'w') as f:
    if m.status == g.GRB.OPTIMAL:
        f.write(f"{int(m.objVal)}\n")
        for i in range(customer_count):
            for k in range(order_count[i]):
                assigned_locker = next(
                    (l+1 for l in range(locker_count) if r[i, k, l].x > 0.5), 0)
                f.write(f"{assigned_locker}\n")
    else:
        f.write("0\n")
