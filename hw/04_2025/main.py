#!/usr/bin/env python3
import itertools
import math
import sys
from collections import deque


def create_edge(u: int, v: int, cost: float = 0, lower_bound: int = 0,
                upper_bound: int = 1, flow: int = 0, residual_flow: int = 0,
                pair: dict = None) -> dict:
    return {
        'u': u,
        'v': v,
        'cost': cost,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'flow': flow,
        'residual_flow': residual_flow,
        'pair': pair
    }


def augment_edge(edge, val):
    edge['residual_flow'] -= val
    edge['flow'] += val


def add_edge(graph: list[list[dict]], edge: dict) -> None:
    graph[edge['u']].append(edge)


def copy_graph(graph):
    return [edges.copy() for edges in graph]


def paired_edges(u, v, ub):
    e1 = create_edge(u, v, residual_flow=ub, upper_bound=ub)
    e2 = create_edge(v, u, residual_flow=0, upper_bound=ub)
    e1['pair'], e2['pair'] = e2, e1
    return e1, e2


def bfs(graph, s, t):
    parents = {}
    queue = deque([s])
    while queue:
        current = queue.popleft()
        if current == t:
            break
        for edge in graph[current]:
            if edge['v'] not in parents and edge['residual_flow'] > 0:
                parents[edge['v']] = edge
                queue.append(edge['v'])
    return parents


def calculate_augmentation(parents, s, t):
    augment_value = math.inf
    v = t
    while v != s:
        edge = parents[v]
        augment_value = min(augment_value, edge['residual_flow'])
        v = edge['u']

    v = t
    while v != s:
        edge = parents[v]
        augment_edge(edge, augment_value)
        augment_edge(edge['pair'], -augment_value)
        v = edge['u']

    return augment_value


def edmonds_karp(graph, s, t):
    '''
    described in: https://www.w3schools.com/dsa/dsa_algo_graphs_edmondskarp.php
    '''
    flow = 0
    while True:
        parents = bfs(graph, s, t)
        if t not in parents:
            break
        flow += calculate_augmentation(parents, s, t)
    return flow


def max_flow_demands(original_graph, balances):
    graph = copy_graph(original_graph)
    graph.append([])  # new_s
    graph.append([])  # new_t
    new_s = len(graph) - 2
    new_t = len(graph) - 1

    for v, balance in balances.items():
        if balance > 0:
            e1, e2 = paired_edges(new_s, v, balance)
            add_edge(graph, e1)
            add_edge(graph, e2)
        elif balance < 0:
            e1, e2 = paired_edges(v, new_t, -balance)
            add_edge(graph, e1)
            add_edge(graph, e2)

    edmonds_karp(graph, new_s, new_t)

    for e in graph[new_s]:
        if e['flow'] < e['upper_bound']:
            return False
    return True


def find_negative_cycle(graph, num_vertices):
    best_cost = {u: 0 for u in range(num_vertices)}
    parents = {v: None for v in range(num_vertices)}
    last_relaxed = None

    for _ in range(num_vertices):
        last_relaxed = None
        for edge in itertools.chain.from_iterable(graph):
            if edge['residual_flow'] > 0:
                u, v, cost = edge['u'], edge['v'], edge['cost']
                if best_cost[v] > best_cost[u] + cost:
                    best_cost[v] = best_cost[u] + cost
                    parents[v] = edge
                    last_relaxed = v

    if last_relaxed is None:
        return parents, None

    for _ in range(num_vertices):
        last_relaxed = parents[last_relaxed]['u']
    return parents, last_relaxed


def cancel_cycle(parents, cycle_vertex):
    augment_val = math.inf
    v = cycle_vertex
    while True:
        e = parents[v]
        augment_val = min(augment_val, e['residual_flow'])
        v = e['u']
        if v == cycle_vertex:
            break

    v = cycle_vertex
    while True:
        edge = parents[v]
        augment_edge(edge, augment_val)
        augment_edge(edge['pair'], -augment_val)
        v = edge['u']
        if v == cycle_vertex:
            break


def cycle_canceling(graph, num_vertices):
    while True:
        parents, cycle_vertex = find_negative_cycle(graph, num_vertices)
        if cycle_vertex is None:
            break
        cancel_cycle(parents, cycle_vertex)


def min_flow(graph, num_vertices, balances):
    if max_flow_demands(graph, balances):
        cycle_canceling(graph, num_vertices)
    else:
        raise ValueError('Unsolvable flow problem')


def main(input_path, output_path):
    with open(input_path, mode='r+', encoding='utf8') as f_in:
        n, p = map(int, f_in.readline().split())
        graphs = []
        prev_positions = list(map(int, f_in.readline().split()))

        for line in f_in:
            curr_positions = list(map(int, line.split()))
            graph = [[] for _ in range(2 * n)]
            for u, (ux, uy) in enumerate(zip(prev_positions[::2], prev_positions[1::2])):
                for v, (vx, vy) in enumerate(zip(curr_positions[::2], curr_positions[1::2])):
                    dist = math.hypot(ux - vx, uy - vy)
                    e1 = create_edge(u, v + n, cost=dist, residual_flow=1)
                    e2 = create_edge(v + n, u, cost=-dist, residual_flow=0)
                    e1['pair'], e2['pair'] = e2, e1
                    add_edge(graph, e1)
                    add_edge(graph, e2)
            graphs.append(graph)
            prev_positions = curr_positions

    with open(output_path, mode='w+', encoding='utf8') as f_out:
        b = {u: 1 if u < n else -1 for u in range(2 * n)}
        for graph in graphs:
            min_flow(graph, 2 * n, b)
            positions = []
            for u in range(n):
                edge = next(e for e in graph[u]
                            if e['flow'] > 0 and e['v'] >= n)
                positions.append(edge['v'] - n + 1)
            f_out.write(f"{' '.join(map(str, positions))}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: please specify input and output paths as arguments in this form: `script.py <input_path> <output_path>`", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
