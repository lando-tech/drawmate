#ifndef GRAPH_EXPORTS_H
#define GRAPH_EXPORTS_H

#include <iostream>
#include <vector>
#include "link.h"

struct LinkExport
{
    double source_x{};
    double source_y{};
    double target_x{};
    double target_y{};
    std::string _id{};
    std::string source_id{};
    std::string target_id{};
    bool has_waypoints{};
    std::vector<WaypointLinks> waypoints{};
};

struct PortExport
{
    std::string label{};
    std::string source_id{};
    std::string target_id{};
    double x{};
    double y{};
    double width{};
    double height{};
};

struct LabelExport
{
    std::string name{};
    std::string source_id{};
    std::string target_id{};
    double x{};
    double y{};
    double width{};
    double height{};
};

struct NodeExport
{
    std::string name{};
    std::string source_id{};
    std::string target_id{};
    double x{};
    double y{};
    double width{};
    double height{};
    LabelExport label{};
};

#endif // GRAPH_EXPORTS_H