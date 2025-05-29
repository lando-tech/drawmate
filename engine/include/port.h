//
// Created by landotech on 5/16/25.
//

#ifndef PORT_H
#define PORT_H
#include <iostream>
#include "keys.h"
#include "graph_object.h"

class Node;

enum class PortType
{
    INPUT,
    OUTPUT,
};

enum class PortOrientation
{
    LEFT,
    RIGHT,
};

class Port : public GraphObject
{
    NodeKey parent_node_id_{};
    PortType port_type{};
    PortOrientation port_orientation_{};
    std::string label{};

    friend class Link;

public:
    Port(double x, double y, int width, int height, const std::string &label, NodeKey parent_id, PortType port_type,
         PortOrientation port_orientation);

    void set_parent_id(const NodeKey parent_id) { this->parent_node_id_ = parent_id; }
    void set_port_type(const PortType port_type) { this->port_type = port_type; }
    void set_port_orientation(const PortOrientation port_orientation)
    { this->port_orientation_ = port_orientation; }
    void set_label(const std::string& label) { this->label = label; }

    [[nodiscard]] PortType get_port_type() const { return this->port_type; }
    [[nodiscard]] PortOrientation get_port_orientation() const { return this->port_orientation_; }
    [[nodiscard]] std::string get_port_label() const { return this->label; }
    [[nodiscard]] NodeKey get_parent_id() const { return this->parent_node_id_; }

};

#endif //PORT_H
