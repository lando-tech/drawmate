#ifndef DRAWMATE_PORT_NODE_H
#define DRAWMATE_PORT_NODE_H
#include "drawmate_node_rect.h"

class DrawmatePortNode : public DrawmateNodeRect {

private:
    std::string m_input_label{};
    std::string m_output_label{};
    long m_edge_id{};

public:
    // Input label getters/setters
    void set_input_label(const std::string_view &label) { this->m_input_label = label; }
    [[nodiscard]] const std::string& get_input_label() const { return this->m_input_label; }

    // Output label getters/setters
    void set_output_label(const std::string_view &label) { this->m_output_label = label; }
    [[nodiscard]] const std::string& get_output_label() const { return this->m_output_label; }

    // Edge ID getters/setters
    void set_edge_id(long edge_id) { this->m_edge_id = edge_id; }
    [[nodiscard]] long get_edge_id() const { return this->m_edge_id; }
};

#endif
