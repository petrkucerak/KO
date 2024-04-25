/**
 * @file main.cpp
 * @author Petr Kucera (kucerp28@fel.cvut.cz)
 * @brief Implementation Ford Fulkerson algorithm to solve problem thats
 * describe in `2024_hw03.pdf` file. The implementation is inspired by Jakub
 * Jira implementation (https://github.com/japawBlob/B4M35KO).
 * @version 0.1
 * @date 2024-04-25
 *
 * @copyright Copyright (c) 2024
 *
 */

#include <cstring>
#include <iostream>
#include <queue>
#include <stack>
#include <vector>

#include "main.h"

int number_of_customers = 0;
int number_of_products = 0;

vector<customer_t> customers;
vector<int> products;

int main(int argc, char **argv)
{
   if (argc < 3) {
      cout << "Specify 2 arguments. Example: "
           << "'./program <input path> <output_path>'\n";
   }
   load_file(argv[1]);

   int term_names = -1;
   flow_node_t s;
   s.iteration = 0;
   s.name = term_names--;
   flow_node_t t;
   t.iteration = 0;
   t.name = term_names--;
   flow_node_t customer_nodes[number_of_customers];
   flow_node_t product_nodes[number_of_products];

   flow_node_t s1;
   s1.iteration = 0;
   s1.name = term_names--;
   flow_node_t t1;
   t1.iteration = 0;
   t1.name = term_names--;

   flow_node_t customer_nodes_1[number_of_customers];
   flow_node_t product_nodes_1[number_of_products];

   for (int i = 0; i < number_of_customers; i++) {
      edge_t *e = new edge_t, *e1 = new edge_t;

      e->lower_bound = customers[i].lower_bound;
      e->upper_bound = customers[i].upper_bound;
      e->flow = 0;
      e->from = &s;
      e->to = &customer_nodes[i];
      s.outbound_edges.push_back(e);
      customer_nodes[i].inbound_edges.push_back(e);
      customer_nodes[i].iteration = 0;
      customer_nodes[i].name = i;

      e1->lower_bound = customers[i].lower_bound;
      e1->upper_bound = customers[i].upper_bound;
      e1->flow = 0;
      e1->from = &s1;
      e1->to = &customer_nodes_1[i];
      s1.outbound_edges.push_back(e1);
      customer_nodes_1[i].inbound_edges.push_back(e1);
      customer_nodes_1[i].iteration = 0;
      customer_nodes_1[i].name = i;

      for (auto u : customers[i].bought_products) {
         edge_t *ee = new edge_t, *ee1 = new edge_t;
         ee->lower_bound = 0;
         ee->upper_bound = 1;
         ee->flow = 0;
         ee->from = &customer_nodes[i];
         ee->to = &product_nodes[u];
         customer_nodes[i].outbound_edges.push_back(ee);
         product_nodes[u].inbound_edges.push_back(ee);

         ee1->lower_bound = 0;
         ee1->upper_bound = 1;
         ee1->flow = 0;
         ee1->from = &customer_nodes_1[i];
         ee1->to = &product_nodes_1[u];
         customer_nodes_1[i].outbound_edges.push_back(ee1);
         product_nodes_1[u].inbound_edges.push_back(ee1);
      }
   }
   for (int i = 0; i < number_of_products; i++) {
      edge_t *e = new edge_t, *e1 = new edge_t;
      e->from = &product_nodes[i];
      e->to = &t;
      e->lower_bound = products[i];
      e->upper_bound = INT32_MAX;
      e->flow = 0;
      t.inbound_edges.push_back(e);
      product_nodes[i].outbound_edges.push_back(e);
      product_nodes[i].iteration = 0;
      product_nodes[i].name = i;

      e1->from = &product_nodes_1[i];
      e1->to = &t1;
      e1->lower_bound = products[i];
      e1->upper_bound = INT32_MAX;
      e1->flow = 0;
      t1.inbound_edges.push_back(e1);
      product_nodes_1[i].outbound_edges.push_back(e1);
      product_nodes_1[i].iteration = 0;
      product_nodes_1[i].name = i;
   }

   edge_t *overflow_edge = new edge_t;
   overflow_edge->lower_bound = 0;
   overflow_edge->flow = 0;
   overflow_edge->upper_bound = INT32_MAX;
   overflow_edge->from = &t1;
   overflow_edge->to = &s1;
   t1.outbound_edges.push_back(overflow_edge);
   s1.inbound_edges.push_back(overflow_edge);

   compute_balance(s1);
   compute_balance(t1);
   for (auto &i : customer_nodes_1) {
      compute_balance(i);
   }
   for (auto &i : product_nodes_1) {
      compute_balance(i);
   }
   update_bounds(s1);
   update_bounds(t1);
   for (auto &i : customer_nodes_1) {
      update_bounds(i);
   }
   for (auto &i : product_nodes_1) {
      update_bounds(i);
   }

   flow_node_t new_s;
   new_s.name = term_names--;
   new_s.iteration = 0;
   flow_node_t new_t;
   new_t.name = term_names--;
   new_t.iteration = 0;
   connect_based_on_balance(s1, new_s, new_t);
   connect_based_on_balance(t1, new_s, new_t);
   for (auto &i : customer_nodes_1) {
      connect_based_on_balance(i, new_s, new_t);
   }
   for (auto &i : product_nodes_1) {
      connect_based_on_balance(i, new_s, new_t);
   }

   ford_fulkerson(new_s, new_t);

   for (auto &b : new_s.outbound_edges) {
      if (b->flow != b->upper_bound) {
         write_output_inf(argv[2]);
         cerr << "Infusible!\n";
         return 0;
      }
   }

   int count = 0;
   for (auto &e : s1.outbound_edges) {
      if (e->to->name == new_t.name) {
         continue;
      }
      s.outbound_edges[count]->flow =
          e->flow + s.outbound_edges[count]->lower_bound;
      count++;
   }

   for (int i = 0; i < number_of_customers; i++) {
      count = 0;
      for (auto &e : customer_nodes_1[i].outbound_edges) {
         if (e->to->name == new_t.name) {
            continue;
         }
         customer_nodes[i].outbound_edges[count]->flow =
             e->flow + customer_nodes[i].outbound_edges[count]->lower_bound;
         count++;
      }
   }
   for (int i = 0; i < number_of_products; i++) {
      count = 0;
      for (auto &e : product_nodes_1[i].outbound_edges) {
         if (e->to->name == new_t.name) {
            continue;
         }
         product_nodes[i].outbound_edges[count]->flow =
             e->flow + product_nodes[i].outbound_edges[count]->lower_bound;
         count++;
      }
   }

   ford_fulkerson(s, t);

   write_output_sol(argv[2], customer_nodes);

   free_resources(s, customer_nodes, product_nodes);
   free_resources(new_s, customer_nodes_1, product_nodes_1);

   for (auto &e : t1.outbound_edges) {
      delete e;
   }
   for (auto &e : s1.outbound_edges) {
      delete e;
   }
   return 0;
}

