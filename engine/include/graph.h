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


/** Graph class
 * The base Graph class responsible for building the diagram model.
 * The Graph class handles containerization of all node objects, to include
 * Nodes, Ports, Links, and their corresponding exports.
 * Objects that end with 'export' are lightweight structs that are exposed
 * to the Python interface.
 * The Graph class implements a multitude of functions to track x/y bounding
 * limits, grid counters responsible for keeping nodes in their respective columns/rows,
 * creation and storage of Graph objects, and various test functions to ensure exports are
 * synced with the native C++ containers. The decision to keep some functions that could
 * have been placed externally was intentional to ensure the state and ownership of objects
 * were tightly controlled by the Graph.
 */

class Graph
{
private:
  GridConfig m_grid_config_{}; /**< GridConfig m_grid_config_ */
  LayoutConfig layout_config_{}; /**< LayoutConfig layout_config_ */
  NodeConfig node_config_{}; /**< NodeConfig node_config_ */
  CentralNodeConfig central_node_config_{}; /**< CentralNodeConfig central_node_config_ */
  PortConfig port_config_{}; /**< PortConfig port_config_ */

  int central_node_count{0}; /**< int central_node_count */
  int column_count_left{0}; /**< int column_count_left */
  int row_count_left{0}; /**< int row_count_left */
  int column_count_right{0}; /**< int column_count_right */
  int row_count_right{0}; /**< int row_count_right */

  int total_node_count_{0}; /**< int total_node_count */
  const int key_size{20}; /**< const int key_size */

  double base_y_left{}; /**< double base_y_left */
  double base_x_left{}; /**< double base_x_left */
  double base_y_right{}; /**< double base_y_right */
  double base_x_right{}; /**< double base_x_right */

  double max_height_{0.0}; /**< double max_height */
  double base_height_{0.0}; /**< double base_height */

  std::unordered_map<NodeKey, std::unique_ptr<Node>> nodes_{}; /**< std::unordered_map<NodeKey, std::unique_ptr<Node>> nodes_ */
  std::unordered_map<PortKey, std::unique_ptr<Port>> ports_{}; /**< std::unordered_map<PortKey, std::unique_ptr<Port>> ports_ */

  std::vector<PortKey> port_ids_left_{}; /**< std::vector<PortKey> port_ids_left_ */
  std::vector<PortKey> port_ids_right_{}; /**< std::vector<PortKey> port_ids_right_ */

  std::unordered_map<PortKey, std::unique_ptr<Link>> incoming_links_{}; /**< std::unordered_map<PortKey, std::unique_ptr<Link>> incoming_links_ */
  std::unordered_map<PortKey, std::unique_ptr<Link>> outgoing_links_{}; /**< std::unordered_map<PortKey, std::unique_ptr<Link>> outgoing_links_ */

  // Exported containers for PYBIND11
  std::unordered_map<std::string, NodeExport> node_exports_{}; /**< std::unordered_map<std::string, NodeExport> node_exports_ */
  std::unordered_map<std::string, PortExport> port_exports_{}; /**< std::unordered_map<std::string, PortExport> port_exports_ */
  std::vector<LinkExport> link_exports_{}; /**< std::vector<LinkExport> link_exports_ */

  std::vector<std::string> node_keys_master_external{}; /**< std::vector<std::string> node_keys_master_external */
  std::vector<std::string> node_keys_left_external{}; /**< std::vector<std::string> node_keys_left_external */
  std::vector<std::string> node_keys_right_external{}; /**< std::vector<std::string> node_keys_right_external */

  std::vector<std::string> node_meta_valid_keys_{"node-label", "node-type",
                                                 "node-orientation"}; /**< std::vector<std::string> node_meta_valid_keys_ */

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

  /**
   * @brief Adds ports to a node, handling both left and right port labels and orientation.
   * @param node_key_internal Internal key for the node.
   * @param node_key_external External key for the node.
   * @param port_labels_left Labels for the left ports.
   * @param port_labels_right Labels for the right ports.
   * @param node_orientation Orientation of the node.
   */
  void add_node_ports(NodeKey node_key_internal,
                      const std::string& node_key_external,
                      const std::vector<std::string> &port_labels_left,
                      const std::vector<std::string> &port_labels_right,
                      NodeOrientation node_orientation);

