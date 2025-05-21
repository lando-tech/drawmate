#include "label_node.h"

LabelNode::LabelNode(const double x, const double y, const double width, const double height, const std::string &name)
{
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->name = name;
}
