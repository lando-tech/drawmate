//
// Created by landotech on 5/16/25.
//

#ifndef LABEL_NODE_H
#define LABEL_NODE_H
#include "graph_object.h"
#include <string>

class Node;

class LabelNode : public GraphObject
{
    Node* parent_node_{};
    std::string name{};

public:
    LabelNode(double x, double y, double width, double height, const std::string& name);
    void set_parent_node(Node* parent_node) { this->parent_node_ = parent_node; }
    void set_name(const std::string& name) { this->name = name; }
    std::string get_name() { return this->name; }
};

#endif //LABEL_NODE_H
