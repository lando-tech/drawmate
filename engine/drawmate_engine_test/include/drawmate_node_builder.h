#ifndef DRAWMATE_NODE_BUILDER_H
#define DRAWMATE_NODE_BUILDER_H
#include "abstract_drawmate_node.h"
#include "drawmate_multiport_nodes.h"
#include "drawmate_port_node.h"
#include "drawmate_node_spec.h"
#include <memory>

class DrawmateNodeBuilder {

private:

    std::unique_ptr<DrawmateMultiPortNode> get_node_by_type(NodeType node_type);

public:
    std::unique_ptr<DrawmateMultiPortNode> build_node(DrawmateNodeSpec node_spec);
    std::unique_ptr<DrawmateMultiPortNode> build_node_grid_based(DrawmateNodeSpec node_spec, NodeOrientation orientation);
    std::unique_ptr<DrawmatePortNode> build_node_port(DrawmatePortSpec port_spec);
    std::unique_ptr<DrawmatePortNode> build_node_port_grid_based(DrawmatePortSpec, NodeOrientation orientation);

};

#endif
