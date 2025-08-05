#ifndef DRAWMATE_NODE_SPEC_H
#define DRAWMATE_NODE_SPEC_H
#include <string>
#include <vector>

enum class NodeType {
    GENERAL_APPLIANCE,
    AUDIO_MATRIX,
    VIDEO_MATRIX,
    AUDIO_CODEC,
    VIDEO_CODEC,
    SWITCH,
    ROUTER,
};

enum class NodeShape {
    RECT,
    CIRCLE,
    TRIANGLE,
    DIAMOND,
    CYLINDER
};

enum class NodeOrientation {
    LEFT,
    RIGHT,
    CENTER
};

struct DrawmateNodeSpec {
    std::string m_node_label{};
    NodeType m_type{};
    NodeShape m_shape{};
};

struct DrawmatePortSpec {
    std::string m_input_label{};
    std::string m_output_label{};
    NodeShape m_shape{};
};

#endif
