#include "drawmate_node_builder.h"
#include "drawmate_port_node.h"
#include "drawmate_multiport_nodes.h"

// Auto mode - builder manages ID assignment
std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_auto(DrawmateNodeSpec node_spec) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_auto(node, node_spec);
    return node;
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_auto(DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_auto(node, node_spec, orientation);
    return node;
}

// Manual mode - caller provides ID and optionally geometry
std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_manual(DrawmateNodeSpec node_spec, long id) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_manual(node, node_spec, id);
    return node;
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_manual(DrawmateNodeSpec node_spec, long id, NodeOrientation orientation) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_manual(node, node_spec, id, orientation);
    return node;
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_manual(DrawmateNodeSpec node_spec, long id, const DrawmateGeometry& geometry) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_manual(node, node_spec, id, geometry);
    return node;
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_manual(DrawmateNodeSpec node_spec, long id, NodeOrientation orientation, const DrawmateGeometry& geometry) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    this->configure_node_manual(node, node_spec, id, orientation, geometry);
    return node;
}

// Legacy methods - redirect to auto mode for backward compatibility
std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node(DrawmateNodeSpec node_spec) {
    return build_node_auto(node_spec);
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_grid_based(DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    return build_node_auto(node_spec, orientation);
}

std::unique_ptr<DrawmatePortNode> DrawmateNodeBuilder::build_node_port(DrawmatePortSpec port_spec) {
    auto port {std::make_unique<DrawmatePortNode>()};
    this->configure_port(port, port_spec);
    return port;
}

std::unique_ptr<DrawmatePortNode> DrawmateNodeBuilder::build_node_port_grid_based(DrawmatePortSpec port_spec, NodeOrientation orientation) {
    auto port {std::make_unique<DrawmatePortNode>()};
    this->configure_port(port, port_spec, orientation);
    return port;
}

void DrawmateNodeBuilder::configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec) {
    node->set_label(node_spec.m_node_label);
}

void DrawmateNodeBuilder::configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    node->set_label(node_spec.m_node_label);
    node->set_node_orientation(orientation);
}

void DrawmateNodeBuilder::configure_port(std::unique_ptr<DrawmatePortNode>& port, DrawmatePortSpec port_spec) {
    port->set_input_label(port_spec.m_input_label);
    port->set_output_label(port_spec.m_output_label);
}

void DrawmateNodeBuilder::configure_port(std::unique_ptr<DrawmatePortNode>& port, DrawmatePortSpec port_spec, NodeOrientation orientation) {
    port->set_input_label(port_spec.m_input_label);
    port->set_output_label(port_spec.m_output_label);
    port->set_node_orientation(orientation);
}

// Auto configuration methods - builder manages ID assignment
void DrawmateNodeBuilder::configure_node_auto(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec) {
    node->set_label(node_spec.m_node_label);
}

void DrawmateNodeBuilder::configure_node_auto(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    node->set_label(node_spec.m_node_label);
    node->set_node_orientation(orientation);
}

// Manual configuration methods - caller provides ID and optionally geometry
void DrawmateNodeBuilder::configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id) {
    node->set_label(node_spec.m_node_label);
    node->set_id(id);
}

void DrawmateNodeBuilder::configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, NodeOrientation orientation) {
    node->set_label(node_spec.m_node_label);
    node->set_id(id);
    node->set_node_orientation(orientation);
}

void DrawmateNodeBuilder::configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, const DrawmateGeometry& geometry) {
    node->set_label(node_spec.m_node_label);
    node->set_id(id);
    node->set_geometry(geometry);
}

void DrawmateNodeBuilder::configure_node_manual(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, long id, NodeOrientation orientation, const DrawmateGeometry& geometry) {
    node->set_label(node_spec.m_node_label);
    node->set_id(id);
    node->set_node_orientation(orientation);
    node->set_geometry(geometry);
}

// Legacy configuration methods (kept for backward compatibility)
void DrawmateNodeBuilder::configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec) {
    configure_node_auto(node, node_spec);
}

void DrawmateNodeBuilder::configure_node(std::unique_ptr<DrawmateMultiPortNode>& node, DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    configure_node_auto(node, node_spec, orientation);
}


std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::get_node_by_type(NodeType node_type) {
    switch (node_type)
    {
    case NodeType::AUDIO_CODEC:
        return std::make_unique<AudioCodecNode>();
    case NodeType::AUDIO_MATRIX:
        return std::make_unique<AudioMatrixNode>();
    case NodeType::VIDEO_CODEC:
        return std::make_unique<VideoCodecNode>();
    case NodeType::VIDEO_MATRIX:
        return std::make_unique<VideoMatrixNode>();
    case NodeType::ROUTER:
        return std::make_unique<RouterNode>();
    case NodeType::SWITCH:
        return std::make_unique<SwitchNode>();
    case NodeType::GENERAL_APPLIANCE:
        return std::make_unique<GeneralApplianceNode>();
    default:
        throw std::runtime_error("Unknown argument for node type");
    }
}
