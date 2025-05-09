#!/usr/bin/env python3
import itertools
import math
import sys
from collections import deque


def create_edge(from_node: int, to_node: int, cost: float = 0, lower_bound: int = 0,
                upper_bound: int = 1, flow: int = 0, residual_flow: int = 0,
                pair: dict = None) -> dict:
    return {
        'u': from_node,
        'v': to_node,
        'cost': cost,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'flow': flow,
        'residual_flow': residual_flow,
        'pair': pair
    }


def augment_edge(edge, value):
    edge['residual_flow'] -= value
    edge['flow'] += value


def add_edge(graph: list[list[dict]], edge: dict) -> None:
    graph[edge['u']].append(edge)


def copy_graph(graph):
    return [edges.copy() for edges in graph]


def create_paired_edges(from_node, to_node, capacity):
    forward_edge = create_edge(
        from_node, to_node, residual_flow=capacity, upper_bound=capacity)
    backward_edge = create_edge(
        to_node, from_node, residual_flow=0, upper_bound=capacity)
    forward_edge['pair'], backward_edge['pair'] = backward_edge, forward_edge
    return forward_edge, backward_edge


def bfs_find_augmenting_path(graph, source, sink):
    parent_edges = {}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        if current == sink:
            break
        for edge in graph[current]:
            if edge['v'] not in parent_edges and edge['residual_flow'] > 0:
                parent_edges[edge['v']] = edge
                queue.append(edge['v'])
    return parent_edges


def apply_augmentation(parent_edges, source, sink):
    flow_increment = math.inf
    current = sink
    while current != source:
        edge = parent_edges[current]
        flow_increment = min(flow_increment, edge['residual_flow'])
        current = edge['u']

    current = sink
    while current != source:
        edge = parent_edges[current]
        augment_edge(edge, flow_increment)
        augment_edge(edge['pair'], -flow_increment)
        current = edge['u']

    return flow_increment


def edmonds_karp_max_flow(graph, source, sink):
    total_flow = 0
    while True:
        parent_edges = bfs_find_augmenting_path(graph, source, sink)
        if sink not in parent_edges:
            break
        total_flow += apply_augmentation(parent_edges, source, sink)
    return total_flow


def max_flow_with_balances(original_graph, node_balances):
    graph = copy_graph(original_graph)
    graph.append([])  # super_source
    graph.append([])  # super_sink
    super_source = len(graph) - 2
    super_sink = len(graph) - 1

    for node, balance in node_balances.items():
        if balance > 0:
            forward, backward = create_paired_edges(
                super_source, node, balance)
            add_edge(graph, forward)
            add_edge(graph, backward)
        elif balance < 0:
            forward, backward = create_paired_edges(node, super_sink, -balance)
            add_edge(graph, forward)
            add_edge(graph, backward)

    edmonds_karp_max_flow(graph, super_source, super_sink)

    for edge in graph[super_source]:
        if edge['flow'] < edge['upper_bound']:
            return False
    return True


def find_negative_cost_cycle(graph, num_nodes):
    best_cost = {node: 0 for node in range(num_nodes)}
    parent_edge = {node: None for node in range(num_nodes)}
    last_updated_node = None

    for _ in range(num_nodes):
        last_updated_node = None
        for edge in itertools.chain.from_iterable(graph):
            if edge['residual_flow'] > 0:
                u, v, cost = edge['u'], edge['v'], edge['cost']
                if best_cost[v] > best_cost[u] + cost:
                    best_cost[v] = best_cost[u] + cost
                    parent_edge[v] = edge
                    last_updated_node = v

    if last_updated_node is None:
        return parent_edge, None

    for _ in range(num_nodes):
        last_updated_node = parent_edge[last_updated_node]['u']

    return parent_edge, last_updated_node


def cancel_cycle_flow(parent_edge, cycle_start_node):
    min_augment = math.inf
    current = cycle_start_node
    while True:
        edge = parent_edge[current]
        min_augment = min(min_augment, edge['residual_flow'])
        current = edge['u']
        if current == cycle_start_node:
            break

    current = cycle_start_node
    while True:
        edge = parent_edge[current]
        augment_edge(edge, min_augment)
        augment_edge(edge['pair'], -min_augment)
        current = edge['u']
        if current == cycle_start_node:
            break


def cancel_negative_cycles(graph, num_nodes):
    while True:
        parent_edge, cycle_start_node = find_negative_cost_cycle(
            graph, num_nodes)
        if cycle_start_node is None:
            break
        cancel_cycle_flow(parent_edge, cycle_start_node)


def compute_min_cost_flow(graph, num_nodes, node_balances):
    if max_flow_with_balances(graph, node_balances):
        cancel_negative_cycles(graph, num_nodes)
    else:
        raise ValueError('Unsolvable flow problem')


def main(input_path, output_path):
    with open(input_path, mode='r+', encoding='utf8') as input_file:
        num_nodes, _ = map(int, input_file.readline().split())
        flow_graphs = []
        previous_positions = list(map(int, input_file.readline().split()))

        for line in input_file:
            current_positions = list(map(int, line.split()))
            graph = [[] for _ in range(2 * num_nodes)]
            for from_index, (x1, y1) in enumerate(zip(previous_positions[::2], previous_positions[1::2])):
                for to_index, (x2, y2) in enumerate(zip(current_positions[::2], current_positions[1::2])):
                    distance = math.hypot(x1 - x2, y1 - y2)
                    forward_edge = create_edge(
                        from_index, to_index + num_nodes, cost=distance, residual_flow=1)
                    backward_edge = create_edge(
                        to_index + num_nodes, from_index, cost=-distance, residual_flow=0)
                    forward_edge['pair'], backward_edge['pair'] = backward_edge, forward_edge
                    add_edge(graph, forward_edge)
                    add_edge(graph, backward_edge)
            flow_graphs.append(graph)
            previous_positions = current_positions

    with open(output_path, mode='w+', encoding='utf8') as output_file:
        balances = {node: 1 if node < num_nodes else -
                    1 for node in range(2 * num_nodes)}
        for graph in flow_graphs:
            compute_min_cost_flow(graph, 2 * num_nodes, balances)
            matching = []
            for source_node in range(num_nodes):
                matched_edge = next(
                    edge for edge in graph[source_node]
                    if edge['flow'] > 0 and edge['v'] >= num_nodes
                )
                matching.append(matched_edge['v'] - num_nodes + 1)
            output_file.write(f"{' '.join(map(str, matching))}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: please specify input and output paths as arguments in this form: `script.py <input_path> <output_path>`", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
