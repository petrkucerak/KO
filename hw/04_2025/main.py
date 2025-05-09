#!/usr/bin/env python3
import itertools
import math
import sys
from collections import deque

# --- Edge utility functions ---


def create_edge(src: int, dest: int, cost: float = 0, lower_bound: int = 0,
                upper_bound: int = 1, flow: int = 0, residual_flow: int = 0,
                pair: dict = None) -> dict:
    """Create an edge with flow and cost attributes for flow network."""
    return {
        'u': src,
        'v': dest,
        'cost': cost,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'flow': flow,
        'residual_flow': residual_flow,
        'pair': pair
    }


def augment_edge(edge, flow_amount):
    """Augments flow along an edge and updates the residual capacity."""
    edge['residual_flow'] -= flow_amount
    edge['flow'] += flow_amount


def add_edge(graph: list[list[dict]], edge: dict) -> None:
    """Adds an edge to the graph."""
    graph[edge['u']].append(edge)


def copy_graph(graph):
    """Creates a shallow copy of the graph (used for augmentation)."""
    return [edges.copy() for edges in graph]


def paired_edges(src, dest, capacity):
    """Creates a forward and reverse edge pair with capacity for residual graph."""
    forward = create_edge(
        src, dest, residual_flow=capacity, upper_bound=capacity)
    backward = create_edge(dest, src, residual_flow=0, upper_bound=capacity)
    forward['pair'], backward['pair'] = backward, forward
    return forward, backward


# --- Flow algorithms ---

def bfs(graph, source, sink):
    """Breadth-first search to find augmenting paths in the residual graph."""
    parents = {}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        if current == sink:
            break
        for edge in graph[current]:
            if edge['v'] not in parents and edge['residual_flow'] > 0:
                parents[edge['v']] = edge
                queue.append(edge['v'])
    return parents


def calculate_augmentation(parents, source, sink):
    """Augment flow along the path found by BFS."""
    augment_value = math.inf
    v = sink
    while v != source:
        edge = parents[v]
        augment_value = min(augment_value, edge['residual_flow'])
        v = edge['u']

    v = sink
    while v != source:
        edge = parents[v]
        augment_edge(edge, augment_value)
        augment_edge(edge['pair'], -augment_value)
        v = edge['u']

    return augment_value


def edmonds_karp(graph, source, sink):
    """
    Computes max flow using Edmonds-Karp algorithm (BFS-based Ford-Fulkerson).
    """
    total_flow = 0
    while True:
        parents = bfs(graph, source, sink)
        if sink not in parents:
            break
        total_flow += calculate_augmentation(parents, source, sink)
    return total_flow


def max_flow_demands(original_graph, node_balances):
    """
    Check if it's possible to satisfy flow demands (specified by node_balances).
    Adds a super source and super sink to handle excess supply/demand.
    """
    graph = copy_graph(original_graph)
    graph.append([])  # super_source
    graph.append([])  # super_sink
    super_source = len(graph) - 2
    super_sink = len(graph) - 1

    for node, balance in node_balances.items():
        if balance > 0:
            # Node is a source (supply)
            fwd, bwd = paired_edges(super_source, node, balance)
            add_edge(graph, fwd)
            add_edge(graph, bwd)
        elif balance < 0:
            # Node is a sink (demand)
            fwd, bwd = paired_edges(node, super_sink, -balance)
            add_edge(graph, fwd)
            add_edge(graph, bwd)

    edmonds_karp(graph, super_source, super_sink)

    # Ensure that all supply was successfully routed
    for edge in graph[super_source]:
        if edge['flow'] < edge['upper_bound']:
            return False
    return True


# --- Cycle canceling for min-cost flow ---

def find_negative_cycle(graph, num_vertices):
    """Bellman-Ford to detect negative cost cycles in residual graph."""
    cost_to = {v: 0 for v in range(num_vertices)}
    parents = {v: None for v in range(num_vertices)}
    last_updated = None

    for _ in range(num_vertices):
        last_updated = None
        for edge in itertools.chain.from_iterable(graph):
            if edge['residual_flow'] > 0:
                u, v, cost = edge['u'], edge['v'], edge['cost']
                if cost_to[v] > cost_to[u] + cost:
                    cost_to[v] = cost_to[u] + cost
                    parents[v] = edge
                    last_updated = v

    if last_updated is None:
        return parents, None

    # Find cycle start
    for _ in range(num_vertices):
        last_updated = parents[last_updated]['u']
    return parents, last_updated


def cancel_cycle(parents, start_node):
    """Augment flow along a negative cost cycle to reduce total cost."""
    min_flow = math.inf
    v = start_node
    while True:
        edge = parents[v]
        min_flow = min(min_flow, edge['residual_flow'])
        v = edge['u']
        if v == start_node:
            break

    v = start_node
    while True:
        edge = parents[v]
        augment_edge(edge, min_flow)
        augment_edge(edge['pair'], -min_flow)
        v = edge['u']
        if v == start_node:
            break


def cycle_canceling(graph, num_vertices):
    """Repeatedly cancel negative cost cycles until none are left."""
    while True:
        parents, cycle_start = find_negative_cycle(graph, num_vertices)
        if cycle_start is None:
            break
        cancel_cycle(parents, cycle_start)


def min_cost_flow(graph, num_vertices, node_balances):
    """Solve minimum-cost flow problem with demands using cycle canceling."""
    if max_flow_demands(graph, node_balances):
        cycle_canceling(graph, num_vertices)
    else:
        raise ValueError('Unsolvable flow problem')


# --- Main I/O & matching logic ---

def main(input_path, output_path):
    """Reads position frames, computes minimum-cost bipartite matching over time."""
    with open(input_path, mode='r+', encoding='utf8') as f_in:
        n, num_frames = map(int, f_in.readline().split())
        frame_graphs = []
        previous_positions = list(map(int, f_in.readline().split()))

        # Read each time step and construct flow graphs
        for line in f_in:
            current_positions = list(map(int, line.split()))
            # Left: previous, Right: current
            graph = [[] for _ in range(2 * n)]
            for u, (x1, y1) in enumerate(zip(previous_positions[::2], previous_positions[1::2])):
                for v, (x2, y2) in enumerate(zip(current_positions[::2], current_positions[1::2])):
                    distance = math.hypot(x1 - x2, y1 - y2)
                    forward = create_edge(
                        u, v + n, cost=distance, residual_flow=1)
                    backward = create_edge(
                        v + n, u, cost=-distance, residual_flow=0)
                    forward['pair'], backward['pair'] = backward, forward
                    add_edge(graph, forward)
                    add_edge(graph, backward)
            frame_graphs.append(graph)
            previous_positions = current_positions

    with open(output_path, mode='w+', encoding='utf8') as f_out:
        node_balances = {u: 1 if u < n else -1 for u in range(2 * n)}
        for graph in frame_graphs:
            min_cost_flow(graph, 2 * n, node_balances)
            matching = []
            for u in range(n):
                matched_edge = next(e for e in graph[u]
                                    if e['flow'] > 0 and e['v'] >= n)
                matching.append(matched_edge['v'] - n + 1)
            f_out.write(f"{' '.join(map(str, matching))}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: please specify input and output paths as arguments in this form: `script.py <input_path> <output_path>`", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
