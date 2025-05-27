//
// Created by landotech on 5/16/25.
//

#include "graph.h"
#include "keys.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <sstream>
#include <string>

NodeType verify_node_type(const std::string &node_type_str)
{
  /*
   * This function simply enforces the API between the Python
   * dict being passed in based on the accetable keys.
   * It also returns the node type back to the caller, or throws
   * an error if not found.
   */
  if (node_type_str == "__SPAN__")
  {
    return NodeType::SPAN;
  }
  if (node_type_str == "video-matrix")
  {
    return NodeType::VIDEO_MATRIX;
  }
  if (node_type_str == "video-codec")
  {
    return NodeType::VIDEO_CODEC;
  }
  if (node_type_str == "audio-matrix")
  {
    return NodeType::AUDIO_MATRIX;
  }
  if (node_type_str == "audio-codec")
  {
    return NodeType::AUDIO_CODEC;
  }
  if (node_type_str == "pc")
  {
    return NodeType::PC;
  }
  if (node_type_str == "laptop")
  {
    return NodeType::LAPTOP;
  }
  if (node_type_str == "appliance")
  {
    return NodeType::APPLIANCE;
  }
  throw std::runtime_error("Invalid Node Type: " + node_type_str);
}

NodeOrientation verify_node_orientation(const std::string &orientation)
{
  /*
   * Verifies node orientation and returns orientation back to the caller.
   */
  if (orientation == "left")
  {
    return NodeOrientation::LEFT;
  }
  if (orientation == "right")
  {
    return NodeOrientation::RIGHT;
  }
  if (orientation == "center")
  {
    return NodeOrientation::CENTER;
  }
  throw std::runtime_error("Please specify Node Orientation: ['left', 'right', "
                           "'center']. Arg passed: " +
                           orientation);
}

void Graph::verify_node_meta_key(
    const std::unordered_map<std::string, std::string> &node_meta_data) const
{
  /*
   * Verifies the acceptable meta keys being passed in by the Python API.
   */
  for (const auto &it : this->node_meta_valid_keys_)
  {
    if (!node_meta_data.contains(it))
    {
      throw std::runtime_error(
          "Error parsing Node metadata Dictionary! Key is invalid!");
    }
  }
}

double Graph::verify_node_height(const double port_count)
{
  /*
   * Verifies the height of each node and ensures it has room to house
   * all of the ports, based on the max number of ports either left/right.
   */
  double node_height{};
  if (port_count <= 1)
  {
    node_height = this->node_config_.height;
    this->base_height_ = node_height;
  }
  else if (port_count == 2)
  {
    node_height = (this->node_config_.height * port_count) +
                  this->port_config_.port_height;
    this->base_height_ = node_height;
  }
  else
  {
    node_height = (this->node_config_.height * port_count) +
                  (this->port_config_.port_height * (port_count - 1));
    this->base_height_ = node_height;
  }

  if (this->base_height_ > this->max_height_)
  {
    this->max_height_ = this->base_height_;
  }

  return node_height;
}

double Graph::verify_node_height_test(const double port_count)
{
  double actual_height{
    (this->port_config_.port_height * port_count) + 
    (this->layout_config_.port_spacing * (port_count - 1)) + 
    (this->node_config_.label_height + this->port_config_.port_height)
  };

  double node_height{};
  if (actual_height > this->node_config_.height)
  {
    node_height = actual_height;
    this->base_height_ = actual_height;
  }
  else
  {
    node_height = this->node_config_.height;
    this->base_height_ = this->node_config_.height;
  }

  if (this->base_height_ > this->max_height_)
  {
    this->max_height_ = this->base_height_;
  }

  return node_height;
}

double get_max_ports(const double port_count_left,
                     const double port_count_right)
{
  if (port_count_left > port_count_right)
  {
    return port_count_left;
  }
  return port_count_right;
}

double Graph::calculate_x_left() const
{
  return (this->base_x_left - (this->layout_config_.node_spacing_x_axis *
                               (this->column_count_left + 1)));
}

double Graph::calculate_x_right(const double central_width) const
{
  const double base{this->layout_config_.base_x + central_width};
  const double offset{this->layout_config_.node_spacing_x_axis -
                      this->node_config_.width};
  return base + offset +
         (this->column_count_right * this->layout_config_.node_spacing_x_axis);
}

void Graph::increment_y_left(const double node_height)
{
  this->base_y_left = this->base_y_left + node_height +
                      this->layout_config_.node_spacing_y_axis;
  double max_y{this->layout_config_.base_y + this->max_height_};

  if (this->base_y_left > max_y)
  {
    this->base_y_left = this->layout_config_.base_y;
  }
}

