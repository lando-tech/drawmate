#ifndef DRAWMATE_NODE_SPEC_H
#define DRAWMATE_NODE_SPEC_H
#include <string>

enum class NodeOrientation {
    LEFT,
    RIGHT,
    CENTER
};

enum class NodeType {
    AUDIO_MATRIX,
    VIDEO_MATRIX,
    AUDIO_CODEC,
    VIDEO_CODEC,
    PC,
    SWITCH,
    ROUTER,
    MICROPHONE,
    CPU,
    GPU
};

enum class NodeShape {
    RECT,
    CIRCLE,
    TRIANGLE,
    DIAMOND,
    CYLINDER
};

struct DrawmateNodeSpec {
    std::string m_node_label{};
    NodeType m_domain{};
    NodeOrientation m_orientation{};
};

#endif
