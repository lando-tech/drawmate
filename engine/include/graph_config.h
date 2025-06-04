#ifndef GRAPH_CONFIG_H
#define GRAPH_CONFIG_H

/**
 * GridOrientation enum
 * The GridOrientation interface is used by the Graph class,
 * as well as some of the GraphObject classes to determine adjacency
 * on the Graph/Grid. 
 */
enum class GridOrientation
{
    LEFT,
    RIGHT,
    ABOVE,
    BELOW,
    CENTER,
};

/**
 * LayoutConfig struct
 * The LayoutConfig interface is exported via PYBIND_11 
 * for Python to declare base x/y values, and x/y spacing
 * for nodes and ports on the Graph.
 */
struct LayoutConfig
{
    // TODO add bounds checking to ensure Graph/Grid integrity
    double base_x{};
    double base_y{};
    double node_spacing_x_axis{};
    double node_spacing_y_axis{};
    // TODO calculated at runtime, remove from Python interface
    double port_spacing{};
};

/** 
 * GridConfig struct 
 * The GridConfig interface is exported via PYBIND_11
 * for Python to pass to the Graph object
 * to account for the number of columns/rows (both left and right)
 * on the grid.
 */
struct GridConfig
{
    int columns_left{};
    int columns_right{};
    int rows_left{};
    int rows_right{};
};

/** 
 * NodeConfig struct
 * The NodeConfig interface is exported via PYBIND_11
 * for Python to declare the width,
 * height, and the label height for each node on the graph.
 */
struct NodeConfig
{
    double width{};
    double height{};
    // TODO calculated at runtime, remove from Python interface
    double label_height{};
};

/**
 * CentralNodeConfig struct
 * The CentralNodeConfig interface is exported via PYBIND_11
 * for Python to declare the width, height, and label height
 * of the central node (matrix) on the Graph.
 */
struct CentralNodeConfig
{
    double width{};
    double height{};
    // TODO calculated at runtime, remove from Python interface
    double label_height{};
};

/**
 * PortConfig struct
 * The PortConfig interface is exported via PYBIND_11
 * for Python to declare the width and height of each
 * port on the Graph. 
 */
struct PortConfig
{
    // TODO calculated at runtime, remove from Python interface
    double port_width{};
    double port_height{};
};

#endif // GRAPH_CONFIG_H