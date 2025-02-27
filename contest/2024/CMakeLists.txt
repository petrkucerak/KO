cmake_minimum_required(VERSION 3.16)
project(cocontest)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}-std=c++11 -O2 -march=native -pthread -fopenmp")

add_executable(main main.cpp)