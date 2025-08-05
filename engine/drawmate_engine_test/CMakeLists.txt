cmake_minimum_required(VERSION 3.16)

project(drawmate_engine
    VERSION 1.0.0
    DESCRIPTION "drawmate Graph Engine - A C++ library for graph layout and visualization"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_EXTENSIONS OFF)


add_library(drawmate_engine_lib SHARED
    src/drawmate_graph.cpp
)

include_directories(drawmate_engine PUBLIC include)

add_executable(drawmate_engine src/main.cpp)
target_link_libraries(drawmate_engine PUBLIC drawmate_engine_lib)
