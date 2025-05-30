cmake_minimum_required(VERSION 3.10)

project(drawmate_plus
    VERSION 1.1 DESCRIPTION "Backend for drawmate"
)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_INSTALL_RPATH "$ORIGIN")
set(CMAKE_BUILD_RPATH "$ORIGIN")
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_MACOSX_RPATH ON)


add_library(drawmate_lib SHARED
        src/graph_object.cpp
        src/graph.cpp
        src/link.cpp
        src/keys.cpp
        src/node.cpp
        src/port.cpp
)

target_include_directories(drawmate_lib PUBLIC include)

set(PYBIND11_FINDPYTHON ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(drawmate_engine bindings.cpp)

if (APPLE)
    set_target_properties(drawmate_lib PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
        MACOSX_RPATH ON
        INSTALL_NAME_DIR "@rpath"
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path"
    )
    set_target_properties(drawmate_engine PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
        MACOSX_RPATH ON
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path"
    )
endif()

if (LINUX)
    set_target_properties(drawmate_lib PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
        PREFIX ""
        INSTALL_RPATH "$ORIGIN"
        BUILD_RPATH "$ORIGIN"
    )
    set_target_properties(drawmate_engine PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
        PREFIX ""
        INSTALL_RPATH "$ORIGIN"
        BUILD_RPATH "$ORIGIN"
    )
endif()

if (WIN32)
    set_target_properties(drawmate_lib PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
    )
    set_target_properties(drawmate_engine PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/drawmate"
    )
endif()

install(TARGETS drawmate_engine drawmate_lib DESTINATION .)

target_link_libraries(drawmate_engine PUBLIC drawmate_lib)