void load_file(char *input_path)
{
   FILE *f = fopen(input_path, "r");

   if (f == nullptr) {
      cout << "Could not open file with input [load_file]\n";
      return;
   }
   fscanf(f, "%i %i", &number_of_customers, &number_of_products);
   for (int i = 0; i < number_of_customers; i++) {
      customer_t tmp;
      fscanf(f, " %i %i", &tmp.lower_bound, &tmp.upper_bound);
      char c;
      while ((c = fgetc(f)) != '\n') {
         int t;
         fscanf(f, "%i", &t);
         tmp.bought_products.push_back(t - 1);
      }
      customers.push_back(tmp);
   }
   for (int i = 0; i < number_of_products; i++) {
      int tmp;
      fscanf(f, "%i", &tmp);
      products.push_back(tmp);
   }
   fclose(f);
}

void write_output_sol(char *output_file, flow_node_t *customer_nodes)
{
   FILE *f = fopen(output_file, "w+");

   if (f == nullptr) {
      cout << "Could not create file with solution [write_output_sol]\n";
      return;
   }

   for (int i = 0; i < number_of_customers; i++) {
      for (auto &e : customer_nodes[i].outbound_edges) {
         if (e->flow == 1) {
            fprintf(f, "%i ", e->to->name + 1);
            cout << e->to->name + 1 << " ";
         }
      }
      fprintf(f, "\n");
      cout << endl;
   }

   fclose(f);
}

