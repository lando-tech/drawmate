#ifndef DRAWMATE_GRAPH_H
#define DRAWMATE_GRAPH_H

#include "abstract_layout_manager.h"
#include "drawmate_node.h"
#include "drawmate_edge.h"

#include <map>
#include <memory>

class DrawmateGraph {

private:
    std::map<long, std::unique_ptr<AbstractDrawmateNode>> m_node_map{};
    std::map<long, std::unique_ptr<DrawmateEdge>> m_edge_map{};

public:

    DrawmateGraph(AbstractLayoutManager layout_manager);

    // Node operations
    void add_node(AbstractDrawmateNode &&node);
    void remove_node(long node_key);
    [[nodiscard]] AbstractDrawmateNode& get_node_ref(long node_key);
    [[nodiscard]] const AbstractDrawmateNode& get_node_const_ref(long node_key) const;
    [[nodiscard]] bool has_node(long node_key) const;
    [[nodiscard]] size_t get_node_count() const;

    // Edge operations
    void add_edge(DrawmateEdge &&edge);
    void remove_edge(long edge_id);
    [[nodiscard]] DrawmateEdge& get_edge_ref(long edge_id);
    [[nodiscard]] const DrawmateEdge& get_edge_const_ref(long edge_id) const;
    [[nodiscard]] bool has_edge(long edge_id) const;
    [[nodiscard]] size_t get_edge_count() const;

    // Container access
    [[nodiscard]] const std::map<long, std::unique_ptr<AbstractDrawmateNode>>& get_nodes() const;
    [[nodiscard]] const std::map<long, std::unique_ptr<DrawmateEdge>>& get_edges() const;

    // Clear operations
    void clear_nodes();
    void clear_edges();
    void clear_all();

};

#endif // DRAWMATE_GRAPH_H
