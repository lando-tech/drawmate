//
// Created by landotech on 5/16/25.
//

#include <iostream>
#include "node.h"

Node::Node(const double x, const double y, const double width, const double height, const NodeType node_type, NodeOrientation node_orientation, const std::string& label)
{
    this->set_x(x);
    this->set_y(y);
    this->set_width(width);
    this->set_height(height);
    this->node_type = node_type;
    this->node_orientation_ = node_orientation;
    this->label = label;
}

void Node::set_node_pointers(const std::string& left_id, const std::string& right_id)
{
    this->left_node_id_ = left_id;
    this->right_node_id_ = right_id;
}

void Node::add_port_left(const std::string& port_id)
{
    this->port_ids_left_.push_back(port_id);
}

void Node::add_port_right(const std::string& port_id)
{
    this->port_ids_right_.push_back(port_id);
}

unsigned long Node::get_port_count_left() const
{
    return this->port_ids_left_.size();
}

unsigned long Node::get_port_count_right() const
{
    return this->port_ids_right_.size();
}

unsigned long Node::get_total_port_count() const
{
    return get_port_count_left() + get_port_count_right();
}
