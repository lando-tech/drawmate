cmake_minimum_required(VERSION 3.5)

project(drawmate_plus
    VERSION 1.0 DESCRIPTION "Backend for drawmate"
)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(drawmate_lib SHARED
        src/graph_object.cpp
        src/graph.cpp
        src/link.cpp
        src/keys.cpp
        src/node.cpp
        src/port.cpp
        include/graph_config.h
        include/graph_exports.h
        include/graph_object.h
        include/link.h
        include/keys.h
        include/node.h
        include/port.h
        include/graph.h)

target_include_directories(drawmate_lib PUBLIC include)

set(PYBIND11_FINDPYTHON ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(drawmate bindings.cpp)

# set_target_properties(drawmate PROPERTIES
#   INSTALL_RPATH "$ORIGIN"
#   BUILD_WITH_INSTALL_RPATH TRUE
# )

install(TARGETS drawmate DESTINATION .)

target_link_libraries(drawmate PUBLIC drawmate_lib)

# add_custom_command(TARGET drawmate POST_BUILD
#     COMMAND ${CMAKE_COMMAND} -E copy
#       $<TARGET_FILE:drawmate_lib>
#       $<TARGET_FILE:drawmate>
#  )
