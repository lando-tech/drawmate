#include "drawmate_graph.h"
#include "abstract_drawmate_node.h"
#include <iostream>


void DrawmateGraph::add_node(std::unique_ptr<AbstractDrawmateNode> node) {
    long node_id {node->get_id()};
    if (this->m_node_map.find(node_id) != this->m_node_map.end()) {
        std::cout << "Node with ID: " << node_id << " does not exist!\n";
        return;
    }
    this->m_node_map.emplace(node_id, std::move(node));
}

void DrawmateGraph::remove_node(long node_key) {
    if (this->m_node_map.find(node_key) != this->m_node_map.end()) {
        this->m_node_map.erase(node_key);
    } else {
        std::cout << "Node with ID: " << node_key << " does not exist!\n";
        return;
    }
}

void DrawmateGraph::add_edge(std::unique_ptr<DrawmateEdge> edge) {
    long edge_id {edge->get_id()};
    if (this->m_edge_map.find(edge_id) != this->m_edge_map.end()) {
        std::cout << "Edge with ID: " << edge_id << " does not exist!\n";
        return;
    }
    this->m_edge_map.emplace(edge_id, std::move(edge));
}

void DrawmateGraph::remove_edge(long edge_key) {
    if (this->m_edge_map.find(edge_key) != this->m_edge_map.end()) {
        this->m_edge_map.erase(edge_key);
    } else {
        std::cout << "Edge with ID: " << edge_key << " does not exist!\n";
        return;
    }
}

const std::map<long, std::unique_ptr<AbstractDrawmateNode>>&
DrawmateGraph::get_nodes() const {
    return this->m_node_map;
}

const std::map<long, std::unique_ptr<DrawmateEdge>>&
DrawmateGraph::get_edges() const {
    return this->m_edge_map;
}

void DrawmateGraph::clear_nodes() {
    this->m_node_map.clear();
}

void DrawmateGraph::clear_edges() {
    this->m_edge_map.clear();
}

void DrawmateGraph::clear_all() {
    this->m_node_map.clear();
    this->m_edge_map.clear();
}
