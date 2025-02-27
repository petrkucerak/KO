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


print("L", locker_count, "C", customer_count)
print("Customer order count ", order_count)
print("Locker height", locker_height)

for order in orders:
    print(order)


# Solve by Gurobi model

# m = g.Model()


# Print results
