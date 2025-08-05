#ifndef DRAWMATE_EDGE_H
#define DRAWMATE_EDGE_H

#include "drawmate_waypoint.h"
#include <vector>
#include <memory>

class DrawmateEdge {

private:
    long m_id{};
    long m_source_id{};
    long m_target_id{};
    std::vector<std::unique_ptr<DrawmateWaypoint>> m_waypoints{};

public:
    // Constructors
    DrawmateEdge() = default;
    DrawmateEdge(long id, long source_id, long target_id)
        : m_id(id), m_source_id(source_id), m_target_id(target_id) {}

    // Getters
    [[nodiscard]] long get_id() const { return m_id; }
    [[nodiscard]] long get_source_id() const { return m_source_id; }
    [[nodiscard]] long get_target_id() const { return m_target_id; }

    // Setters
    void set_id(long id) { m_id = id; }
    void set_source_id(long source_id) { m_source_id = source_id; }
    void set_target_id(long target_id) { m_target_id = target_id; }

    // Waypoint operations
    void add_waypoint(std::unique_ptr<DrawmateWaypoint> waypoint);
    void remove_waypoint(long waypoint_id);
    [[nodiscard]] DrawmateWaypoint& get_waypoint_ref(long waypoint_id);
    [[nodiscard]] const DrawmateWaypoint& get_waypoint_const_ref(long waypoint_id) const;
    [[nodiscard]] bool has_waypoint(long waypoint_id) const;
    [[nodiscard]] size_t get_waypoint_count() const;
    [[nodiscard]] const std::vector<std::unique_ptr<DrawmateWaypoint>>& get_waypoints() const;
    void clear_waypoints();

};

#endif
