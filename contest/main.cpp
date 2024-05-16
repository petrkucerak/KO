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
} edge_t;

void print_graph(vector<vector<edge_t>> &graph);
bool is_cyclic(vector<edge_t> &graph, uint32_t &vertices_count);
bool is_cyclic_util(uint32_t node, vector<bool> &visited,
                    vector<bool> &rec_stack, vector<edge_t> &graph);

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
   vector<vector<edge_t>> graph(DEFAULT_VERTICES_COUNT);
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

   // print_graph(graph);

   /* Write solution */
   FILE *output_p;
   output_p = fopen(OUTPUT_PATH, "w+");

   uint32_t remove_weight = 0;
   fprintf(output_p, "%d\n", remove_weight);

   /* Close output file */
   if (fclose(output_p) != 0) {
      perror("Can't close the output file!");
      exit(EXIT_FAILURE);
   }
   return 0;
}

void print_graph(vector<vector<edge_t>> &graph)
{
   for (uint32_t i = 0; i < graph.size(); ++i) {
      cout << endl << "VERTEX: " << i << endl;
      for (uint32_t j = 0; j < graph[i].size(); ++j) {
         cout << "target: " << graph[i][j].to << ", cost " << graph[i][j].cost
              << endl;
      }
   }
}

bool is_cyclic(vector<edge_t> &graph, uint32_t &vertices_count)
{
   // Mark all the vertices as not visited
   // and not part of recursion stack
   vector<bool> visited(vertices_count, false);
   vector<bool> rec_stack(vertices_count, false);

   // Call the recursive helper function
   // to detect cycle in different DFS trees
   for (uint32_t i = 0; i < vertices_count; ++i) {
      if (!visited[i] && is_cyclic_util(i, visited, rec_stack, graph))
         return true;
   }
   return false;
}

bool is_cyclic_util(uint32_t node, vector<bool> &visited,
                    vector<bool> &rec_stack, vector<edge_t> &graph)
{
   if (visited[node] == false) {
      // Mark the current node as visited
      // and part of recursion stack
      visited[node] = true;
      rec_stack[node] = true;
   }
}