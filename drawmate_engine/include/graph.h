//
// Created by landotech on 5/16/25.
//

#ifndef GRAPH_H
#define GRAPH_H
#include "graph_exports.h"
#include "graph_config.h"
#include "link.h"
#include "keys.h"
#include "node.h"
#include <memory>
#include <unordered_map>

class Graph
{

  int central_node_count{0};
  int column_count_left{0};
  int row_count_left{0};
  int column_count_right{0};
  int row_count_right{0};

  int total_node_count_{0};
  const int key_size{20};

  double base_y_left{};
  double base_x_left{};
  double base_y_right{};
  double base_x_right{};

  double max_height_{0.0};
  double base_height_{0.0};

  std::unordered_map<NodeKey, std::unique_ptr<Node>> nodes_test_{};
  std::unordered_map<std::string, std::unique_ptr<Node>> nodes{};
  std::unordered_map<std::string, std::unique_ptr<Port>> ports{};
  std::unordered_map<std::string, NodeExport> node_exports_{};

  std::unordered_map<std::string, std::unique_ptr<Link>> incoming_links_{};
  std::unordered_map<std::string, std::unique_ptr<Link>> outgoing_links_{};

  std::vector<LinkExport> link_exports_{};

  std::vector<std::string> node_keys_master_{};
  std::vector<std::string> node_keys_left_{};
  std::vector<std::string> node_keys_right_{};
  std::vector<std::string> node_meta_valid_keys_{"node-label", "node-type",
                                                 "node-orientation"};

  std::vector<std::string> port_ids_left_{};
  std::vector<std::string> port_ids_right_{};

  GridConfig grid_config_{};
  LayoutConfig layout_config_{};
  NodeConfig node_config_{};
  CentralNodeConfig central_node_config_{};
  PortConfig port_config_{};

  void add_node_internal(const std::string &node_label,
                         std::vector<std::string> port_labels_left,
                         std::vector<std::string> port_labels_right,
                         NodeType node_type, NodeOrientation node_orientation,
                         const std::vector<int> connection_indexes_left,
                         const std::vector<int> connection_indexes_right);

  void add_node_export(const std::string &node_key);

  void add_node_ports(const std::string &node_key,
                      const std::vector<std::string> &port_labels_left,
                      const std::vector<std::string> &port_labels_right,
                      NodeOrientation node_orientation);

  PortExport add_port_export(double x, double y, std::string port_label);

  void add_link_export(double src_x, double src_y, double tgt_x, double tgt_y, bool has_waypoints, std::vector<WaypointLinks> waypoints);

  void add_connection_incoming();

  void add_connection_outgoing();

  void connect_central_node();

  void connect_nodes_internal();

  void set_node_colum_row(const std::string &node_key);

  // TODO add better error message for invalid keys
  void verify_node_meta_key(
      const std::unordered_map<std::string, std::string> &node_meta_data) const;

  double verify_node_height(double port_count);

  double verify_node_height_test(double port_count);

  double calculate_x_left() const;

  void increment_y_left(double node_height);

  // TODO account for central node, add fallback if none exists
  double calculate_x_right(double central_width) const;

  void increment_y_right(double node_height);

  void increment_grid_column_left();

  void increment_grid_column_right();

  void test_port_map();

  void test_node_map();

  void test_link_map();

  void pretty_print_node_data(const std::string &node_id,
                              double node_height) const;

public:
  Graph(const LayoutConfig &layout_config, const GridConfig &grid_config,
        const CentralNodeConfig &central_node_config,
        const NodeConfig &node_config, const PortConfig &port_config);

  void
  add_node(const std::unordered_map<std::string, std::string> &node_meta_data,
           const std::vector<std::string> &port_labels_left,
           const std::vector<std::string> &port_labels_right,
           const std::vector<int> connection_indexes_left,
           const std::vector<int> connection_indexes_right);

  void connect_nodes();

  void debug_print_node_data() const;

  std::unordered_map<std::string, NodeExport> get_nodes();

  std::vector<LinkExport> get_links() { return this->link_exports_; }

  std::vector<std::string> get_node_ids() const
  {
    return this->node_keys_master_;
  }
  std::vector<std::string> get_node_ids_left() const
  {
    return this->node_keys_left_;
  }
  std::vector<std::string> get_node_ids_right() const
  {
    return this->node_keys_right_;
  }
};

#endif // GRAPH_H
