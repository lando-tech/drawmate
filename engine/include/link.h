//
// Created by landotech on 5/16/25.
//

#ifndef LINK_H
#define LINK_H
#include <iostream>
#include <vector>
#include "port.h"
#include "node.h"
#include "keys.h"

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
    PortKey source_port_id_{};
    PortKey target_port_id_{};
    double source_x{};
    double source_y{};
    double target_x{};
    double target_y{};
    std::string id{};
    std::string label{};
    bool has_waypoints{false};
    std::vector<WaypointLinks> vec_waypoint_links{};

    std::string link_label_err();

    void set_source_port(PortKey source_port_id, double source_x, double source_y);
    void set_target_port(PortKey target_port_id, double target_x, double target_y);

    void set_link_label_center(int column, int row);
    void set_link_label_left_justified(int column, int row);
    void set_link_label_right_justified(int column, int row);
    void set_link_label(int column, int row, NodeOrientation node_orientation, PortOrientation port_orientation);

    void add_waypoints(double source_x, double source_y, double target_x, double target_y);
    friend class Graph;

public:

    void set_id(const std::string& id) { this->id = id; };
    [[nodiscard]] std::string get_id() const { return this->id; };
    void add_link(PortKey source_port_id, PortKey target_port_id, double source_x, double source_y, double target_x,
                  double target_y);
};

#endif //LINK_H
