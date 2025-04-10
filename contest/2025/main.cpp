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
   if (argc < 3) {
      throw invalid_argument("\
         Please, specify program input correctly!\n\
         Right input is: ./program_name <input_path> <output_path>\
      ");
   }

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
   vector<Size> locker_sizes(locker_count);
   for (auto &size : locker_sizes) {
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

   // Save data
   ofstream output(argv[2]);
   output << "This is the output file" << endl;
   output.close();

   cout << "Hello world" << endl;
   return 0;
}

// Lockers M
// - parameters
// Customers N
// - bonus pay
// - list of items
//   - price
//   - parameters
