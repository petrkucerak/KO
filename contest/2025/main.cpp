
#include "main.h"
#include <ctime>
#include <fstream>
#include <stdexcept>
#include <vector>

using namespace std;

/**
 * @brief Main entry point for the TurkeyBox solver.
 *
 * Reads input data, initializes the solver, computes the optimal placement of
 * items in lockers, and writes the results to the output file.
 *
 * @param argc Number of command-line arguments.
 * @param argv Array of command-line arguments: [program_name, input_path,
 * output_path, time_limit].
 * @return 0 on successful execution.
 */
int main(int argc, char const *argv[])
{
   // Check if the correct number of arguments is provided
   if (argc < 4) {
      throw invalid_argument("Please, specify program input correctly!\n"
                             "Right input is: ./program_name <input_path> "
                             "<output_path> <time_limit>");
   }

   // Parse and validate the time limit
   double time_limit = stod(argv[3]);
   if (time_limit <= 0) {
      throw invalid_argument("Time limit must be positive");
   }

   // Open the input file
   ifstream input(argv[1]);
   if (!input.is_open()) {
      throw invalid_argument("Cannot open input file");
   }

   // Read the number of lockers and customers
   uint32_t locker_count, customer_count;
   input >> locker_count >> customer_count;
   if (locker_count == 0 || customer_count == 0) {
      throw invalid_argument(
          "Locker count and customer count must be positive");
   }

   // Read the number of items for each customer
   vector<uint32_t> items_counts(customer_count);
   for (vector<uint32_t>::iterator count = items_counts.begin();
        count != items_counts.end(); ++count) {
      input >> *count;
      if (*count == 0) {
         throw invalid_argument("Item count must be positive");
      }
   }

   // Initialize lockers with their dimensions
   vector<Locker> lockers(locker_count);
   for (vector<Locker>::iterator size = lockers.begin(); size != lockers.end();
        ++size) {
      input >> size->width >> size->height;
      if (size->width == 0 || size->height == 0) {
         throw invalid_argument("Locker dimensions must be positive");
      }
   }

   // Initialize the list of customer orders
   vector<OrderList> order_list;
   order_list.reserve(customer_count);
   for (uint32_t i = 0; i < customer_count; ++i) {
      // Create an OrderList for the customer with the specified number of items
      OrderList list(items_counts[i]);
      input >> list.bonus; // Read the customer's bonus

      // Read payment and dimensions for each item
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

   // Initialize and run the solver
   Solver solver(order_list, lockers);
   solver.solve(time_limit);
   order_list =
       solver.order_list; // Update order_list with the solved placements

   // Open the output file
   ofstream output(argv[2]);
   if (!output.is_open()) {
      throw invalid_argument("Cannot open output file");
   }

   // Write the objective value and item placements to the output file
   output << solver.objective << endl;
   OrderList::print_list(order_list, output);
   output.close();

   // Notify the user of completion
   cout << "The computing is done. See algorithm results in " << argv[2]
        << endl;
   return 0;
}

/**
 * @brief Attempts to place an item in the locker.
 *
 * Checks if the item can be placed without overlapping other items, respecting
 * the single-customer constraint and locker dimensions. Tries both rotations
 * (0 and 90 degrees) and updates the skyline if successful.
 *
 * @param order The item to place (modified if placed successfully).
 * @param locker_idx 0-based index of the locker.
 * @return true if the item was placed, false otherwise.
 */
bool Locker::put_order(Order &order, uint32_t locker_idx)
{
   // Ensure the locker is either empty or assigned to the same customer
   if (customer_id != 0 && customer_id != order.customer_id) {
      return false;
   }

   // Try both rotations (0: no rotation, 1: 90-degree rotation)
   for (uint32_t r = 0; r <= 1; ++r) {
      uint32_t item_width = (r == 0) ? order.width : order.height;
      uint32_t item_height = (r == 0) ? order.height : order.width;

      uint32_t best_x = 0, best_y = UINT32_MAX;
      bool can_place = false;

      // Try placing the item at each possible x-coordinate
      for (uint32_t x = 0; x + item_width <= width; ++x) {
         uint32_t max_height = 0;
         // Find the maximum height in the skyline over [x, x + item_width]
         for (vector<pair<uint32_t, uint32_t>>::const_iterator segment =
                  skyline.begin();
              segment != skyline.end(); ++segment) {
            if (segment->first >= x && segment->first < x + item_width) {
               max_height = max(max_height, segment->second);
            }
         }

         // Check if the item fits vertically
         if (max_height + item_height <= height) {
            // Verify no overlap by simulating placement
            bool overlap = false;
            for (vector<pair<uint32_t, uint32_t>>::const_iterator segment =
                     skyline.begin();
                 segment != skyline.end(); ++segment) {
               // Check if any skyline point in the x-range is above max_height
               if (segment->first >= x && segment->first < x + item_width &&
                   segment->second > max_height) {
                  overlap = true;
                  break;
               }
            }

            // Additional check to ensure no existing item extends into the area
            if (!overlap) {
               for (uint32_t check_x = x; check_x < x + item_width; ++check_x) {
                  for (vector<pair<uint32_t, uint32_t>>::const_iterator
                           segment = skyline.begin();
                       segment != skyline.end(); ++segment) {
                     if (segment->first == check_x &&
                         segment->second > max_height) {
                        overlap = true;
                        break;
                     }
                  }
                  if (overlap)
                     break;
               }
            }

            // If no overlap and this y is better, update the best position
            if (!overlap && max_height < best_y) {
               best_y = max_height;
               best_x = x;
               can_place = true;
            }
         }
      }

      // If a valid placement was found, update the item and skyline
      if (can_place) {
         order.locker_id = locker_idx + 1;
         order.x = best_x;
         order.y = best_y;
         order.rotated = r;

         // Update the skyline to reflect the new item
         vector<pair<uint32_t, uint32_t>> new_skyline;
         for (uint32_t x = 0; x < width; ++x) {
            uint32_t height = 0;
            if (x >= best_x && x < best_x + item_width) {
               height = best_y + item_height; // Set height for the new item
            } else {
               // Copy existing skyline height
               for (vector<pair<uint32_t, uint32_t>>::const_iterator s =
                        skyline.begin();
                    s != skyline.end(); ++s) {
                  if (s->first == x) {
                     height = max(height, s->second);
                     break;
                  }
               }
            }
            new_skyline.push_back(make_pair(x, height));
         }
         skyline = new_skyline;

         // Assign the customer to the locker
         customer_id = order.customer_id;
         return true;
      }
   }
   // No valid placement found
   return false;
}

/**
 * @brief Solves the TurkeyBox problem.
 *
 * Iteratively places items in lockers using a heuristic based on profit density
 * and randomization. Aims to maximize the objective (sum of payments and
 * bonuses) within the given time limit. Keeps track of the best solution found.
 *
 * @param time_limit Maximum time (in seconds) allowed for solving.
 */
void Solver::solve(double time_limit)
{
   // Initialize timing and best solution tracking
   clock_t start_time = clock();
   double elapsed_time = 0.0;

   uint64_t best_objective = 0;
   vector<OrderList> best_order_list = order_list;
   vector<Locker> best_lockers = lockers;

   // Seed the random number generator
   srand(time(NULL));

   uint32_t iteration = 0;
   // Run iterations until 80% of the time limit is reached
   while (elapsed_time < time_limit * 0.8) {
      // Reset the objective and restore the best known state
      objective = 0;
      order_list = best_order_list;
      lockers = best_lockers;

      // Reset all lockers
      for (vector<Locker>::iterator locker = lockers.begin();
           locker != lockers.end(); ++locker) {
         locker->skyline.clear();
         locker->skyline.reserve(locker->width);
         for (uint32_t x = 0; x < locker->width; ++x) {
            locker->skyline.push_back(make_pair(x, 0));
         }
         locker->customer_id = 0;
      }

      // Prioritize customers based on profit density
      vector<pair<uint32_t, double>> customer_priority;
      for (uint32_t i = 0; i < order_list.size(); ++i) {
         uint64_t total_area = 0;
         uint64_t total_payment = order_list[i].bonus;
         // Calculate total area and payment for the customer
         for (vector<Order>::const_iterator order =
                  order_list[i].orders.begin();
              order != order_list[i].orders.end(); ++order) {
            total_area += order->width * order->height;
            total_payment += order->payment;
         }
         // Compute density as payment per unit area
         double density = total_area > 0
                              ? static_cast<double>(total_payment) / total_area
                              : 0.0;
         customer_priority.push_back(make_pair(i, density));
      }
      // Sort customers by density (descending) and shuffle for randomization
      sort(customer_priority.begin(), customer_priority.end(),
           [](const pair<uint32_t, double> &a,
              const pair<uint32_t, double> &b) { return a.second > b.second; });
      random_shuffle(customer_priority.begin(), customer_priority.end());

#ifdef DEBUG
      uint32_t items_placed = 0;
#endif // DEBUG

      // Process each customer
      for (vector<pair<uint32_t, double>>::const_iterator cp =
               customer_priority.begin();
           cp != customer_priority.end(); ++cp) {
         uint32_t customer_idx = cp->first + 1;
         vector<Order> &orders = order_list[cp->first].orders;

         // Prioritize items based on profit density
         vector<pair<uint32_t, double>> order_priority;
         for (uint32_t j = 0; j < orders.size(); ++j) {
            double area = orders[j].width * orders[j].height;
            double density =
                area > 0 ? static_cast<double>(orders[j].payment) / area : 0.0;
            order_priority.push_back(make_pair(j, density));
         }

         // Sort items by density (descending)
         sort(order_priority.begin(), order_priority.end(),
              [](const pair<uint32_t, double> &a,
                 const pair<uint32_t, double> &b) {
                 return a.second > b.second;
              });

         // Track if all items for the customer are assigned
         bool all_assigned = true;
         // Try to place each item
         for (vector<pair<uint32_t, double>>::const_iterator op =
                  order_priority.begin();
              op != order_priority.end(); ++op) {
            uint32_t order_idx = op->first;
            Order &order = orders[order_idx];
            order.customer_id = customer_idx;

            bool placed = false;
            // Try each locker
            for (uint32_t m = 0; m < lockers.size(); ++m) {
               if (lockers[m].put_order(order, m)) {
                  // Validate locker assignment
                  if (order.locker_id > 0 &&
                      order.locker_id <= lockers.size()) {
                     objective += order.payment;
                     placed = true;
#ifdef DEBUG
                     items_placed++;
#endif // DEBUG
                  } else {
                     // Invalid assignment, reset item
                     order.locker_id = 0;
                     order.x = 0;
                     order.y = 0;
                     order.rotated = 0;
                  }
                  break;
               }
            }
            // If not placed, mark as unassigned
            if (!placed) {
               all_assigned = false;
               order.locker_id = 0;
               order.x = 0;
               order.y = 0;
               order.rotated = 0;
            }
         }

         // Award bonus if all items are assigned
         if (all_assigned) {
            bool valid = true;
            for (vector<Order>::const_iterator order = orders.begin();
                 order != orders.end(); ++order) {
               if (order->locker_id == 0) {
                  valid = false;
                  break;
               }
            }
            if (valid) {
               objective += order_list[cp->first].bonus;
            }
         }
      }

      // Update the best solution if this one is better
      if (objective > best_objective) {
         best_objective = objective;
         best_order_list = order_list;
         best_lockers = lockers;
#ifdef DEBUG
         cout << "Iteration " << iteration << ": Objective = " << objective
              << ", Items placed = " << items_placed << endl;
#endif // DEBUG
      }

      // Update elapsed time
      elapsed_time = static_cast<double>(clock() - start_time) / CLOCKS_PER_SEC;
      iteration++;
   }

   // Set the final solution to the best found
   objective = best_objective;
   order_list = best_order_list;
   lockers = best_lockers;
}