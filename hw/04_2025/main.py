#!/usr/bin/env python3
import math
import sys
import itertools
from collections import deque


# --- Minimum-Cost Flow: Core Edge Functions ---

def create_edge(u, v, cost=0, lower_bound=0, upper_bound=1, flow=0, residual_flow=0, pair=None):
    """Creates a directed edge with flow-related metadata."""
    return {
        'u': u, 'v': v, 'cost': cost,
        'lower_bound': lower_bound, 'upper_bound': upper_bound,
        'flow': flow, 'residual_flow': residual_flow,
        'pair': pair
    }


def augment_edge(edge, value):
    """Updates flow and residual capacity in the edge and its reverse pair."""
    edge['residual_flow'] -= value
    edge['flow'] += value


def add_edge(graph, edge):
    """Adds a directed edge to the graph's adjacency list."""
    graph[edge['u']].append(edge)


def create_edge_pair(u, v, cost, capacity):
    """Creates a forward and reverse edge with cost and capacity."""
    forward = create_edge(
        u, v, cost=cost, residual_flow=capacity, upper_bound=capacity)
    backward = create_edge(
        v, u, cost=-cost, residual_flow=0, upper_bound=capacity)
    forward['pair'], backward['pair'] = backward, forward
    return forward, backward


def copy_graph(graph):
    """Performs a shallow copy of graph structure (not deep copy of edges)."""
    return [edges.copy() for edges in graph]


# --- Edmonds-Karp Algorithm: Initial Feasible Flow Finder ---

def bfs_augmenting_path(graph, source, sink):
    """BFS to find an augmenting path with available residual capacity."""
    parent = {}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for edge in graph[node]:
            if edge['v'] not in parent and edge['residual_flow'] > 0:
                parent[edge['v']] = edge
                queue.append(edge['v'])
                if edge['v'] == sink:
                    return parent
    return parent


def apply_augmentation(parent, source, sink):
    """Augments flow along a found path and returns the augmented amount."""
    flow = math.inf
    current = sink
    while current != source:
        edge = parent[current]
        flow = min(flow, edge['residual_flow'])
        current = edge['u']

    current = sink
    while current != source:
        edge = parent[current]
        augment_edge(edge, flow)
        augment_edge(edge['pair'], -flow)
        current = edge['u']

    return flow


def edmonds_karp(graph, source, sink):
    """Classic max flow algorithm using BFS repeatedly to augment flow."""
    total_flow = 0
    while True:
        parent = bfs_augmenting_path(graph, source, sink)
        if sink not in parent:
            break
        total_flow += apply_augmentation(parent, source, sink)
    return total_flow


# --- Cycle Canceling: Cost Optimization ---

def find_negative_cycle(graph, n):
    """Detects a negative-cost cycle using Bellman-Ford."""
    cost = {v: 0 for v in range(n)}
    parent = {v: None for v in range(n)}
    last = None

    for _ in range(n):
        last = None
        for edge in itertools.chain.from_iterable(graph):
            if edge['residual_flow'] > 0:
                u, v, c = edge['u'], edge['v'], edge['cost']
                if cost[v] > cost[u] + c:
                    cost[v] = cost[u] + c
                    parent[v] = edge
                    last = v

    if last is None:
        return parent, None

    for _ in range(n):
        last = parent[last]['u']
    return parent, last


def cancel_negative_cycle(parent, cycle_start):
    """Augments flow along the detected negative cycle."""
    delta = math.inf
    v = cycle_start
    while True:
        edge = parent[v]
        delta = min(delta, edge['residual_flow'])
        v = edge['u']
        if v == cycle_start:
            break

    v = cycle_start
    while True:
        edge = parent[v]
        augment_edge(edge, delta)
        augment_edge(edge['pair'], -delta)
        v = edge['u']
        if v == cycle_start:
            break


def cancel_cycles(graph, n):
    """Main loop to repeatedly cancel negative-cost cycles."""
    while True:
        parent, start = find_negative_cycle(graph, n)
        if start is None:
            break
        cancel_negative_cycle(parent, start)


# --- Min-Cost Flow with Demand Balancing ---

def is_balanced_flow_possible(original_graph, balances):
    """Adds super source/sink and checks if flow balances are feasible."""
    graph = copy_graph(original_graph)
    graph.append([])  # super source
    graph.append([])  # super sink
    source, sink = len(graph) - 2, len(graph) - 1

    for node, balance in balances.items():
        if balance > 0:
            e1, e2 = create_edge_pair(source, node, cost=0, capacity=balance)
        elif balance < 0:
            e1, e2 = create_edge_pair(node, sink, cost=0, capacity=-balance)
        else:
            continue
        add_edge(graph, e1)
        add_edge(graph, e2)

    edmonds_karp(graph, source, sink)

    return all(edge['flow'] >= edge['upper_bound'] for edge in graph[source])


def compute_min_cost_flow(graph, n, balances):
    """Computes minimum-cost flow using cycle canceling."""
    if not is_balanced_flow_possible(graph, balances):
        raise ValueError("No feasible balanced flow exists.")
    cancel_cycles(graph, n)


# --- Main: Tracking Objects Using Frame-by-Frame Assignment ---

def main(input_path, output_path):
    """
    Solves the object tracking assignment problem using minimum-cost flow:
    Matches positions between frames based on Euclidean distance.
    """
    with open(input_path, 'r', encoding='utf8') as f:
        n, p = map(int, f.readline().split())
        positions = [list(map(int, f.readline().split())) for _ in range(p)]

    with open(output_path, 'w', encoding='utf8') as f_out:
        for frame_idx in range(p - 1):
            current_frame = positions[frame_idx]
            next_frame = positions[frame_idx + 1]
            graph = [[] for _ in range(2 * n)]

            # Build bipartite graph from current_frame to next_frame
            for u in range(n):
                x1, y1 = current_frame[2 * u], current_frame[2 * u + 1]
                for v in range(n):
                    x2, y2 = next_frame[2 * v], next_frame[2 * v + 1]
                    cost = math.hypot(x1 - x2, y1 - y2)
                    e1 = create_edge(u, v + n, cost=cost, residual_flow=1)
                    e2 = create_edge(v + n, u, cost=-cost, residual_flow=0)
                    e1['pair'], e2['pair'] = e2, e1
                    add_edge(graph, e1)
                    add_edge(graph, e2)

            balances = {u: 1 if u < n else -1 for u in range(2 * n)}
            compute_min_cost_flow(graph, 2 * n, balances)

            # Extract assignments for current frame
            assignment = []
            for u in range(n):
                matched = next(edge for edge in graph[u] if edge['flow'] > 0)
                assignment.append(matched['v'] - n + 1)
            f_out.write(" ".join(map(str, assignment)) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_path>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
