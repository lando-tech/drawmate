//
// Created by landotech on 5/16/25.
//

#include <iostream>
#include "node.h"

Node::Node(const double x, const double y, const double width, const double height, const NodeType node_type)
{
    this->set_x(x);
    this->set_y(y);
    this->set_width(width);
    this->set_height(height);
    this->node_type = node_type;
}

void Node::set_node_pointers(const std::string& left_id, const std::string& right_id)
{
    this->left_node_id_ = left_id;
    this->right_node_id_ = right_id;
}

void Node::add_port_left(std::unique_ptr<Port> port, const int port_key)
{
    if ( this->ports_left.count(port_key) == 1)
    {
        std::cout << "Key already exists!\n";
        return;
    }
    this->ports_left[port_key] = std::move(port);
}

void Node::add_port_right(std::unique_ptr<Port> port, const int port_key)
{
    if ( this->ports_right.count(port_key) == 1 )
    {
        std::cout << "Key already exists!\n";
        return;
    }
    this->ports_right[port_key] = std::move(port);
}

unsigned long Node::get_port_count_left() const
{
    return this->ports_left.size();
}

unsigned long Node::get_port_count_right() const
{
    return this->ports_right.size();
}

unsigned long Node::get_total_port_count() const
{
    return get_port_count_left() + get_port_count_right();
}

Port& Node::get_port_ref_left(const int port_key)
{
    const auto it = this->ports_left.find(port_key);
    if ( it == this->ports_left.end() )
    {
        throw std::runtime_error("Port not found!" + port_key);
    }

    return *(it->second);
}

Port& Node::get_port_ref_right(const int port_key)
{
    const auto it = this->ports_right.find(port_key);
    if ( it == this->ports_right.end() )
    {
        throw std::runtime_error("Port not found!" + port_key);
    }

    return *(it->second);
}
