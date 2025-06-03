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
  double actual_height{
      (this->port_config_.port_height * port_count) +
      (this->layout_config_.port_spacing * (port_count - 1)) +
      (this->node_config_.label_height + this->port_config_.port_height)};

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
      verify_node_orientation(node_meta_data.at("node-orientation"))};
  
  if (this->nodes_.empty() && node_orientation != NodeOrientation::CENTER)
  {
    throw std::runtime_error("First node must be center aligned!");
  }

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
    NodeKey internal_key{};
    std::string external_key{};
    if (node_orientation == NodeOrientation::LEFT)
    {
      internal_key = add_node_left_justified(
          max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = convert_node_key_internal(internal_key);
      this->node_keys_left_external.push_back(external_key);
    }
    else if (node_orientation == NodeOrientation::RIGHT)
    {
      internal_key = add_node_right_justified(
          max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = convert_node_key_internal(internal_key);
      this->node_keys_right_external.push_back(external_key);
    }
    else
    {
      internal_key = add_node_center_justified(
          max_ports, node_type, node_meta_data.at("node-label"), connection_indexes_left, connection_indexes_right);
      external_key = convert_node_key_internal(internal_key);
    }
    add_node_export(internal_key, external_key);
    add_node_ports(internal_key, external_key, port_labels_left, port_labels_right, node_orientation);
    this->node_keys_master_external.push_back(external_key);
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
                                       const std::string &node_label,
                                       std::vector<int> connection_indexes_left,
                                       std::vector<int> connection_indexes_right)
{
  NodeOrientation node_orientation{NodeOrientation::LEFT};
  double node_width{this->node_config_.width};
  double node_height{verify_node_height(max_ports)};
  double x{calculate_x_left()};
  double y{this->base_y_left};

  NodeKey test_key{'L', this->column_count_left, this->row_count_left};
  this->nodes_[test_key] = std::make_unique<Node>(
      x, y, node_width, node_height, node_type, node_orientation, node_label);

  auto &curr_node{this->nodes_.at(test_key)};
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
                                        const std::string &node_label,
                                        std::vector<int> connection_indexes_left,
                                        std::vector<int> connection_indexes_right)
{
  NodeOrientation node_orientation{NodeOrientation::RIGHT};
  double node_width{this->node_config_.width};
  double node_height{verify_node_height(max_ports)};
  double x{calculate_x_right(this->central_node_config_.width)};
  double y{this->base_y_right};

  NodeKey test_key{'R', this->column_count_right, this->row_count_right};
  this->nodes_[test_key] = std::make_unique<Node>(
      x, y, node_width, node_height, node_type, node_orientation, node_label);

  auto &curr_node{this->nodes_.at(test_key)};
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
                                         const std::string &node_label,
                                         std::vector<int> connection_indexes_left,
                                         std::vector<int> connection_indexes_right)
{
  NodeOrientation node_orientation{NodeOrientation::CENTER};
  double node_height{verify_node_height(max_ports)};
  double x{this->layout_config_.base_x};
  double y{this->layout_config_.base_y};

  NodeKey test_key{'C', this->central_node_count++, 0};
  this->nodes_[test_key] = std::make_unique<Node>(
      x, y, this->central_node_config_.width, node_height, node_type, node_orientation, node_label);

  auto &curr_node{this->nodes_.at(test_key)};
  curr_node->set_connection_indexes_left(connection_indexes_left);
  curr_node->set_connection_indexes_right(connection_indexes_right);
  return test_key;
}

void Graph::add_node_export(NodeKey node_key_internal, const std::string& node_key_external)
{
  if (this->nodes_.contains(node_key_internal))
  {
    const auto &node{this->nodes_.at(node_key_internal)};
    std::string node_export_id{generate_export_key(this->key_size)};
    node_export_id.append("-" + std::to_string(this->total_node_count_++));

    std::string label_export_id{generate_export_key(this->key_size)};
    label_export_id.append("-" + std::to_string(this->total_node_count_++));

    NodeExport node_export{};
    node_export.x = node->get_x();
    node_export.y = node->get_y();
    node_export.width = node->get_width();
    node_export.height = node->get_height();
    node_export.name = node->get_label();
    node_export.source_id = node_export_id;

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
    label.source_id = label_export_id;

    node_export.label = label;
    this->node_exports_[node_key_external] = node_export;
  }
  else
  {
    throw std::runtime_error("Error at <add_node_export>, key does not exist");
  }
}

void Graph::add_node_ports(NodeKey node_key,
                           const std::string& node_key_external,
                           const std::vector<std::string> &port_labels_left,
                           const std::vector<std::string> &port_labels_right,
                           NodeOrientation node_orientation)
{
  const auto &node{this->nodes_.at(node_key)};
  auto &node_export{this->node_exports_.at(node_key_external)};

  double x_left{node->get_x()};
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

  add_node_ports_left_justified(
      port_labels_left, node_key, x_left, y_left, node_export, port_index_left);
  add_node_ports_right_justified(
      port_labels_right, node_key, x_right, y_right, node_export, port_index_right);
}

void Graph::add_node_ports_left_justified(std::vector<std::string> port_labels,
                                          const NodeKey node_key,
                                          double x_left,
                                          double y_left,
                                          NodeExport &node_export,
                                          int port_index)
{
  for (const auto &it : port_labels)
  {
    PortKey port_key{node_key.orientation, 'L', node_key.column, port_index};
    this->ports_[port_key] = std::make_unique<Port>(x_left, y_left, this->port_config_.port_width,
                                                         this->port_config_.port_height, it, node_key,
                                                         PortType::INPUT, PortOrientation::LEFT);
    this->port_ids_left_.push_back(port_key);
    this->port_exports_[convert_port_key_internal(port_key)] = add_port_export(x_left, y_left, it);
    y_left +=
        this->port_config_.port_height + this->layout_config_.port_spacing;
    port_index++;
  }
}

void Graph::add_node_ports_right_justified(std::vector<std::string> port_labels,
                                           const NodeKey node_key,
                                           double x_right,
                                           double y_right,
                                           NodeExport &node_export,
                                           int port_index)
{
  for (const auto &it : port_labels)
  {
    PortKey port_key{node_key.orientation, 'R', node_key.column, port_index};
    this->ports_[port_key] = std::make_unique<Port>(x_right, y_right, this->port_config_.port_width,
                                                         this->port_config_.port_height, it, node_key,
                                                         PortType::INPUT, PortOrientation::LEFT);
    this->port_ids_right_.push_back(port_key);
    this->port_exports_[convert_port_key_internal(port_key)] = add_port_export(x_right, y_right, it);
    y_right +=
        this->port_config_.port_height + this->layout_config_.port_spacing;
    port_index++;
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

void Graph::add_link_outgoing()
{
  for (auto it : this->port_ids_right_)
  {
    const auto &outgoing_port{this->ports_.at(it)};
    const auto &parent_node{this->nodes_.at(outgoing_port->get_parent_id())};

    NodeOrientation node_orientation{parent_node->get_node_orientation()};
    PortOrientation port_orientation{outgoing_port->get_port_orientation()};

    PortKey incoming_port_id{get_adjacent_port_key(it)};
    if (this->outgoing_links_.contains(it))
    {
      throw std::runtime_error("Attempt to overwrite outgoing Port ID!");
    }
    if (this->ports_.contains(incoming_port_id))
    {
      add_port_target_id(it, incoming_port_id);
      auto &incoming_port{this->ports_.at(incoming_port_id)};
      this->outgoing_links_[it] = std::make_unique<Link>();

      auto &link{this->outgoing_links_.at(it)};
      link->add_link(it, incoming_port_id,
                     outgoing_port->get_x(), outgoing_port->get_y(),
                     incoming_port->get_x(), incoming_port->get_y());
      link->set_link_label(it.column, it.row, node_orientation, port_orientation);
      this->add_link_export(convert_port_key_internal(it), convert_port_key_internal(incoming_port_id),
                            link->label, 
                            outgoing_port->get_x(), outgoing_port->get_y(),
                            incoming_port->get_x(), incoming_port->get_y(),
                            link->has_waypoints, link->vec_waypoint_links);
    }
  }
}

void Graph::add_port_target_id(PortKey source_port_key, PortKey target_port_key)
{
  auto& source_port {this->port_exports_.at(convert_port_key_internal(source_port_key))};
  auto& target_port {this->port_exports_.at(convert_port_key_internal(target_port_key))};
  source_port.target_id = target_port.source_id;
}

void Graph::add_link_export(const std::string& source_id, const std::string& target_id, 
                            const std::string& label,
                            double src_x, double src_y, double tgt_x,
                            double tgt_y, bool has_waypoints,
                            std::vector<WaypointLinks> waypoints)
{
  std::string export_id{generate_export_key(this->key_size)};
  export_id.append("-" + std::to_string(this->total_node_count_++));
  LinkExport link_export{};
  link_export.source_x = src_x + this->port_config_.port_width;
  link_export.source_y = src_y + this->port_config_.port_height / 2.0;
  link_export.target_x = tgt_x;
  link_export.target_y = src_y + this->port_config_.port_height / 2.0;
  link_export.source_id = source_id;
  link_export.target_id = target_id;
  link_export.label = label;
  link_export._id = export_id;
  if (has_waypoints)
  {
    link_export.has_waypoints = true;
    link_export.waypoints = waypoints;
  }
  this->link_exports_.push_back(link_export);
}

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
