#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

#define INPUT_PATH argv[1]
#define OUTPUT_PATH argv[2]

using namespace std;

typedef struct {
   uint32_t to;
   uint32_t from;
   uint32_t cost;
} edge_t;

void print_graph(vector<edge_t> &graph)
{
   for (auto edge : graph) {
      printf("%d %d %d\n", edge.from, edge.to, edge.cost);
   }
}

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
   vector<edge_t> graph(edges_count);
   for (uint32_t i = 0; i < edges_count; ++i) {
      if (fscanf(input_p, "%d %d %d", &graph[i].from, &graph[i].to,
                 &graph[i].cost) != 3) {
         perror("Can't correctly load graph edges!");
         exit(EXIT_FAILURE);
      }
   }
   /* Close input file */
   if (fclose(input_p) != 0) {
      perror("Can't close the input file!");
      exit(EXIT_FAILURE);
   }

   print_graph(graph);

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
