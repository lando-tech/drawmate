#ifndef GRAPH_CONFIG_H
#define GRAPH_CONFIG_H

enum class GridOrientation
{
    LEFT,
    RIGHT,
    ABOVE,
    BELOW,
    CENTER,
};

struct LayoutConfig
{
    double base_x{};
    double base_y{};
    double node_spacing_x_axis{};
    double node_spacing_y_axis{};
    double port_spacing{};
};

struct GridConfig
{
    int columns_left{};
    int columns_right{};
    int rows_left{};
    int rows_right{};
};

struct NodeConfig
{
    double width{};
    double height{};
    double label_height{};
};

struct CentralNodeConfig
{
    double width{};
    double height{};
    double label_height{};
};

struct PortConfig
{
    double port_width{};
    double port_height{};
};

#endif // GRAPH_CONFIG_H