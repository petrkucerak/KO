#include "main.h"
#include <ctime>
#include <fstream>
#include <stdexcept>
#include <vector>

using namespace std;

int main(int argc, char const *argv[])
{
   if (argc < 4) {
      throw invalid_argument("Please, specify program input correctly!\n"
                             "Right input is: ./program_name <input_path> "
                             "<output_path> <time_limit>");
   }
   double time_limit = stod(argv[3]);
   if (time_limit <= 0) {
      throw invalid_argument("Time limit must be positive");
   }

   ifstream input(argv[1]);
   if (!input.is_open()) {
      throw invalid_argument("Cannot open input file");
   }

   uint32_t locker_count, customer_count;
   input >> locker_count >> customer_count;
   if (locker_count == 0 || customer_count == 0) {
      throw invalid_argument(
          "Locker count and customer count must be positive");
   }

   vector<uint32_t> items_counts(customer_count);
   for (vector<uint32_t>::iterator count = items_counts.begin();
        count != items_counts.end(); ++count) {
      input >> *count;
      if (*count == 0) {
         throw invalid_argument("Item count must be positive");
      }
   }

   vector<Locker> lockers(locker_count);
   for (vector<Locker>::iterator size = lockers.begin(); size != lockers.end();
        ++size) {
      input >> size->width >> size->height;
      if (size->width == 0 || size->height == 0) {
         throw invalid_argument("Locker dimensions must be positive");
      }
   }

   vector<OrderList> order_list;
   order_list.reserve(customer_count);
   for (uint32_t i = 0; i < customer_count; ++i) {
      OrderList list(items_counts[i]);
      input >> list.bonus;
      for (vector<Order>::iterator order = list.orders.begin();
           order != list.orders.end(); ++order) {
         input >> order->payment >> order->width >> order->height;
         if (order->width == 0 || order->height == 0) {
            throw invalid_argument("Item dimensions must be positive");
         }
      }
      order_list.push_back(list);
   }
   input.close();

   Solver solver(order_list, lockers);
   solver.solve(time_limit);
   order_list = solver.order_list;

   ofstream output(argv[2]);
   if (!output.is_open()) {
      throw invalid_argument("Cannot open output file");
   }
   output << solver.objective << endl;
   OrderList::print_list(order_list, output);
   output.close();

   cout << "The computing is done. See algorithm results in " << argv[2]
        << endl;
   return 0;
}

bool Locker::put_order(Order &order, uint32_t locker_idx)
{
   if (customer_id != 0 && customer_id != order.customer_id) {
      return false;
   }

   for (uint32_t r = 0; r <= 1; ++r) {
      uint32_t item_width = (r == 0) ? order.width : order.height;
      uint32_t item_height = (r == 0) ? order.height : order.width;

      uint32_t best_x = 0, best_y = UINT32_MAX;
      bool can_place = false;

      for (uint32_t x = 0; x + item_width <= width; ++x) {
         uint32_t max_height = 0;
         for (vector<pair<uint32_t, uint32_t>>::const_iterator segment =
                  skyline.begin();
              segment != skyline.end(); ++segment) {
            if (segment->first >= x && segment->first < x + item_width) {
               max_height = max(max_height, segment->second);
            }
         }

         if (max_height + item_height <= height) {
            bool overlap = false;
            for (vector<pair<uint32_t, uint32_t>>::const_iterator segment =
                     skyline.begin();
                 segment != skyline.end(); ++segment) {
               if (segment->first >= x && segment->first < x + item_width &&
                   segment->second > max_height) {
                  overlap = true;
                  break;
               }
            }
            if (!overlap && max_height < best_y) {
               best_y = max_height;
               best_x = x;
               can_place = true;
            }
         }
      }

      if (can_place) {
         order.locker_id = locker_idx + 1;
         order.x = best_x;
         order.y = best_y;
         order.rotated = r;

         vector<pair<uint32_t, uint32_t>> new_skyline;
         for (vector<pair<uint32_t, uint32_t>>::iterator s = skyline.begin();
              s != skyline.end(); ++s) {
            if (s->first < best_x || s->first >= best_x + item_width) {
               new_skyline.push_back(*s);
            }
         }

         new_skyline.push_back(make_pair(best_x, best_y + item_height));
         for (uint32_t x = best_x + 1; x < best_x + item_width; ++x) {
            new_skyline.push_back(make_pair(x, best_y + item_height));
         }
         sort(new_skyline.begin(), new_skyline.end());
         skyline = new_skyline;

         customer_id = order.customer_id;
         return true;
      }
   }
   return false;
}