void Graph::increment_y_right(const double node_height)
{
  this->base_y_right = this->base_y_right + node_height +
                       this->layout_config_.node_spacing_y_axis;
  double max_y{this->layout_config_.base_y + this->max_height_};
  if (this->base_y_right > max_y)
  {
    this->base_y_right = this->layout_config_.base_y;
  }
}

void Graph::increment_grid_column_left()
{
  this->row_count_left++;
  if (this->row_count_left >= this->grid_config_.rows_left)
  {
    this->row_count_left = 0;
    this->column_count_left++;
  }
}

void Graph::increment_grid_column_right()
{
  this->row_count_right++;
  if (this->row_count_right >= this->grid_config_.rows_right)
  {
    this->row_count_right = 0;
    this->column_count_right++;
  }
}

void Graph::add_node_ports(NodeKey node_key_test,
                           const std::vector<std::string> &port_labels_left,
                           const std::vector<std::string> &port_labels_right,
                           NodeOrientation node_orientation)
{
  const auto &node{this->nodes_test_.at(node_key_test)};
  std::string node_key_str{generate_node_key_string(node_key_test.orientation, node_key_test.column, node_key_test.row)};
  auto &node_export{this->node_exports_.at(node_key_str)};

  double x_left{node->get_x()};
  double y_left{node->get_y() + this->node_config_.label_height +
                this->port_config_.port_height / 2};
  double y_right{node->get_y() + this->node_config_.label_height +
                 this->port_config_.port_height / 2};

  int port_index_left{};
  int port_index_right{};

  if (node_orientation == NodeOrientation::CENTER)
  {
    port_index_left = 0;
    port_index_right = 0;
  }
  else
  {
    port_index_left = node->get_row();
    port_index_right = node->get_row();
  }

  for (const auto &it : port_labels_left)
  {
    std::string port_id{generate_port_key_string(node_key_str, PortOrientation::LEFT, port_index_left)};
    if (this->ports.contains(port_id))
    {
      throw std::runtime_error("Attempting to overwrite port! add_node_ports() graph.cpp");
    }
    this->port_ids_left_.push_back(port_id);
    this->ports[port_id] = std::make_unique<Port>(x_left, y_left, this->port_config_.port_width,
                                                  this->port_config_.port_height, it, node_key_test,
                                                  PortType::INPUT, PortOrientation::LEFT);

    node_export.ports_left_.push_back(add_port_export(x_left, y_left, it));
    y_left +=
        this->port_config_.port_height + this->layout_config_.port_spacing;
    port_index_left++;
  }

  for (const auto &it : port_labels_right)
  {
    double x_right{};
    if (node_orientation == NodeOrientation::CENTER)
    {
      x_right = x_left + (this->central_node_config_.width) -
                this->port_config_.port_width;
    }
    else
    {
      x_right = x_left + (this->node_config_.width / 2);
    }
    std::string port_id{generate_port_key_string(node_key_str, PortOrientation::RIGHT, port_index_right)};
    if (this->ports.contains(port_id))
    {
      throw std::runtime_error("Attempting to overwrite port! add_node_ports() graph.cpp");
    }
    this->port_ids_right_.push_back(port_id);
    this->ports[port_id] = std::make_unique<Port>(x_right, y_right, this->port_config_.port_width,
                                                  this->port_config_.port_height, it, node_key_test,
                                                  PortType::OUTPUT, PortOrientation::RIGHT),
    node_export.ports_right_.push_back(add_port_export(x_right, y_right, it));
    y_right +=
        this->port_config_.port_height + this->layout_config_.port_spacing;
    port_index_right++;
  }
}

PortExport Graph::add_port_export(double x, double y, std::string port_label)
{
  std::string export_id{generate_export_key(this->key_size)};
  export_id.append("-" + std::to_string(this->total_node_count_++));

  auto port_export{PortExport()};
  port_export.x = x;
  port_export.y = y;
  port_export.width = this->port_config_.port_width;
  port_export.height = this->port_config_.port_height;
  port_export.label = port_label;
  port_export.source_id = export_id;
  return port_export;
}

