#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(drawmate, m)
{
    py::class_<LayoutConfig>(m, "LayoutConfig")
        .def(py::init<>())
        .def_readwrite("base_x", &LayoutConfig::base_x)
        .def_readwrite("base_y", &LayoutConfig::base_y)
        .def_readwrite("node_width", &LayoutConfig::node_width)
        .def_readwrite("node_height", &LayoutConfig::node_height)
        .def_readwrite("node_label_height", &LayoutConfig::node_label_height)
        .def_readwrite("port_width", &LayoutConfig::port_width)
        .def_readwrite("port_height", &LayoutConfig::port_height)
        .def_readwrite("node_spacing_x_axis", &LayoutConfig::node_spacing_x_axis)
        .def_readwrite("node_spacing_y_axis", &LayoutConfig::node_spacing_y_axis)
        .def_readwrite("port_spacing", &LayoutConfig::port_spacing);

    py::class_<GridConfig>(m, "GridConfig")
        .def(py::init<>())
        .def_readwrite("num_columns_left", &GridConfig::columns_left)
        .def_readwrite("num_columns_right", &GridConfig::columns_right)
        .def_readwrite("num_rows_left", &GridConfig::rows_left)
        .def_readwrite("num_rows_right", &GridConfig::rows_right);

    py::class_<Graph>(m, "Graph")
        .def(py::init<LayoutConfig, GridConfig>())
        .def("add_node", &Graph::add_node)
        .def("get_nodes", &Graph::get_nodes)
        .def("get_node_ids", &Graph::get_node_ids)
        .def("add_connection", &Graph::add_connection);
}
