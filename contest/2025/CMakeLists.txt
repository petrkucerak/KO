cmake_minimum_required(VERSION 3.10)

project(TurkeyBox LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -march=native -pthread")

set(ROOT_DIR "${CMAKE_SOURCE_DIR}")

file(GLOB CPP_FILES "${ROOT_DIR}/*.cpp")
file(GLOB H_FILES "${ROOT_DIR}/*.h")

add_executable(TurkeyBox ${CPP_FILES})

add_custom_target(zip_sources
   COMMAND ${CMAKE_COMMAND} -E tar cfv "${ROOT_DIR}/kucerp28_cocontest25_cpp.zip" --format=zip ${CPP_FILES} ${H_FILES}
   WORKING_DIRECTORY ${ROOT_DIR}
   COMMENT "Creating zip archive of all .cpp and .h files in root directory"
)