//
// Created by landotech on 5/16/25.
//

#ifndef NODE_H
#define NODE_H

#include "graph_object.h"
#include "port.h"
#include <memory>
#include <unordered_map>
#include <vector>

enum class NodeType {
  SPAN,
  VIDEO_MATRIX,
  VIDEO_CODEC,
  AUDIO_MATRIX,
  AUDIO_CODEC,
  PC,
  LAPTOP,
  APPLIANCE,
};

enum class NodeOrientation {
  LEFT,
  RIGHT,
  CENTER,
};

class Node : public GraphObject {
  NodeType node_type{};
  NodeOrientation node_orientation_{};
  std::string left_node_id_{};
  std::string right_node_id_{};
  int column{};
  int row{};
  std::string label{};
  std::vector<std::string> port_ids_left_{};
  std::vector<std::string> port_ids_right_{};
  std::vector<int> connection_indexes_left{};
  std::vector<int> connection_indexes_right{};
  std::string style{};

public:
  Node(double x, double y, double width, double height, NodeType node_type,
       NodeOrientation node_orientation, const std::string &label);

  void set_node_type(const NodeType node_type) { this->node_type = node_type; }

  void set_node_orientation(const NodeOrientation node_orientation) {
    this->node_orientation_ = node_orientation;
  }

  void set_style(const std::string &style) { this->style = style; }

  void set_node_pointers(const std::string &left_id,
                         const std::string &right_id);

  void set_node_label(const std::string &label) { this->label = label; }

  void set_left_id(const std::string &left_id) {
    this->left_node_id_ = left_id;
  };

  void set_right_id(const std::string &right_id) {
    this->right_node_id_ = right_id;
  }

  void set_column(const int column) { this->column = column; }

  void set_row(const int row) { this->row = row; }

  void set_connection_indexes_left(std::vector<int> indexes) {
    this->connection_indexes_left = indexes;
  }

  void set_connection_indexes_right(std::vector<int> indexes) {
    this->connection_indexes_right = indexes;
  }

  NodeType get_node_type() const { return this->node_type; }

  NodeOrientation get_node_orientation() const {
    return this->node_orientation_;
  }

  std::string get_style() { return this->style; }

  std::string get_label() const { return this->label; };

  void add_port_left(const std::string& port_id);
  void add_port_right(const std::string& port_id);

  unsigned long get_port_count_left() const;
  unsigned long get_port_count_right() const;
  unsigned long get_total_port_count() const;

  std::vector<int> get_connection_indexes_left() {
    return this->connection_indexes_left;
  }
  std::vector<int> get_connection_indexes_right() {
    return this->connection_indexes_right;
  }

  int get_column() const { return this->column; }
  int get_row() const { return this->row; }

};

#endif // NODE_H
