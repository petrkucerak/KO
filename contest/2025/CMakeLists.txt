cmake_minimum_required(VERSION 3.10)

# Set project name and language
project(TurkeyBox LANGUAGES CXX)

# Set the C++ standard and compiler flags
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -march=native -pthread")

# Define the root source directory (no subdirectories allowed)
set(ROOT_DIR "${CMAKE_SOURCE_DIR}")

# Gather all .cpp and .h files in ROOT_DIR
file(GLOB SRC_FILES "${ROOT_DIR}/*.cpp" "${ROOT_DIR}/*.h")

# Add executable target
add_executable(TurkeyBox ${SRC_FILES})

# Create a custom target to zip all .cpp and .h files
add_custom_target(zip_sources
   COMMAND ${CMAKE_COMMAND} -E tar cfv "${ROOT_DIR}/kucerp28_cocontest25_cpp.zip" --format=zip ${SRC_FILES}
   WORKING_DIRECTORY ${ROOT_DIR}
   COMMENT "Creating zip archive of all .cpp and .h files in root directory"
)
