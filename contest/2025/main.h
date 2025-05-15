#ifndef __MAIN_H
#define __MAIN_H

#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

using namespace std;

class Size
{
   public:
   uint32_t width;
   uint32_t height;

   Size() : width(0), height(0) {}
   Size(uint32_t width, uint32_t height) : width(width), height(height) {}
};

class Order : public Size
{
   public:
   uint32_t payment;
   uint32_t customer_id; // 1-based customer index
   uint32_t locker_id;
   uint32_t x;
   uint32_t y;
   uint32_t rotated;

   Order()
       : Size(), payment(0), customer_id(0), locker_id(0), x(0), y(0),
         rotated(0)
   {
   }
   Order(uint32_t payment, uint32_t width, uint32_t height)
       : Size(width, height), payment(payment), customer_id(0), locker_id(0),
         x(0), y(0), rotated(0)
   {
   }
};

class OrderList
{
   public:
   uint32_t bonus;
   vector<Order> orders;

   OrderList(uint32_t items_count) : bonus(0), orders(items_count) {}

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

class Locker : public Size
{
   public:
   uint32_t customer_id; // 0 if unassigned, else customer index + 1
   vector<pair<uint32_t, uint32_t>> skyline; // (x, height)

   Locker() : Size(), customer_id(0), skyline() {}
   Locker(uint32_t width, uint32_t height)
       : Size(width, height), customer_id(0), skyline()
   {
      skyline.reserve(width);
      for (uint32_t x = 0; x < width; ++x) {
         skyline.push_back(make_pair(x, 0));
      }
   }

   bool put_order(Order &order, uint32_t locker_idx);
};

class Solver
{
   public:
   uint64_t objective;
   vector<OrderList> order_list;
   vector<Locker> lockers;

   Solver(vector<OrderList> &orders, vector<Locker> &l)
       : objective(0), order_list(orders), lockers(l)
   {
   }

   void solve(double time_limit);
};

#endif /* __MAIN_H */