  /**
   * @brief Adds left-justified ports to a node.
   * @param port_labels Labels for the ports.
   * @param node_key Key for the node.
   * @param x_left X coordinate for the leftmost port.
   * @param y_left Y coordinate for the leftmost port.
   * @param node_export Reference to the node export struct.
   * @param port_index Index of the port.
   */
  void add_node_ports_left_justified(std::vector<std::string> port_labels,
                                     const NodeKey node_key,
                                     double x_left,
                                     double y_left,
                                     NodeExport& node_export,
                                     int port_index);

  /**
   * @brief Adds right-justified ports to a node.
   * @param port_labels Labels for the ports.
   * @param node_key Key for the node.
   * @param x_left X coordinate for the rightmost port.
   * @param y_left Y coordinate for the rightmost port.
   * @param node_export Reference to the node export struct.
   * @param port_index Index of the port.
   */
  void add_node_ports_right_justified(std::vector<std::string> port_labels,
                                      const NodeKey node_key,
                                      double x_left,
                                      double y_left,
                                      NodeExport& node_export,
                                      int port_index);

  /**
   * @brief Creates and returns a PortExport struct for a port.
   * @param x X coordinate of the port.
   * @param y Y coordinate of the port.
   * @param port_label Label for the port.
   * @return PortExport struct with the specified parameters.
   */
  PortExport add_port_export(double x, double y, std::string port_label);

  /**
   * @brief Sets the target port ID for a given source port.
   * @param source_port_key Key of the source port.
   * @param target_port_key Key of the target port.
   */
  void add_port_target_id(PortKey source_port_key, PortKey target_port_key);

  /**
   * @brief Adds a link export between two ports or nodes.
   * @param source_id Source ID.
   * @param target_id Target ID.
   * @param src_x X coordinate of the source.
   * @param src_y Y coordinate of the source.
   * @param tgt_x X coordinate of the target.
   * @param tgt_y Y coordinate of the target.
   * @param has_waypoints Whether the link has waypoints.
   * @param waypoints List of waypoints for the link.
   */
  void add_link_export(const std::string& source_id, const std::string& target_id, const std::string& label, double src_x, double src_y, double tgt_x, double tgt_y, bool has_waypoints, std::vector<WaypointLinks> waypoints);

  /**
   * @brief Adds incoming links to the graph.
   */
  void add_link_incoming();

  /**
   * @brief Adds outgoing links to the graph.
   */
  void add_link_outgoing();

  /**
   * @brief Verifies that the node metadata contains valid keys.
   * @param node_meta_data Map of node metadata.
   */
  void verify_node_meta_key(const std::unordered_map<std::string, std::string> &node_meta_data) const;

  /**
   * @brief Function for verifying node height calculation.
   * @param port_count Number of ports.
   * @return Calculated node height.
   */
  double verify_node_height(double port_count);

  /**
   * @brief Calculates the leftmost X coordinate for node placement.
   * @return X coordinate.
   */
  double calculate_x_left() const;

  /**
   * @brief Calculates the rightmost X coordinate for node placement.
   * @param central_width Width of the central node.
   * @return X coordinate.
   */
  double calculate_x_right(double central_width) const;

  /**
   * @brief Increments the Y coordinate for left-side node placement.
   * @param node_height Height of the node.
   */
  void increment_y_left(double node_height);

  /**
   * @brief Increments the Y coordinate for right-side node placement.
   * @param node_height Height of the node.
   */
  void increment_y_right(double node_height);

  void increment_grid_column_left();

  void increment_grid_column_right();

  void test_port_map();

  void test_node_map();

  void test_link_map();

  void pretty_print_node_data(const std::string &node_id,
                              double node_height) const;

public:
  /**
   * @brief Constructs a Graph object for building and managing diagram models.
   *
   * Initializes the Graph with configuration objects for layout, grid, central node, node, and port.
   * The Graph manages all nodes, ports, and links, and maintains export containers for Python integration.
   * All state and ownership of objects are tightly controlled within the Graph.
   *
   * @param layout_config Layout configuration for node and port positioning.
   * @param grid_config Grid configuration specifying columns and rows.
   * @param central_node_config Configuration for the central node.
   * @param node_config Configuration for node dimensions.
   * @param port_config Configuration for port dimensions.
   */
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
