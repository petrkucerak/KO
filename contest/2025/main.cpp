#include <cinttypes>
#include <fstream>
#include <iostream>
#include <stdexcept>

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
   string tmp;
   ifstream input(argv[1]);
   uint32_t locker_count, customer_count;
   input >> locker_count >> customer_count;
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

class Parameters
{
   public:
   uint32_t width;
   uint32_t height;
   Parameters() : width(0), height(0) {} // Default constructor
   Parameters(uint32_t width, uint32_t height)
   {
      this->height = height;
      this->width = width;
   }
};

class Locker
{
   public:
   Parameters size;
   Parameters occupancy;

   Locker(uint32_t width, uint32_t height)
   {
      this->size.width = width;
      this->size.height = height;
      this->occupancy.width = 0;
      this->occupancy.height = 0;
   }

   void addItem(Parameters item_size) {}
};
