//
// Created by landotech on 5/16/25.
//

#ifndef NODE_H
#define NODE_H

#include <memory>
#include <unordered_map>
#include "graph_object.h"
#include "label_node.h"
#include "port.h"

enum class NodeType
{
    VIDEO_MATRIX,
    VIDEO_CODEC,
    AUDIO_MATRIX,
    AUDIO_CODEC,
    PC,
    LAPTOP,
    APPLIANCE,
};

enum class NodeOrientation
{
    LEFT,
    RIGHT,
    CENTER,
};

class Node : public GraphObject
{
    NodeType node_type{};
    NodeOrientation node_orientation_{};
    std::string left_node_id_{};
    std::string right_node_id_{};
    std::unique_ptr<LabelNode> label{};
    std::unordered_map<int, std::unique_ptr<Port> > ports_left{};
    std::unordered_map<int, std::unique_ptr<Port>> ports_right{};
    std::string style{};

public:
    Node(double x, double y, double width, double height, NodeType node_type);

    void set_node_type(const NodeType node_type) { this->node_type = node_type; }

    void set_style(const std::string& style) { this->style = style; }

    void set_node_pointers(const std::string& left_id, const std::string& right_id);

    void set_node_label(std::unique_ptr<LabelNode> label) { this->label = std::move(label); }

    NodeType get_node_type() const { return this->node_type; }

    std::string get_style() { return this->style; }

    std::string get_label() const { return this->label->get_name(); };

    void add_port_left(std::unique_ptr<Port> port, int port_key);
    void add_port_right(std::unique_ptr<Port> port, int port_key);

    unsigned long get_port_count_left() const;
    unsigned long get_port_count_right() const;
    unsigned long get_total_port_count() const;
    Port& get_port_ref_left(int port_key);
    Port& get_port_ref_right(int port_key);

};

#endif //NODE_H
