#ifndef DRAWMATE_NODE_BUILDER_H
#define DRAWMATE_NODE_BUILDER_H
#include "abstract_drawmate_node.h"
#include "drawmate_multiport_nodes.h"
#include "drawmate_port_node.h"
#include "drawmate_node_spec.h"
#include "drawmate_geometry.h"
#include <memory>

class DrawmateNodeBuilder {

private:

    std::unique_ptr<DrawmateMultiPortNode> get_node_by_type(NodeType node_type);

    // Auto configuration methods (builder manages IDs)
    void configure_node_auto(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec);
    void configure_node_auto(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, NodeOrientation orientation);

    // Manual configuration methods (caller provides ID and optionally geometry)
    void configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id);
    void configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, NodeOrientation orientation);
    void configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, const DrawmateGeometry& geometry);
    void configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, NodeOrientation orientation, const DrawmateGeometry& geometry);

    // Legacy configuration methods
    void configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec);
    void configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, NodeOrientation orientation);

    void configure_port(std::unique_ptr<DrawmatePortNode>& port, DrawmatePortSpec port_spec);
    void configure_port(std::unique_ptr<DrawmatePortNode>& port, DrawmatePortSpec port_spec, NodeOrientation orientation);

public:
    // Auto mode - builder manages ID assignment
    std::unique_ptr<DrawmateMultiPortNode> build_node_auto(DrawmateNodeSpec node_spec);
    std::unique_ptr<DrawmateMultiPortNode> build_node_auto(DrawmateNodeSpec node_spec, NodeOrientation orientation);

    // Manual mode - caller provides ID and optionally geometry
    std::unique_ptr<DrawmateMultiPortNode> build_node_manual(DrawmateNodeSpec node_spec, long id);
    std::unique_ptr<DrawmateMultiPortNode> build_node_manual(DrawmateNodeSpec node_spec, long id, NodeOrientation orientation);
    std::unique_ptr<DrawmateMultiPortNode> build_node_manual(DrawmateNodeSpec node_spec, long id, const DrawmateGeometry& geometry);
    std::unique_ptr<DrawmateMultiPortNode> build_node_manual(DrawmateNodeSpec node_spec, long id, NodeOrientation orientation, const DrawmateGeometry& geometry);

    // Legacy methods (redirect to auto mode for backward compatibility)
    std::unique_ptr<DrawmateMultiPortNode> build_node(DrawmateNodeSpec node_spec);
    std::unique_ptr<DrawmateMultiPortNode> build_node_grid_based(DrawmateNodeSpec node_spec, NodeOrientation orientation);

    // Port building methods
    std::unique_ptr<DrawmatePortNode> build_node_port(DrawmatePortSpec port_spec);
    std::unique_ptr<DrawmatePortNode> build_node_port_grid_based(DrawmatePortSpec, NodeOrientation orientation);

};

#endif
