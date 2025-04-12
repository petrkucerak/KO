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
   uint32_t customer;

   Locker() : Size(), customer(0) {};
   Locker(uint32_t width, uint32_t height) : Size(width, height) {};
};

class Order : public Size
{
   public:
   uint32_t payment;

   Order() : Size(), payment(0) {}
   Order(uint32_t payment, uint32_t width, uint32_t height)
       : Size(width, height), payment(payment) {};
};

class OrderList
{
   public:
   uint32_t bonus;
   vector<Order> orders;

   OrderList(uint32_t items_count) : bonus(0), orders(items_count) {};

   void print()
   {
      cout << "BONUS: " << bonus << " ";
      for (auto order : orders) {
         cout << "p: " << order.payment << " [w: " << order.width
              << "; h: " << order.height << "]" << endl;
      }
   };

   static void print_list(vector<OrderList> order_list)
   {
      for (auto order : order_list) {
         cout << endl;
         order.print();
      }
   };
};

#endif /* __MAIN_H */