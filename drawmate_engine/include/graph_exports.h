/******************************************************************************
 * The following module is used to expose various Graph snapshots to the Python
 * interface. The structs were intentionally kept lightweight and are passed
 * to Python as readonly to ensure Graph integrity.
 ******************************************************************************/


#ifndef GRAPH_EXPORTS_H
#define GRAPH_EXPORTS_H

#include <iostream>
#include <vector>
#include "link.h"

/** LinkExport struct
 */
struct LinkExport
{
    double source_x{}; /**< double source_x */
    double source_y{}; /**< double source_y */
    double target_x{}; /**< double target_x */
    double target_y{}; /**< double target_y */
    std::string _id{}; /**< std::string _id */
    std::string source_id{}; /**< std::string source_id */
    std::string target_id{}; /**< std::string target_id */
    bool has_waypoints{}; /**< bool has_waypoints */
    std::vector<WaypointLinks> waypoints{}; /**< std::vector<WaypointLinks> */
};

/** PortExport struct
 */
struct PortExport
{
    std::string label{}; /**< std::string label */
    std::string source_id{}; /**< std::string source_id */
    std::string target_id{}; /**< std::string target_id */
    double x{}; /**< double x */
    double y{}; /**< double y */
    double width{}; /**< double width */
    double height{}; /**< double height */
};

/** LabelExport struct 
 * 
 */
struct LabelExport
{
    std::string name{}; /**< std::string name */
    std::string source_id{}; /**< std::string source_id */
    std::string target_id{}; /**< std::string target_id */
    double x{}; /**< double x */
    double y{}; /**< double y */
    double width{}; /**< double width */
    double height{}; /**< double height */
};

/** NodeExport struct
 * 
 */
struct NodeExport
{
    LabelExport label{}; /**< std::string label */
    std::string name{}; /**< std::string name */
    std::string source_id{}; /**< std::string source_id */
    std::string target_id{}; /**< std::string target_id */
    double x{}; /**< double x */
    double y{}; /**< double y */
    double width{}; /**< double width */
    double height{}; /**< double height */
};

#endif // GRAPH_EXPORTS_H