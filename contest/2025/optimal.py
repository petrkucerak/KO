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
    locker_count, customer_count = map(int, f.readline().split())
    order_count = list(map(int, f.readline().split()))
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

good_price = []
for N in range(customer_count):
    good_price.append(m.addVars(order_count[N],vtype=g.GRB.BINARY))
    
bonus_price = m.addVars(customer_count, vtype=g.GRB.BINARY, name="bonus_price")


m.setObjective(
    g.quicksum(
        g.quicksum(
            orders[N]["price"][locker]*good_price[N][locker]
            for locker in range(len(orders[N]["price"]))
        )
        for N in range(customer_count)),
    sense=g.GRB.MAXIMIZE)

m.optimize()

# Print results
ret = 0
for order in orders:
    ret += sum(order["price"])
    
print(ret)
    
