//
// Created by landotech on 5/16/25.
//

#ifndef GRAPH_H
#define GRAPH_H
#include <memory>
#include <unordered_map>
#include "node.h"
#include "link.h"

struct GridConfig
{
    int columns_left{};
    int columns_right{};
    int rows_left{};
    int rows_right{};
};

struct LayoutConfig
{
    double node_spacing_x_axis{};
    double node_spacing_y_axis{};
    double port_spacing{};
    double base_x{};
    double base_y{};
    double node_width{};
    double node_height{};
    double node_label_height{};
    double port_height{};
    double port_width{};
};

class Graph
{
    int column_count_left{0};
    int row_count_left{0};
    int column_count_right{0};
    int row_count_right{0};

    double base_y_left{};
    double base_x_left{};
    double base_y_right{};
    double base_x_right{};

    std::unordered_map<std::string, std::unique_ptr<Node>> nodes{};
    std::unordered_map<std::string, std::unordered_map<int, std::unique_ptr<Link>>> links{};

    std::vector<std::string> node_keys_master_{};
    std::vector<std::string> node_keys_left_{};
    std::vector<std::string> node_keys_right_{};
    std::vector<std::string> node_meta_valid_keys_{"node-label", "node-type", "node-orientation"};
    GridConfig grid_config_{};
    LayoutConfig layout_config_{};

    void add_node_ports(const std::string &node_key, const std::vector<std::string> &port_labels_left,
                        const std::vector<std::string> &port_labels_right);

    // TODO add better error message for invalid keys
    void verify_node_meta_key(const std::unordered_map<std::string, std::string>& node_meta_data) const;

    double verify_node_height(double port_count) const;

    double calculate_x_left() const;

    void increment_y_left(double node_height);

    // TODO account for central node, add fallback if none exists
    double calculate_x_right(double central_width) const;

    void increment_y_right(double node_height);

    std::string generate_node_key(char orientation);

    void pretty_print_node_data(const std::string& node_id, double node_height) const;

public:

    Graph(const LayoutConfig &layout_config, GridConfig grid_config);

    void add_node(const std::unordered_map<std::string, std::string>& node_meta_data,
                  const std::vector<std::string>& port_labels_left, const std::vector<std::string>& port_labels_right);

    void add_connection(const std::string &source_node_id, const std::string &target_node_id, int port_index_source,
                        int port_index_target);

    void get_nodes() const;

    std::vector<std::string> get_node_ids() const { return this->node_keys_master_; }
    std::vector<std::string> get_node_ids_left() const { return this->node_keys_left_; }
    std::vector<std::string> get_node_ids_right() const { return this->node_keys_right_; }

};

#endif //GRAPH_H