void Solver::solve(double time_limit)
{
   clock_t start_time = clock();
   double elapsed_time = 0.0;

   uint64_t best_objective = 0;
   vector<OrderList> best_order_list = order_list;
   vector<Locker> best_lockers = lockers;

   srand(time(NULL));

   while (elapsed_time < time_limit * 0.8) {
      objective = 0;
      order_list = best_order_list;
      lockers = best_lockers;

      for (vector<Locker>::iterator locker = lockers.begin();
           locker != lockers.end(); ++locker) {
         locker->skyline.clear();
         locker->skyline.reserve(locker->width);
         for (uint32_t x = 0; x < locker->width; ++x) {
            locker->skyline.push_back(make_pair(x, 0));
         }
         locker->customer_id = 0;
      }

      vector<pair<uint32_t, double>> customer_priority;
      for (uint32_t i = 0; i < order_list.size(); ++i) {
         uint64_t total_area = 0;
         uint64_t total_payment = order_list[i].bonus;
         for (vector<Order>::const_iterator order =
                  order_list[i].orders.begin();
              order != order_list[i].orders.end(); ++order) {
            total_area += order->width * order->height;
            total_payment += order->payment;
         }
         double density = total_area > 0
                              ? static_cast<double>(total_payment) / total_area
                              : 0.0;
         customer_priority.push_back(make_pair(i, density));
      }
      sort(customer_priority.begin(), customer_priority.end(),
           [](const pair<uint32_t, double> &a,
              const pair<uint32_t, double> &b) { return a.second > b.second; });
      random_shuffle(customer_priority.begin(),
                     customer_priority.end()); // C++11 random_shuffle

      for (vector<pair<uint32_t, double>>::const_iterator cp =
               customer_priority.begin();
           cp != customer_priority.end(); ++cp) {
         uint32_t customer_idx = cp->first + 1;
         vector<Order> &orders = order_list[cp->first].orders;

         vector<pair<uint32_t, double>> order_priority;
         for (uint32_t j = 0; j < orders.size(); ++j) {
            double area = orders[j].width * orders[j].height;
            double density =
                area > 0 ? static_cast<double>(orders[j].payment) / area : 0.0;
            order_priority.push_back(make_pair(j, density));
         }
         sort(order_priority.begin(), order_priority.end(),
              [](const pair<uint32_t, double> &a,
                 const pair<uint32_t, double> &b) {
                 return a.second > b.second;
              });

         bool all_assigned = true;
         for (vector<pair<uint32_t, double>>::const_iterator op =
                  order_priority.begin();
              op != order_priority.end(); ++op) {
            uint32_t order_idx = op->first;
            Order &order = orders[order_idx];
            order.customer_id = customer_idx;

            bool placed = false;
            for (uint32_t m = 0; m < lockers.size(); ++m) {
               if (lockers[m].put_order(order, m)) {
                  objective += order.payment;
                  placed = true;
                  break;
               }
            }
            if (!placed) {
               all_assigned = false;
               order.locker_id = 0;
               order.x = 0;
               order.y = 0;
               order.rotated = 0;
            }
         }

         if (all_assigned) {
            objective += order_list[cp->first].bonus;
         }
      }

      if (objective > best_objective) {
         best_objective = objective;
         best_order_list = order_list;
         best_lockers = lockers;
      }

      elapsed_time = static_cast<double>(clock() - start_time) / CLOCKS_PER_SEC;
   }

   objective = best_objective;
   order_list = best_order_list;
   lockers = best_lockers;
}

// Lockers M
// - parameters
// Customers N
// - bonus pay
// - list of items
//   - price
//   - parameters