void write_output_inf(char *output_file)
{
   FILE *f = fopen(output_file, "w+");

   if (f == nullptr) {
      cout << "Could not create file with solution [write_output_inf]\n";
      return;
   }

   fprintf(f, "-1\n");

   fclose(f);
}

void compute_balance(flow_node_t &n)
{
   int sum_inbound = 0, sum_outbound = 0;
   for (const auto &e : n.inbound_edges) {
      sum_inbound += e->lower_bound;
   }
   for (const auto &e : n.outbound_edges) {
      sum_outbound += e->lower_bound;
   }
   n.balance = sum_inbound - sum_outbound;
}

void update_bounds(flow_node_t &n)
{
   for (auto &e : n.inbound_edges) {
      e->upper_bound -= e->lower_bound;
      e->lower_bound = 0;
   }
   for (auto &e : n.outbound_edges) {
      e->upper_bound -= e->lower_bound;
      e->lower_bound = 0;
   }
}

void connect_based_on_balance(flow_node_t &n, flow_node_t &new_s,
                              flow_node_t &new_t)
{
   if (n.balance > 0) {
      edge_t *e = new edge_t;
      e->lower_bound = 0;
      e->flow = 0;
      e->upper_bound = n.balance;
      e->from = &new_s;
      e->to = &n;
      new_s.outbound_edges.push_back(e);
      n.inbound_edges.push_back(e);
   } else if (n.balance < 0) {
      edge_t *e = new edge_t;
      e->lower_bound = 0;
      e->flow = 0;
      e->upper_bound = -n.balance;
      e->from = &n;
      e->to = &new_t;
      n.outbound_edges.push_back(e);
      new_t.inbound_edges.push_back(e);
   }
}

int search(flow_node_t &s, flow_node_t &t)
{
   int terminate = t.name;
   int iteration = ++s.iteration;
   queue<flow_node *> st;
   s.augmenting_edge = nullptr;
   st.push(&s);

   flow_node *current_node;
   while (!st.empty()) {
      current_node = st.front();
      st.pop();
      if (current_node->name == terminate) {
         edge_t *e = current_node->augmenting_edge;
         int max_flow_increase = INT32_MAX;
         while (e != nullptr) {
            max_flow_increase = min(max_flow_increase, e->increment);
            if (e->natural) {
               e = e->from->augmenting_edge;
            } else {
               e = e->to->augmenting_edge;
            }
         }
         return max_flow_increase;
      }
      for (auto &e : current_node->outbound_edges) {
         if (e->to->iteration != iteration && e->flow < e->upper_bound) {
            e->to->iteration = iteration;
            e->increment = e->upper_bound - e->flow;
            e->natural = true;
            e->to->augmenting_edge = e;
            st.push(e->to);
         }
      }
      for (auto &e : current_node->inbound_edges) {
         if (e->from->iteration != iteration && e->lower_bound < e->flow) {
            e->from->iteration = iteration;
            e->increment = e->flow - e->lower_bound;
            e->natural = false;
            e->from->augmenting_edge = e;
            st.push(e->from);
         }
      }
   }
   return 0;
}

void ford_fulkerson(flow_node_t &s, flow_node_t &t)
{
   flow_node_t *current_node = &t;
   int flow_increase;
   while ((flow_increase = search(s, t)) != 0) {
      edge_t *curr_aug_path = current_node->augmenting_edge;
      while (curr_aug_path != nullptr) {
         if (curr_aug_path->natural) {
            curr_aug_path->flow += flow_increase;
            curr_aug_path = curr_aug_path->from->augmenting_edge;
         } else {
            curr_aug_path->flow -= flow_increase;
            curr_aug_path = curr_aug_path->to->augmenting_edge;
         }
      }
   }
}

void free_resources(flow_node_t &s, flow_node_t *customer_nodes,
                    flow_node_t *product_nodes)
{
   for (auto &e : s.outbound_edges) {
      delete e;
   }
   for (int i = 0; i < number_of_customers; i++) {
      for (auto &e : customer_nodes[i].outbound_edges) {
         delete e;
      }
   }
   for (int i = 0; i < number_of_products; i++) {
      for (auto &e : product_nodes[i].outbound_edges) {
         delete e;
      }
   }
}