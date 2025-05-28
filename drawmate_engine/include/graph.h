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
  GridConfig grid_config_{};
  LayoutConfig layout_config_{};
  NodeConfig node_config_{};
  CentralNodeConfig central_node_config_{};
  PortConfig port_config_{};

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

  std::unordered_map<NodeKey, std::unique_ptr<Node>> nodes_{};
  std::unordered_map<PortKey, std::unique_ptr<Port>> ports_{};

  std::vector<PortKey> port_ids_left_{};
  std::vector<PortKey> port_ids_right_{};

  std::unordered_map<PortKey, std::unique_ptr<Link>> incoming_links_{};
  std::unordered_map<PortKey, std::unique_ptr<Link>> outgoing_links_{};

  // Exported containers for PYBIND11
  std::unordered_map<std::string, NodeExport> node_exports_{};
  std::unordered_map<std::string, PortExport> port_exports_{};
  std::vector<LinkExport> link_exports_{};

  std::vector<std::string> node_keys_master_external{};
  std::vector<std::string> node_keys_left_external{};
  std::vector<std::string> node_keys_right_external{};

  std::vector<std::string> node_meta_valid_keys_{"node-label", "node-type",
                                                 "node-orientation"};

  NodeKey add_node_left_justified(const double max_ports, 
                               NodeType node_type, 
                               const std::string &node_label, 
                               std::vector<int> connection_indexes_left, 
                               std::vector<int> connection_indexes_right);

  NodeKey add_node_right_justified(const double max_ports, 
                                NodeType node_type, 
                                const std::string &node_label, 
                                std::vector<int> connection_indexes_left, 
                                std::vector<int> connection_indexes_right);

  NodeKey add_node_center_justified(const double max_ports,
                                 NodeType node_type, 
                                 const std::string &node_label, 
                                 std::vector<int> connection_indexes_left, 
                                 std::vector<int> connection_indexes_right);

  void add_node_spanning(NodeOrientation node_orientation);

  void add_node_export(NodeKey node_key_internal, const std::string& node_key_external);

  void add_node_ports(NodeKey node_key_internal,
                      const std::string& node_key_external,
                      const std::vector<std::string> &port_labels_left,
                      const std::vector<std::string> &port_labels_right,
                      NodeOrientation node_orientation);

  void add_node_ports_left_justified(std::vector<std::string> port_labels,
                                     const NodeKey node_key, 
                                     double x_left, 
                                     double y_left, 
                                     NodeExport& node_export, 
                                     int port_index);

  void add_node_ports_right_justified(std::vector<std::string> port_labels, 
                                      const NodeKey node_key, 
                                      double x_left, 
                                      double y_left, 
                                      NodeExport& node_export, 
                                      int port_index);

  PortExport add_port_export(double x, double y, std::string port_label);

  void add_port_target_id(PortKey source_port_key, PortKey target_port_key);

  void add_link_export(const std::string& source_id, const std::string& target_id, double src_x, double src_y, double tgt_x, double tgt_y, bool has_waypoints, std::vector<WaypointLinks> waypoints);

  void add_link_incoming();

  void add_link_outgoing();

  // TODO add better error message for invalid keys
  void verify_node_meta_key(
      const std::unordered_map<std::string, std::string> &node_meta_data) const;

  double verify_node_height(double port_count);

  double verify_node_height_test(double port_count);

  double calculate_x_left() const;

  // TODO account for central node, add fallback if none exists
  double calculate_x_right(double central_width) const;

  void increment_y_left(double node_height);

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

  void connect_nodes()
  {
    this->add_link_outgoing();
  };

  void debug_print_node_data() const;

  std::unordered_map<std::string, NodeExport> get_nodes()
  {
    return this->node_exports_;
  };

  std::unordered_map<std::string, PortExport> get_ports()
  {
    return this->port_exports_;
  }

  std::vector<LinkExport> get_links()
  {
    return this->link_exports_;
  }

  std::vector<std::string> get_node_ids() const
  {
    return this->node_keys_master_external;
  }
  std::vector<std::string> get_node_ids_left() const
  {
    return this->node_keys_left_external;
  }
  std::vector<std::string> get_node_ids_right() const
  {
    return this->node_keys_right_external;
  }
};

#endif // GRAPH_H
