#ifndef DRAWMATE_NODE_BUILDER_H
#define DRAWMATE_NODE_BUILDER_H
#include "abstract_drawmate_node.h"
#include "drawmate_node_spec.h"
#include <memory>

class DrawmateNodeBuilder {

private:

public:
    std::unique_ptr<AbstractDrawmateNode> build_node(NodeType node_type);
    std::unique_ptr<AbstractDrawmateNode> build_node(NodeType node_type, NodeOrientation orientation);
    std::unique_ptr<AbstractDrawmateNode> build_node(
        NodeType node_type, NodeOrientation orientation, NodeShape node_shape);

};

#endif
