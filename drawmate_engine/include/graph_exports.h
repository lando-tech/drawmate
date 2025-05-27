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
    std::vector<PortExport> ports_left_{};
    std::vector<PortExport> ports_right_{};
};

#endif // GRAPH_EXPORTS_H