// External PYBIND11 Function
void Graph::add_node(
    const std::unordered_map<std::string, std::string> &node_meta_data,
    const std::vector<std::string> &port_labels_left,
    const std::vector<std::string> &port_labels_right,
    const std::vector<int> connection_indexes_left,
    const std::vector<int> connection_indexes_right)
{
  verify_node_meta_key(node_meta_data);

  NodeType node_type{verify_node_type(node_meta_data.at("node-type"))};
  NodeOrientation node_orientation{
      verify_node_orientation(node_meta_data.at("node-orientation"))
  };

  if (node_type == NodeType::SPAN)
  {
    add_node_spanning(node_orientation);
    return;
  }
  else
  {
    const double max_ports{
        get_max_ports(static_cast<double>(port_labels_left.size()),
                      static_cast<double>(port_labels_right.size()))};
    NodeKey key{};
    std::string external_key{};
    if (node_orientation == NodeOrientation::LEFT)
    {
      key = add_node_left_justified(max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = generate_node_key_string(key.orientation, key.column, key.row);
      this->node_keys_left_.push_back(external_key);
    }
    else if (node_orientation == NodeOrientation::RIGHT)
    {
      key = add_node_right_justified(max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = generate_node_key_string(key.orientation, key.column, key.row);
      this->node_keys_right_.push_back(external_key);
    }
    else
    {
      key = add_node_center_justified(max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = generate_node_key_string(key.orientation, key.column, key.row);
    }
    std::cout << "Export Key: " << external_key << "\n";
    add_node_export(key);
    add_node_ports(key, port_labels_left, port_labels_right, node_orientation);
    this->node_keys_master_.push_back(external_key);
  }
}

void Graph::add_node_spanning(NodeOrientation node_orientation)
{
  if (node_orientation == NodeOrientation::LEFT)
    {
      increment_grid_column_left();
      if (this->row_count_left == 0 && this->column_count_left > 0)
      {
        this->base_y_left = this->layout_config_.base_y;
      }
      else
      {
        increment_y_left(this->node_config_.height);
      }
      return;
    }
    else
    {
      increment_grid_column_right();
      if (this->row_count_right == 0 && this->column_count_right > 0)
      {
        this->base_y_right = this->layout_config_.base_y;
      }
      else
      {
        increment_y_right(this->node_config_.height);
      }
      return;
    }
}

NodeKey Graph::add_node_left_justified(const double max_ports, 
                                    NodeType node_type, 
                                    const std::string& node_label, 
                                    std::vector<int> connection_indexes_left, 
                                    std::vector<int> connection_indexes_right)
{
  NodeOrientation node_orientation{NodeOrientation::LEFT};
  double node_width {this->node_config_.width};
  double node_height {verify_node_height(max_ports)};
  double x {calculate_x_left()};
  double y {this->base_y_left};

  NodeKey test_key{'L', this->column_count_left, this->row_count_left};
  this->nodes_test_[test_key] = std::make_unique<Node>(
      x, y, node_width, node_height, node_type, node_orientation, node_label);

  auto &curr_node{this->nodes_test_.at(test_key)};
  curr_node->set_connection_indexes_left(connection_indexes_left);
  curr_node->set_connection_indexes_right(connection_indexes_right);
  curr_node->set_column(this->column_count_left);
  curr_node->set_row(this->row_count_left);

  increment_grid_column_left();
  increment_y_left(this->node_config_.height);
  return test_key;
}

NodeKey Graph::add_node_right_justified(const double max_ports, 
                                     NodeType node_type, 
                                     const std::string& node_label, 
                                     std::vector<int> connection_indexes_left, 
                                     std::vector<int> connection_indexes_right)
{
    NodeOrientation node_orientation {NodeOrientation::RIGHT};
    double node_width {this->node_config_.width};
    double node_height {verify_node_height(max_ports)};
    double x {calculate_x_right(this->central_node_config_.width)};
    double y {this->base_y_right};

    NodeKey test_key{'R', this->column_count_right, this->row_count_right};
    this->nodes_test_[test_key] = std::make_unique<Node>(
        x, y, node_width, node_height, node_type, node_orientation, node_label);

    auto &curr_node{this->nodes_test_.at(test_key)};
    curr_node->set_connection_indexes_left(connection_indexes_left);
    curr_node->set_connection_indexes_right(connection_indexes_right);
    curr_node->set_column(this->column_count_right);
    curr_node->set_row(this->row_count_right);

    increment_grid_column_right();
    increment_y_right(this->node_config_.height);
    return test_key;
}

NodeKey Graph::add_node_center_justified(const double max_ports, 
                                      NodeType node_type, 
                                      const std::string& node_label, 
                                      std::vector<int> connection_indexes_left, 
                                      std::vector<int> connection_indexes_right)
{
    NodeOrientation node_orientation{NodeOrientation::CENTER};
    double node_height {verify_node_height(max_ports)};
    double x {this->layout_config_.base_x};
    double y {this->layout_config_.base_y};

    NodeKey test_key{'C', this->central_node_count++, 0};
    this->nodes_test_[test_key] = std::make_unique<Node>(
        x, y, this->central_node_config_.width, node_height, node_type, node_orientation, node_label);

    auto &curr_node{this->nodes_test_.at(test_key)};
    curr_node->set_connection_indexes_left(connection_indexes_left);
    curr_node->set_connection_indexes_right(connection_indexes_right);
    return test_key;
}

void Graph::add_node_export(NodeKey node_key)
{
  const auto &node{this->nodes_test_.at(node_key)};

  std::string export_id{generate_export_key(this->key_size)};
  export_id.append("-" + std::to_string(this->total_node_count_++));

  NodeExport node_export{};
  node_export.x = node->get_x();
  node_export.y = node->get_y();
  node_export.width = node->get_width();
  node_export.height = node->get_height();
  node_export.name = node->get_label();
  node_export.source_id = export_id;

  LabelExport label{};
  label.x = node_export.x;
  label.y = node_export.y;

  if (node->get_node_orientation() == NodeOrientation::CENTER)
  {
    label.width = this->central_node_config_.width;
  }
  else
  {
    label.width = this->node_config_.width;
  }

  label.height = this->node_config_.label_height;
  label.name = node_export.name;

  node_export.label = label;
  std::string node_key_str{generate_node_key_string(node_key.orientation, node_key.column, node_key.row)};
  this->node_exports_[node_key_str] = node_export;
}

void Graph::add_link_outgoing()
{
  for (auto it : this->port_ids_right_)
  {
    const auto &outgoing_port{this->ports.at(it)};
    const auto &parent_node{this->nodes_test_.at(outgoing_port->get_parent_id())};
    NodeOrientation node_orientation{parent_node->get_node_orientation()};
    PortOrientation port_orientation{outgoing_port->get_port_orientation()};

    std::string incoming_port_id{get_adjacent_port_key_string(it, port_orientation, node_orientation)};

    if (this->outgoing_links_.contains(it))
    {
      throw std::runtime_error("Attempt to overwrite outgoing Port ID!");
    }
    if (this->ports.contains(incoming_port_id))
    {
      auto &incoming_port{this->ports.at(incoming_port_id)};
      this->outgoing_links_[it] = std::make_unique<Link>();

      auto &link{this->outgoing_links_.at(it)};
      link->add_link(it, incoming_port_id,
                     outgoing_port->get_x(), outgoing_port->get_y(),
                     incoming_port->get_x(), incoming_port->get_y());
      this->add_link_export(outgoing_port->get_x(), outgoing_port->get_y(),
                            incoming_port->get_x(), incoming_port->get_y(),
                            link->has_waypoints, link->vec_waypoint_links);
    }
  }
}

void Graph::add_link_export(double src_x, double src_y, double tgt_x,
                            double tgt_y, bool has_waypoints,
                            std::vector<WaypointLinks> waypoints)
{
  std::string export_id{generate_export_key(this->key_size)};
  LinkExport link_export{};
  link_export.source_x = src_x + this->port_config_.port_width;
  link_export.source_y = src_y + this->port_config_.port_height / 2.0;
  link_export.target_x = tgt_x;
  link_export.target_y = src_y + this->port_config_.port_height / 2.0;
  if (has_waypoints)
  {
    link_export.has_waypoints = true;
    link_export.waypoints = waypoints;
  }
  this->link_exports_.push_back(link_export);
}

// void Graph::debug_print_node_data() const
// {
//   for (const auto &id : this->node_keys_master_)
//   {
//     const auto &node{this->nodes_test_.at(id)};
//     std::cout << "\nNode     ID: " << id << "\n";
//     printf("Node      x: %.2f\n", node->get_x());
//     printf("Node      y: %.2f\n", node->get_y());
//     printf("Node  width: %.2f\n", node->get_width());
//     printf("Node height: %.2f\n", node->get_height());
//     printf("\n======================\n");
//   }
// }

Graph::Graph(const LayoutConfig &layout_config, const GridConfig &grid_config,
             const CentralNodeConfig &central_node_config,
             const NodeConfig &node_config, const PortConfig &port_config)
{
  this->layout_config_ = layout_config;
  this->grid_config_ = grid_config;
  this->central_node_config_ = central_node_config;
  this->node_config_ = node_config;
  this->port_config_ = port_config;

  this->base_y_left = this->layout_config_.base_y;
  this->base_x_left = this->layout_config_.base_x;
  this->base_y_right = this->layout_config_.base_y;
  this->base_x_right = this->layout_config_.base_x;
}
