import gurobipy as g
import sys


def get_lock_position(i, k, n):
    """The function is the MACRO for unify access to the `g_p` gurobi variable.

    Args:
        i (int): customer id
        k (int): good id
        k (object): list of `order_count`
    """
    return sum(n[:i]) + k


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


# Solve by Gurobi model

m = g.Model("TurkeyBox")


# CREATE VARIABLES
# je zbozi umisteno
g_p = m.addVars(sum(order_count), vtype=g.GRB.BINARY, name="Good is placed")

# CREATE CONSTRAINS
# 1) Single customer per locker
# 2) Locker is not overfilled


# CREATE OBJECTIVE
# maximize the profit
m.setObjective(
    g.quicksum(
        orders[i]["price"][k] * g_p[get_lock_position(i, k, order_count)]
        for i in range(customer_count)
        for k in range(order_count[i])
    ), g.GRB.MAXIMIZE
)


# Solve the model
m.optimize()

# Print results
