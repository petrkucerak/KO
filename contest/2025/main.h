/**
 * @file main.h
 * @brief Header file for the TurkeyBox problem solver.
 *
 * Defines classes and structures for representing items, lockers, and the
 * solver for the TurkeyBox optimization problem, where items must be placed in
 * lockers to maximize profit while respecting constraints.
 */
#ifndef __MAIN_H
#define __MAIN_H

#include <cstdint>
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>
// #define DEBUG

using namespace std;

/**
 * @class Size
 * @brief Base class for objects with width and height dimensions.
 *
 * Provides a simple structure for storing and initializing dimensions of items
 * and lockers in the TurkeyBox problem.
 */
class Size
{
   public:
   uint32_t width;  ///< Width of the object.
   uint32_t height; ///< Height of the object.

   /**
    * @brief Default constructor.
    *
    * Initializes width and height to 0.
    */
   Size() : width(0), height(0) {}

   /**
    * @brief Constructor with dimensions.
    *
    * @param width Width of the object.
    * @param height Height of the object.
    */
   Size(uint32_t width, uint32_t height) : width(width), height(height) {}
};

/**
 * @class Order
 * @brief Represents an item to be placed in a locker.
 *
 * Inherits from Size to include width and height. Stores additional properties
 * such as payment, customer ID, locker assignment, position, and rotation.
 */
class Order : public Size
{
   public:
   uint32_t payment;     ///< Payment for placing the item.
   uint32_t customer_id; ///< 1-based index of the customer owning the item.
   uint32_t locker_id;   ///< 1-based index of the locker (0 if unassigned).
   uint32_t x;           ///< x-coordinate of the item's bottom-left corner.
   uint32_t y;           ///< y-coordinate of the item's bottom-left corner.
   uint32_t rotated;     ///< 0 if not rotated, 1 if rotated 90 degrees.

   /**
    * @brief Default constructor.
    *
    * Initializes all fields to 0.
    */
   Order()
       : Size(), payment(0), customer_id(0), locker_id(0), x(0), y(0),
         rotated(0)
   {
   }

   /**
    * @brief Constructor with payment and dimensions.
    *
    * @param payment Payment for placing the item.
    * @param width Width of the item.
    * @param height Height of the item.
    */
   Order(uint32_t payment, uint32_t width, uint32_t height)
       : Size(width, height), payment(payment), customer_id(0), locker_id(0),
         x(0), y(0), rotated(0)
   {
   }
};

/**
 * @class OrderList
 * @brief Represents a list of items belonging to a single customer.
 *
 * Stores the customer's bonus and a vector of their items (Orders).
 */
class OrderList
{
   public:
   uint32_t bonus;       ///< Bonus awarded if all items are placed.
   vector<Order> orders; ///< List of items for the customer.

   /**
    * @brief Constructor.
    *
    * Initializes the bonus to 0 and allocates space for the specified number
    * of items.
    *
    * @param items_count Number of items for the customer.
    */
   OrderList(uint32_t items_count) : bonus(0), orders(items_count) {}

   /**
    * @brief Prints the placement of all items in the order lists.
    *
    * Outputs the locker ID, x, y coordinates, and rotation for each item
    * in the format: "locker_id x y rotated".
    *
    * @param order_list Vector of OrderList objects for all customers.
    * @param target Output stream to write the results to.
    */
   static void print_list(vector<OrderList> &order_list, ostream &target)
   {
      for (vector<OrderList>::iterator customer = order_list.begin();
           customer != order_list.end(); ++customer) {
         for (vector<Order>::iterator order = customer->orders.begin();
              order != customer->orders.end(); ++order) {
            target << order->locker_id << " " << order->x << " " << order->y
                   << " " << order->rotated << endl;
         }
      }
   }
};

/**
 * @class Locker
 * @brief Represents a locker where items can be placed.
 *
 * Inherits from Size to include width and height. Stores the assigned customer
 * and a skyline to track occupied space.
 */
class Locker : public Size
{
   public:
   uint32_t customer_id; ///< 0 if unassigned, else 1-based customer index.
   vector<pair<uint32_t, uint32_t>>
       skyline; ///< Skyline: (x, height) pairs tracking occupied space.

   /**
    * @brief Default constructor.
    *
    * Initializes an empty locker with no dimensions or customer.
    */
   Locker() : Size(), customer_id(0), skyline() {}

   /**
    * @brief Constructor with dimensions.
    *
    * Initializes the locker with the given width and height, and sets up
    * an initial skyline with height 0 for each x-coordinate.
    *
    * @param width Width of the locker.
    * @param height Height of the locker.
    */
   Locker(uint32_t width, uint32_t height)
       : Size(width, height), customer_id(0), skyline()
   {
      skyline.reserve(width);
      for (uint32_t x = 0; x < width; ++x) {
         skyline.push_back(make_pair(x, 0));
      }
   }

   /**
    * @brief Attempts to place an item in the locker.
    *
    * Checks if the item can be placed without overlapping other items,
    * respecting the single-customer constraint and locker dimensions.
    * Tries both rotations (0 and 90 degrees).
    *
    * @param order The item to place (modified if placed successfully).
    * @param locker_idx 0-based index of the locker.
    * @return true if the item was placed, false otherwise.
    */
   bool put_order(Order &order, uint32_t locker_idx);
};

/**
 * @class Solver
 * @brief Solves the TurkeyBox problem by placing items in lockers.
 *
 * Uses a heuristic approach to maximize the objective (sum of payments and
 * bonuses) within a given time limit.
 */
class Solver
{
   public:
   uint64_t objective; ///< Total objective value (payments + bonuses).
   vector<OrderList> order_list; ///< List of all customers' items.
   vector<Locker> lockers;       ///< List of all lockers.

   /**
    * @brief Constructor.
    *
    * Initializes the solver with the given items and lockers.
    *
    * @param orders Vector of OrderList objects for all customers.
    * @param l Vector of Locker objects.
    */
   Solver(vector<OrderList> &orders, vector<Locker> &l)
       : objective(0), order_list(orders), lockers(l)
   {
   }

   /**
    * @brief Solves the TurkeyBox problem.
    *
    * Iteratively places items in lockers using a heuristic based on profit
    * density and randomization, aiming to maximize the objective within
    * the time limit.
    *
    * @param time_limit Maximum time (in seconds) allowed for solving.
    */
   void solve(double time_limit);
};

#endif /* __MAIN_H */