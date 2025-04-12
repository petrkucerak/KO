#ifndef __MAIN_H
#define __MAIN_H

#include <cinttypes>
#include <iostream>
#include <vector>

using namespace std;

class Size
{
   public:
   uint32_t width;
   uint32_t height;

   Size() : width(0), height(0) {};
   Size(uint32_t width, uint32_t height) : width(width), height(height) {};
};

class Locker : public Size
{
   public:
   uint32_t customer_id;
   /* List of (customer_idx, items_idx) assigned */
   vector<pair<uint32_t, uint32_t>> items;

   Locker() : Size(), customer_id(0) {};
   Locker(uint32_t width, uint32_t height)
       : Size(width, height), customer_id(0) {};
};

class Order : public Size
{
   public:
   uint32_t payment;
   uint32_t locker_id;
   uint32_t x;
   uint32_t y;
   uint32_t rotated;

   Order() : Size(), payment(0), locker_id(0), x(0), y(0), rotated(0) {};
   Order(uint32_t payment, uint32_t width, uint32_t height)
       : Size(width, height), payment(payment), locker_id(0), x(0), y(0),
         rotated(0) {};
};

class OrderList
{
   public:
   uint32_t bonus;
   vector<Order> orders;

   OrderList(uint32_t items_count) : bonus(0), orders(items_count) {};

   static void print_list(vector<OrderList> &order_list, ostream &target)
   {
      for (auto &customer : order_list) {
         for (auto &order : customer.orders) {
            // print in format `π x y r`, where
            // π ... locker_id
            // x ... x position in a box
            // y ... y position in a box
            // r ... rotated
            target << order.locker_id << " " << order.x << " " << order.y << " "
                   << order.rotated << endl;
         }
      }
   };
};

#endif /* __MAIN_H */