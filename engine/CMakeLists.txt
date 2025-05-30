cmake_minimum_required(VERSION 3.5)

project(drawmate_plus
    VERSION 1.1 DESCRIPTION "Backend for drawmate"
)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_INSTALL_RPATH "$ORIGIN")
set(CMAKE_BUILD_RPATH "$ORIGIN")
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)


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

pybind11_add_module(drawmate_engine bindings.cpp)

# set_target_properties(drawmate_lib PROPERTIES
#     LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
# )

set_target_properties(drawmate_engine PROPERTIES
    # LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
    PREFIX ""
    BUILD_RPATH "$ORIGIN"
    INSTALL_RPATH "$ORIGIN"
    MACOSX_RPATH ON
)

install(TARGETS drawmate_engine DESTINATION .)

target_link_libraries(drawmate_engine PUBLIC drawmate_lib)
