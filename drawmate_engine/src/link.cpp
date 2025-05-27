//
// Created by landotech on 5/16/25.
//

#include "link.h"

double get_midpoint_x(const double x1, const double x2)
{
    if ( x1 < x2 )
    {
        return (x2 + x1) / 2.0;
    }
    return (x1 + x2) / 2.0;
}

void Link::set_source_port(PortKey source_port_id, const double source_x, const double source_y)
{
    this->source_x = source_x;
    this->source_y = source_y;
    this->source_port_id_ = source_port_id;
}

void Link::set_target_port(PortKey target_port_id, const double target_x, const double target_y)
{

    this->target_x = target_x;
    this->target_y = target_y;
    this->target_port_id_ = target_port_id;
}

void Link::add_waypoints(const double source_x, const double source_y, const double target_x, const double target_y)
{

    WaypointLinks waypoint1{};
    WaypointLinks waypoint2{};
    WaypointLinks waypoint3{};

    const double midpoint_x = get_midpoint_x(source_x, target_x);

    waypoint1.source_x = source_x;
    waypoint1.source_y = source_y;
    waypoint1.target_x = midpoint_x;
    waypoint1.target_y = source_y;
    this->vec_waypoint_links.push_back(waypoint1);

    waypoint2.source_x = midpoint_x;
    waypoint2.source_y = source_y;
    waypoint2.target_x = midpoint_x;
    waypoint2.target_y = target_y;
    this->vec_waypoint_links.push_back(waypoint2);

    waypoint3.source_x = midpoint_x;
    waypoint3.source_y = target_y;
    waypoint3.target_x = target_x;
    waypoint3.target_y = target_y;
    this->vec_waypoint_links.push_back(waypoint3);

}

void Link::add_link(PortKey source_port_id, PortKey target_port_id, const double source_x, const double source_y,
                    const double target_x, const double target_y)
{
    set_source_port(source_port_id, source_x, source_y);
    set_target_port(target_port_id, target_x, target_y);

    if ( source_y != target_y )
    {
        add_waypoints(source_x, source_y, target_x, target_y);
        this->has_waypoints = true;
    }
}
