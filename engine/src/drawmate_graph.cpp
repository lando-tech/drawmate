#include "drawmate_graph.h"
#include "drawmate_node.h"


void DrawmateGraph::add_node(AbstractDrawmateNode &&node) {
    long node_id {node.get_id()};
    if (this->m_node_map.contains(node_id)) {
        throw std::runtime_error("Node already exists!");
    }
    this->m_node_map.emplace(node_id, node);  
}

void DrawmateGraph::remove_node(long node_key) {
    if (this->m_node_map.contains(node_key)) {
        this->m_node_map.erase(node_key);
    } else {
        throw std::runtime_error("Unable to remove node!");
    }
}

