#ifndef DRAWMATE_GRAPH_H
#define DRAWMATE_GRAPH_H

#include "keys.h"
#include "drawmate_node.h"
#include "drawmate_port.h"
#include "drawmate_edge.h"

#include <map>
#include <memory>

class DrawmateGraph {

private:
    std::map<NodeKey, std::unique_ptr<AbstractDrawmateNode>> m_node_map{};
    std::map<long, std::unique_ptr<DrawmateEdge>> m_edge_map{};
    std::map<PortKey, std::unique_ptr<AbstractDrawmatePort>> m_port_map{};

public:

    // Node operations
    void add_node(AbstractDrawmateNode &&node);
    void remove_node(NodeKey node_key);
    AbstractDrawmateNode& get_node_ref(NodeKey node_key);
    const AbstractDrawmateNode& get_node_const_ref(NodeKey node_key) const;
    bool has_node(NodeKey node_key) const;
    size_t get_node_count() const;

    // Edge operations
    void add_edge(DrawmateEdge &&edge);
    void remove_edge(long edge_id);
    DrawmateEdge& get_edge_ref(long edge_id);
    const DrawmateEdge& get_edge_const_ref(long edge_id) const;
    bool has_edge(long edge_id) const;
    size_t get_edge_count() const;

    // Port operations
    void add_port(AbstractDrawmatePort &&port);
    void remove_port(PortKey port_key);
    AbstractDrawmatePort& get_port_ref(PortKey port_key);
    const AbstractDrawmatePort& get_port_const_ref(PortKey port_key) const;
    bool has_port(PortKey port_key) const;
    size_t get_port_count() const;

    // Container access
    const std::map<NodeKey, std::unique_ptr<AbstractDrawmateNode>>& get_nodes() const;
    const std::map<long, std::unique_ptr<DrawmateEdge>>& get_edges() const;
    const std::map<PortKey, std::unique_ptr<AbstractDrawmatePort>>& get_ports() const;

    // Clear operations
    void clear_nodes();
    void clear_edges();
    void clear_ports();
    void clear_all();

};

#endif // DRAWMATE_GRAPH_H
