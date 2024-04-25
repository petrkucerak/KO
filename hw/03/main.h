#ifndef __MAIN_H
#define __MAIN_H

#include <vector>

using namespace std;

typedef struct edge {
   struct flow_node *from, *to;
   int lower_bound;
   int upper_bound;
   int flow;
   bool natural;
   int increment;
} edge_t;

typedef struct flow_node {
   vector<edge_t *> inbound_edges;
   vector<edge_t *> outbound_edges;
   edge_t *augmenting_edge;
   int iteration;
   int name;
   int balance;
} flow_node_t;

typedef struct customer {
   int lower_bound;
   int upper_bound;
   vector<int> bought_products;
} customer_t;

/**
 * @brief Open the file and load input data
 *
 * @param input_path
 */
void load_file(char *input_path);

/**
 * @brief Create file and write success solution
 *
 * @param output_file
 * @param customer_nodes
 */
void write_output_sol(char *output_file, flow_node_t *customer_nodes);

/**
 * @brief Create file and write infusible solution
 *
 * @param output_file
 */
void write_output_inf(char *output_file);

void compute_balance(flow_node_t &n);

void update_bounds(flow_node_t &n);

void connect_based_on_balance(flow_node_t &n, flow_node_t &new_s,
                              flow_node_t &new_t);

int search(flow_node_t &s, flow_node_t &t);

/**
 * @brief Implementation Ford Fulkerson algorithm
 * https://cs.wikipedia.org/wiki/Ford%C5%AFv%E2%80%93Fulkerson%C5%AFv_algoritmus
 *
 * @param s start node
 * @param t target node
 */
void ford_fulkerson(flow_node_t &s, flow_node_t &t);

void free_resources(flow_node_t &s, flow_node_t *customer_nodes,
                    flow_node_t *product_nodes);

#endif // __MAIN_H