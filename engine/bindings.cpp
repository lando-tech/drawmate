#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(drawmate_engine, m)
{
    py::class_<LayoutConfig>(m, "LayoutConfig",
        R"doc(
        The LayoutConfig class is used to pass base axis parameters and axis spacing to the Graph object.
        )doc"
    )
        .def(py::init<double, double, double, double, double>(), 
            py::arg("base_x"), 
            py::arg("base_y"), 
            py::arg("node_spacing_x_axis"), 
            py::arg("node_spacing_y_axis"), 
            py::arg("port_spacing"),
            R"pbdoc(
            Constructs a LayoutConfig object.
            Args:
                base_x (float): The base x-axis coordinate.
                base_y (float): The base y-axis coordinate.
                node_spacing_x_axis (float): Horizontal spacing between nodes.
                node_spacing_y_axis (float): Vertical spacing between nodes.
                port_spacing (float): Spacing between ports on a node.
            )pbdoc"
        )
        .def_readwrite("base_x", &LayoutConfig::base_x, "The base x-axis coordinate.")
        .def_readwrite("base_y", &LayoutConfig::base_y, "The base y-axis coordinate.")
        .def_readwrite("node_spacing_x_axis", &LayoutConfig::node_spacing_x_axis, "Horizontal spacing between nodes")
        .def_readwrite("node_spacing_y_axis", &LayoutConfig::node_spacing_y_axis, "Vertical spacing between nodes.")
        .def_readwrite("port_spacing", &LayoutConfig::port_spacing, "Spacing between ports on a node.");

    py::class_<GridConfig>(m, "GridConfig", 
        R"doc(
        The GridConfig class is used to pass the number of columns and rows for both left and right sides of the grid to the Graph object.
        )doc"
    )
        .def(py::init<int, int, int, int>(), 
            py::arg("columns_left"), 
            py::arg("columns_right"), 
            py::arg("rows_left"), 
            py::arg("rows_right"),
            R"pbdoc(
            Constructs a GridConfig object.
            Args:
                columns_left (int): Number of columns on the left side of the grid.
                columns_right (int): Number of columns on the right side of the grid.
                rows_left (int): Number of rows on the left side of the grid.
                rows_right (int): Number of rows on the right side of the grid.
            )pbdoc"
        )
        .def_readwrite("num_columns_left", &GridConfig::columns_left, "Number of columns on the left side of the grid.")
        .def_readwrite("num_columns_right", &GridConfig::columns_right, "Number of columns on the right side of the grid.")
        .def_readwrite("num_rows_left", &GridConfig::rows_left, "Number of rows on the left side of the grid.")
        .def_readwrite("num_rows_right", &GridConfig::rows_right, "Number of rows on the right side of the grid.");

    py::class_<NodeConfig>(m, "NodeConfig", 
        R"doc(
        The NodeConfig class is used to pass the width, height, and label height of each node on the Graph.
        )doc"
    )
        .def(py::init<double, double, double>(), 
            py::arg("width"), 
            py::arg("height"), 
            py::arg("label_height"),
            R"pbdoc(
            Constructs a NodeConfig object.
            Args:
                width (float): The width of the node.
                height (float): The height of the node.
                label_height (float): The height of the label on the node.
            )pbdoc"
        );

    py::class_<CentralNodeConfig>(m, "CentralNodeConfig", R"doc(
        The CentralNodeConfig class is used to pass the width, height, and label height of the central node on the Graph.
    )doc"
    )
        .def(py::init<double, double, double>(), 
            py::arg("width"), 
            py::arg("height"), 
            py::arg("label_height"));

    py::class_<PortConfig>(m, "PortConfig", R"doc(
        The PortConfig class is used to pass the width and height of each port on the Graph.
    )doc"
    )
        .def(py::init<double, double>(), 
            py::arg("port_width"), 
            py::arg("port_height"),
        
            R"pbdoc(
            Constructs a PortConfig object.
            Args:
                port_width (float): The width of each port.
                port_height (float): The height of each port.
            )pbdoc"
        )
        .def_readwrite("port_width", &PortConfig::port_width, "The width of each port.")
        .def_readwrite("port_height", &PortConfig::port_height, "The height of each port.");

    py::class_<LabelExport>(m, "Label", 
        R"doc(
        The LabelExport class is used to export label information for nodes on the Graph.
        It contains the label name, source and target IDs, and position dimensions.
        These attributes are read-only to ensure the integrity of the Graph.
        )doc"
    )
        .def(py::init<>())
        .def_readonly("name", &LabelExport::name, "The name of the label.")
        .def_readonly("x", &LabelExport::x, "The x-coordinate of the label.")
        .def_readonly("y", &LabelExport::y, "The y-coordinate of the label.")
        .def_readonly("width", &LabelExport::width, "The width of the label.")
        .def_readonly("height", &LabelExport::height, "The height of the label.")
        .def_readonly("source_id", &LabelExport::source_id, "The source ID of the label.")
        .def_readonly("target_id", &LabelExport::target_id, "The target ID of the label.");

    py::class_<LinkExport>(m, "Link", R"doc(
        The LinkExport class is used to export link information between nodes on the Graph.
        It contains the source and target coordinates, as well as the IDs of the connected nodes/ports.
        These attributes are read-only to ensure the integrity of the Graph.
    )doc"
    )
        .def(py::init<>())
        .def_readonly("source_x", &LinkExport::source_x, "The x-coordinate of the source node.")
        .def_readonly("source_y", &LinkExport::source_y, "The y-coordinate of the source node.")
        .def_readonly("target_x", &LinkExport::target_x, "The x-coordinate of the target node.")
        .def_readonly("target_y", &LinkExport::target_y, "The y-coordinate of the target node.")
        .def_readonly("label", &LinkExport::label, "The label of the link")
        .def_readonly("_id", &LinkExport::_id, "The ID of the link.")
        .def_readonly("source_id", &LinkExport::source_id, "The source ID of the link.")
        .def_readonly("target_id", &LinkExport::target_id, "The target ID of the link.")
        .def_readonly("has_waypoints", &LinkExport::has_waypoints, "Indicates if the link has waypoints.")
        .def_readonly("waypoints", &LinkExport::waypoints, "The waypoints of the link.");
    
    py::class_<WaypointLinks>(m, "WaypointLinks", R"doc(
        The WaypointLinks class is used to export waypoint information for links on the Graph.
        It contains the x and y coordinates of the waypoints.
        These attributes are read-only to ensure the integrity of the Graph.
    )doc"
    )
        .def(py::init<>())
        .def_readonly("source_x", &WaypointLinks::source_x, "The x-coordinate of the waypoint.")
        .def_readonly("source_y", &WaypointLinks::source_y, "The y-coordinate of the waypoint.")
        .def_readonly("target_x", &WaypointLinks::target_x, "The x-coordinate of the target waypoint.")
        .def_readonly("target_y", &WaypointLinks::target_y, "The y-coordinate of the target waypoint.");

    py::class_<PortExport>(m, "Port", R"doc(
        The PortExport class is used to export port information on the Graph.
        It contains the position and dimensions of the port, as well as the IDs of the connected ports.
        These attributes are read-only to ensure the integrity of the Graph.
    )doc"
    )
        .def(py::init<>())
        .def_readonly("name", &PortExport::label, "The name of the port.")
        .def_readonly("x", &PortExport::x, "The x-coordinate of the port.")
        .def_readonly("y", &PortExport::y, "The y-coordinate of the port.")
        .def_readonly("width", &PortExport::width, "The width of the port.")
        .def_readonly("height", &PortExport::height, "The height of the port.")
        .def_readonly("source_id", &PortExport::source_id, "The source ID of the port.")
        .def_readonly("target_id", &PortExport::target_id, "The target ID of the port.");

    py::class_<NodeExport>(m, "Node", R"doc(
        The NodeExport class is used to export node information on the Graph.
        It contains the node's label, position, dimensions, and IDs for the source and target.
        These attributes are read-only to ensure the integrity of the Graph.
    )doc"
    )
        .def(py::init<>())
        .def_readonly("name", &NodeExport::name, "The label/name of the node.")
        .def_readonly("label", &NodeExport::label, "The label object of the node.")
        .def_readonly("source_id", &NodeExport::source_id, "The source ID of the node.")
        .def_readonly("target_id", &NodeExport::target_id, "The target ID of the node.")
        .def_readonly("x", &NodeExport::x, "The x-coordinate of the node.")
        .def_readonly("y", &NodeExport::y, "The y-coordinate of the node.")
        .def_readonly("width", &NodeExport::width, "The width of the node.")
        .def_readonly("height", &NodeExport::height, "The height of the node.");

    py::class_<Graph>(m, "Graph",
        R"doc(
        The Graph class builds and manages diagram models, handling all node, port, and link objects.

        The Graph class maintains containers for nodes, ports, and links, as well as their lightweight export structs for Python integration.
        It tracks layout, grid, and node positions, manages creation and storage, and provides functions to ensure data consistency between C++ and Python.
        All state and ownership of objects are tightly controlled within the Graph class.

        Args:
            layout_config (LayoutConfig): Layout configuration for node and port positioning.
            grid_config (GridConfig): Grid configuration specifying columns and rows.
            central_node_config (CentralNodeConfig): Configuration for the central node.
            node_config (NodeConfig): Configuration for node dimensions.
            port_config (PortConfig): Configuration for port dimensions.

        Methods:
            add_node(node_meta_data, port_labels_left, port_labels_right, connection_indexes_left, connection_indexes_right)
                Adds a node to the graph with the specified metadata, port labels, and connection indexes.

            connect_nodes()
                Connects nodes in the graph by adding outgoing links.

            get_nodes()
                Returns a dictionary of node exports representing all nodes in the graph.

            get_ports()
                Returns a dictionary of port exports representing all ports in the graph.

            get_links()
                Returns a list of link exports representing all links in the graph.

            get_node_ids()
                Returns a list of all node IDs in the graph.

            get_node_ids_left()
                Returns a list of node IDs on the left side of the graph.

            get_node_ids_right()
                Returns a list of node IDs on the right side of the graph.

            debug_print_node_data()
                Prints debug information for all nodes in the graph.
        )doc"
    )
        .def(py::init<LayoutConfig, GridConfig, CentralNodeConfig, NodeConfig, PortConfig>(),
            py::arg("layout_config"),
            py::arg("grid_config"),
            py::arg("central_node_config"),
            py::arg("node_config"),
            py::arg("port_config"),
            R"pbdoc(
            Constructs a Graph object.

            Args:
                layout_config (LayoutConfig): Layout configuration for node and port positioning.
                grid_config (GridConfig): Grid configuration specifying columns and rows.
                central_node_config (CentralNodeConfig): Configuration for the central node.
                node_config (NodeConfig): Configuration for node dimensions.
                port_config (PortConfig): Configuration for port dimensions.
            )pbdoc"
        )
        .def("add_node", &Graph::add_node, 
            py::arg("node_meta_data"), 
            py::arg("port_labels_left"), 
            py::arg("port_labels_right"), 
            py::arg("connection_indexes_left"), 
            py::arg("connection_indexes_right"),
            R"pbdoc(
            Adds a node to the graph with the specified metadata, port labels, and connection indexes.
            Args:
                node_meta_data (dict): Metadata for the node, including label, type, and orientation.
                port_labels_left (list): Labels for ports on the left side of the node.
                port_labels_right (list): Labels for ports on the right side of the node.
                connection_indexes_left (list): Connection indexes for left ports.
                connection_indexes_right (list): Connection indexes for right ports.
            )pbdoc"
        )
        .def("connect_nodes", &Graph::connect_nodes, 
            R"pbdoc(
            Connects nodes in the graph by adding outgoing links.
            )pbdoc"
        )
        .def("get_nodes", &Graph::get_nodes, 
            R"pbdoc(
            Returns a dictionary of node exports representing all nodes in the graph.
            )pbdoc"
        )
        .def("get_ports", &Graph::get_ports, 
            R"pbdoc(
            Returns a dictionary of port exports representing all ports in the graph.
            )pbdoc"
        )
        .def("get_node_ids", &Graph::get_node_ids, 
            R"pbdoc(
            Returns a list of all node IDs in the graph.
            )pbdoc"
        )
        .def("get_node_ids_left", &Graph::get_node_ids_left, 
            R"pbdoc(
            Returns a list of node IDs on the left side of the graph.
            )pbdoc"
        )
        .def("get_node_ids_right", &Graph::get_node_ids_right, 
            R"pbdoc(
            Returns a list of node IDs on the right side of the graph.
            )pbdoc"
        )
        .def("connect_nodes", &Graph::connect_nodes, 
            R"pbdoc(
            Connects nodes in the graph by adding outgoing links.
            )pbdoc"
        )
        .def("get_links", &Graph::get_links, 
            R"pbdoc(
            Returns a list of link exports representing all links in the graph.
            )pbdoc"
        );
}
