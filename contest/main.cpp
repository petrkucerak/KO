#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

#define INPUT_PATH argv[1]
#define OUTPUT_PATH argv[2]
#define DEFAULT_VERTICES_COUNT 10

using namespace std;

typedef struct {
   uint32_t to;
   uint32_t cost;
} target_t;

typedef struct {
   uint32_t from;
   uint32_t to;
} edge_t;

void print_graph(vector<vector<target_t>> &graph);

/**
 * @brief Main function if graph is cycle, return true. Algorithm uses DFS and
 * is implemented by: https://www.geeksforgeeks.org/detect-cycle-in-a-graph/.
 *
 * @param graph
 * @return true
 * @return false
 */
bool is_cyclic(vector<vector<target_t>> &graph);

/**
 * @brief Util function to find cycle in graph.
 *
 * @param vertex
 * @param visited
 * @param rec_stack
 * @param graph
 * @return true
 * @return false
 */
bool is_cyclic_util(uint32_t vertex, vector<bool> &visited,
                    vector<bool> &rec_stack, vector<vector<target_t>> &graph);

uint32_t get_best_solution(vector<vector<target_t>> &graph,
                           vector<edge_t> &removed_edges, uint32_t best_cost,
                           uint32_t depth);

int main(int argc, char const *argv[])
{
   /* Parse arguments */
   if (argc < 4) {
      perror("Wrong number of arguments.");
      exit(EXIT_FAILURE);
   }
   /* Get time limit as a float */
   const float time_limit = stof(argv[3]);

   /* Load data */
   FILE *input_p;
   input_p = fopen(INPUT_PATH, "r");
   if (input_p == NULL) {
      perror("Can't open the input file");
      exit(EXIT_FAILURE);
   }
   /* Load edges count */
   uint32_t edges_count;
   if (fscanf(input_p, "%d", &edges_count) != 1) {
      perror("Can't correctly load count of edges!");
      exit(EXIT_FAILURE);
   }
   /* Load graph */
   vector<vector<target_t>> graph(DEFAULT_VERTICES_COUNT);
   uint32_t vertices_count = 0;
   for (uint32_t i = 0; i < edges_count; ++i) {
      uint32_t from, to, cost;
      if (fscanf(input_p, "%d %d %d", &from, &to, &cost) != 3) {
         perror("Can't correctly load graph edges!");
         exit(EXIT_FAILURE);
      }
      /* Get count of vertices */
      if (from > vertices_count)
         vertices_count = from;
      if (to > vertices_count)
         vertices_count = to;
      /* Resize graph is it necessary */
      if (graph.size() < vertices_count)
         graph.resize(graph.size() * 2);
      /* Push edge */
      graph[from - 1].push_back({to - 1, cost});
   }
   graph.resize(vertices_count);
   /* Close input file */
   if (fclose(input_p) != 0) {
      perror("Can't close the input file!");
      exit(EXIT_FAILURE);
   }

   // if (is_cyclic(graph))
   //    cout << "The graph is cyclic!" << endl;
   // else
   //    cout << "The graph is not cyclic!" << endl;

   /* Iterate on all edges */
   uint32_t removed_cost = UINT32_MAX;
   vector<edge_t> removed_edges;
   removed_cost = get_best_solution(graph, removed_edges, removed_cost, 0);
   if (!removed_cost) {
      perror("Map does not contains Penrose stairs!");
      exit(EXIT_FAILURE);
   }

   /* Print the best solution */
   cout << "Objective " << removed_cost << endl;
   for (uint32_t line = 0; line < removed_edges.size(); ++line) {
      printf("%d %d\n", removed_edges[line].from + 1,
             removed_edges[line].to + 1);
   }

   /* Write solution */
   FILE *output_p;
   output_p = fopen(OUTPUT_PATH, "w+");

   fprintf(output_p, "%d\n", removed_cost);
   for (uint32_t line = 0; line < removed_edges.size(); ++line) {
      fprintf(output_p, "%d %d\n", removed_edges[line].from + 1,
              removed_edges[line].to + 1);
   }

   /* Close output file */
   if (fclose(output_p) != 0) {
      perror("Can't close the output file!");
      exit(EXIT_FAILURE);
   }
   return 0;
}

void print_graph(vector<vector<target_t>> &graph)
{
   cout << " ------------------- " << endl;
   for (uint32_t i = 0; i < graph.size(); ++i) {
      cout << "VERTEX: " << i << endl;
      for (uint32_t j = 0; j < graph[i].size(); ++j) {
         cout << "target: " << graph[i][j].to << ", cost " << graph[i][j].cost
              << endl;
      }
   }
}

bool is_cyclic(vector<vector<target_t>> &graph)
{
   // Mark all the vertices as not visited and not part of recursion stack
   vector<bool> visited(graph.size(), false);
   vector<bool> rec_stack(graph.size(), false);

   // Call the recursive helper function to detect cycle in different DFS trees
   for (uint32_t i = 0; i < graph.size(); ++i) {
      if (!visited[i] && is_cyclic_util(i, visited, rec_stack, graph))
         return true;
   }
   return false;
}

bool is_cyclic_util(uint32_t vertex, vector<bool> &visited,
                    vector<bool> &rec_stack, vector<vector<target_t>> &graph)
{
   if (visited[vertex] == false) {
      // Mark the current vertex as visited and part of recursion stack
      visited[vertex] = true;
      rec_stack[vertex] = true;
      // Recur for all the vertices adjacent to this vertex
      for (uint32_t i = 0; i < graph[vertex].size(); ++i) {
         if (!visited[graph[vertex][i].to] &&
             is_cyclic_util(graph[vertex][i].to, visited, rec_stack, graph))
            return true;
         else if (rec_stack[graph[vertex][i].to])
            return true;
      }
   }
   // Remove the vertex from recursion stack
   rec_stack[vertex] = false;
   return false;
}

uint32_t get_best_solution(vector<vector<target_t>> &graph,
                           vector<edge_t> &removed_edges, uint32_t best_cost,
                           uint32_t depth)
{
   for (uint32_t vertex = 0; vertex < graph.size(); ++vertex) {
      for (uint32_t edge = 0; edge < graph[vertex].size(); ++edge) {

         /* If the edge cost is higher then the best found cost, skip it */
         if (graph[vertex][edge].cost >= best_cost)
            continue;

         /* Remove edge */
         target_t tmp;
         tmp.cost = graph[vertex][edge].cost;
         tmp.to = graph[vertex][edge].to;
         graph[vertex].erase(graph[vertex].begin() + edge);

         uint32_t cost = tmp.cost;
         /* Check cycle */
         if (is_cyclic(graph))
            cost =
                +get_best_solution(graph, removed_edges, best_cost, depth + 1);

         if (cost < best_cost) {
            /* Update new cost */
            best_cost = cost;

            /* Remove last added edge */
            if (removed_edges.size() > depth)
               removed_edges.pop_back();

            /* Push new edge */
            removed_edges.push_back({vertex, tmp.to});
         }

         /* Add remove edge */
         graph[vertex].insert(graph[vertex].begin() + edge, tmp);
      }
   }
   return best_cost;
}
