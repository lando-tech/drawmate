#include "drawmate_node_builder.h"
#include "drawmate_multiport_nodes.h"

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node(DrawmateNodeSpec node_spec) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    node->set_label(node_spec.m_node_label);
    return node;
}

std::unique_ptr<DrawmateMultiPortNode> DrawmateNodeBuilder::build_node_grid_based(DrawmateNodeSpec node_spec, NodeOrientation orientation) {
    auto node {this->get_node_by_type(node_spec.m_type)};
    node->set_label(node_spec.m_node_label);
    node->set_node_orientation(orientation);
    return node;
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
