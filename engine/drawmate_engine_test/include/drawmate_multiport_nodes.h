
#ifndef DRAWMATE_MULTIPORT_NODES_H
#define DRAWMATE_MULTIPORT_NODES_H
#include "drawmate_node_rect.h"
#include <vector>

class MultiPortNode : public DrawmateNodeRect {

private:
    std::vector<long> m_port_ids_input{};
    std::vector<long> m_port_ids_output{};

public:
    [[nodiscard]] const std::vector<long>& get_port_ids_input() const { return this->m_port_ids_input; }
    void add_input_port(long port_id) { this->m_port_ids_input.push_back(port_id); }

    [[nodiscard]] const std::vector<long>& get_port_ids_output() const {return this->m_port_ids_output; }
    void add_output_port(long port_id) { this->m_port_ids_output.push_back(port_id); }
};

class SwitchNode : public MultiPortNode {


};

class AudioMatrixNode : public MultiPortNode {

};

class VideoMatrixNode : public MultiPortNode {

};

class AudioCodecNode: public MultiPortNode {

};

class VideoCodecNode: public MultiPortNode {

};

#endif
