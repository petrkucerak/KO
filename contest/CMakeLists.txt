cmake_minimum_required(VERSION 3.16)
project(cocontest)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}-std=c++14 -pipe -Wall -O3 -fsanitize=address,undefined")

add_executable(main main.cpp)