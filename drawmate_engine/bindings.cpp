#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(drawmate, m)
{
    py::class_<LayoutConfig>(m, "LayoutConfig")
        .def(py::init<double, double, double, double, double>(), 
            py::arg("base_x"), py::arg("base_y"), py::arg("node_spacing_x_axis"), py::arg("node_spacing_y_axis"), py::arg("port_spacing")
        )
        .def_readwrite("base_x", &LayoutConfig::base_x)
        .def_readwrite("base_y", &LayoutConfig::base_y)
        .def_readwrite("node_spacing_x_axis", &LayoutConfig::node_spacing_x_axis)
        .def_readwrite("node_spacing_y_axis", &LayoutConfig::node_spacing_y_axis)
        .def_readwrite("port_spacing", &LayoutConfig::port_spacing);

    py::class_<GridConfig>(m, "GridConfig")
        .def(py::init<int, int, int, int>(), py::arg("columns_left"), py::arg("columns_right"), py::arg("rows_left"), py::arg("rows_right")
        )
        .def_readwrite("num_columns_left", &GridConfig::columns_left)
        .def_readwrite("num_columns_right", &GridConfig::columns_right)
        .def_readwrite("num_rows_left", &GridConfig::rows_left)
        .def_readwrite("num_rows_right", &GridConfig::rows_right);

    py::class_<NodeConfig>(m, "NodeConfig")
        .def(py::init<double, double, double>(), py::arg("width"), py::arg("height"), py::arg("label_height"));

    py::class_<CentralNodeConfig>(m, "CentralNodeConfig")
        .def(py::init<double, double, double>(), py::arg("width"), py::arg("height"), py::arg("label_height"));

    py::class_<PortConfig>(m, "PortConfig")
        .def(py::init<double, double>(), py::arg("port_width"), py::arg("port_height"));

    py::class_<LabelExport>(m, "Label")
        .def(py::init<>())
        .def_readonly("name", &LabelExport::name)
        .def_readonly("x", &LabelExport::x)
        .def_readonly("y", &LabelExport::y)
        .def_readonly("width", &LabelExport::width)
        .def_readonly("height", &LabelExport::height);

    py::class_<LinkExport>(m, "Link")
        .def(py::init<>())
        .def_readonly("source_x", &LinkExport::source_x)
        .def_readonly("source_y", &LinkExport::source_y)
        .def_readonly("target_x", &LinkExport::target_x)
        .def_readonly("target_y", &LinkExport::target_y)
        .def_readonly("has_waypoints", &LinkExport::has_waypoints)
        .def_readonly("waypoints", &LinkExport::waypoints);
    
    py::class_<PortExport>(m, "Port")
        .def(py::init<>())
        .def_readonly("name", &PortExport::label)
        .def_readonly("x", &PortExport::x)
        .def_readonly("y", &PortExport::y)
        .def_readonly("width", &PortExport::width)
        .def_readonly("height", &PortExport::height);
    
    py::class_<NodeExport>(m, "Node")
        .def(py::init<>())
        .def_readonly("name", &NodeExport::name)
        .def_readonly("id_", &NodeExport::source_id)
        .def_readonly("x", &NodeExport::x)
        .def_readonly("y", &NodeExport::y)
        .def_readonly("width", &NodeExport::width)
        .def_readonly("height", &NodeExport::height)
        .def_readonly("label", &NodeExport::label)
        .def_readonly("ports_left", &NodeExport::ports_left_)
        .def_readonly("ports_right", &NodeExport::ports_right_);

    py::class_<Graph>(m, "Graph")
        .def(py::init<LayoutConfig, GridConfig, CentralNodeConfig, NodeConfig, PortConfig>())
        .def("add_node", &Graph::add_node)
        // .def("debug_print_node_data", &Graph::debug_print_node_data)
        .def("get_nodes", &Graph::get_nodes)
        .def("get_node_ids", &Graph::get_node_ids)
        .def("get_node_ids_left", &Graph::get_node_ids_left)
        .def("get_node_ids_right", &Graph::get_node_ids_right)
        .def("connect_nodes", &Graph::connect_nodes)
        .def("get_links", &Graph::get_links);
}
