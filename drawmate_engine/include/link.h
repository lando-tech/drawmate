//
// Created by landotech on 5/16/25.
//

#ifndef LINK_H
#define LINK_H
#include <iostream>
#include <vector>

class Port;

enum class LinkType
{
    INCOMING,
    OUTGOING,
    BIDIRECTIONAL,
};

struct WaypointLinks
{
    double source_x{};
    double source_y{};
    double target_x{};
    double target_y{};
};

class Link
{
    std::string source_port_id_{};
    std::string target_port_id_{};
    double source_x{};
    double source_y{};
    double target_x{};
    double target_y{};
    std::string id{};
    bool has_waypoints{false};
    std::vector<WaypointLinks> vec_waypoint_links{};

    void set_source_port(const std::string& source_port_id, double source_x, double source_y);
    void set_target_port(const std::string& target_port_id, double target_x, double target_y);
    void add_waypoints(double source_x, double source_y, double target_x, double target_y);
    friend class Graph;

public:

    void set_id(const std::string& id) { this->id = id; };
    [[nodiscard]] std::string get_id() const { return this->id; };
    void add_link(const std::string& source_port_id, const std::string& target_port_id, double source_x, double source_y, double target_x,
                  double target_y);
};

#endif //LINK_H
