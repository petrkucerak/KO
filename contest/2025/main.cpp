#include "main.h"
#include <cinttypes>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

using namespace std;

int main(int argc, char const *argv[])
{
   // Parse arguments
   if (argc < 4) {
      throw invalid_argument("\
         Please, specify program input correctly!\n\
         Right input is: ./program_name <input_path> <output_path> <time_limit>\
      ");
   }
   double time_limit = stod(argv[3]);

   // LOAD DATA
   ifstream input(argv[1]);
   // Load metadata
   uint32_t locker_count, customer_count;
   input >> locker_count >> customer_count;
   // Load items_counts
   vector<uint32_t> items_counts(customer_count);
   for (auto &count : items_counts) {
      input >> count;
   }
   // Load locker_sizes
   vector<Locker> lockers(locker_count);
   for (auto &size : lockers) {
      input >> size.width >> size.height;
   }
   // Load customer_orders
   std::vector<OrderList> order_list;
   order_list.reserve(customer_count);

   for (uint32_t i = 0; i < customer_count; ++i) {
      OrderList list(items_counts[i]);
      input >> list.bonus;
      for (auto &order : list.orders) {
         input >> order.payment >> order.width >> order.height;
      }
      order_list.push_back(move(list));
   }
   input.close();

   Solver solver;

   // PRINT DATA RESULTS INTO THE FILE
   ofstream output(argv[2]);
   // Print objective
   output << solver.objective << endl;
   OrderList::print_list(order_list, output);
   output.close();
   cout << "The computing is done. See algorithm results in " << argv[2]
        << endl;
   return 0;
}

// Lockers M
// - parameters
// Customers N
// - bonus pay
// - list of items
//   - price
//   - parameters