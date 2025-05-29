//
// Created by landotech on 5/16/25.
//

#ifndef GRAPH_OBJECT_H
#define GRAPH_OBJECT_H
#include <iostream>
#include <tuple>

/** GraphObject class
 * The GraphObject class is used as a base class for all objects
 * on the Graph. This was implemented to reduce boilerplate functions
 * for common behavior/usages of Nodes on the Graph. The member functions are almost 
 * exclusively getters and setters pertaining to attributes like x, y, width, and height.
 */
class GraphObject
{
protected:
    double x{};                           /**< double x */
    double y{};                           /**< double y */
    double width{};                    /** double width */
    double height{};                 /**< double height */
    std::string id{};               /**< std::string id */

    std::string source_id{}; /**< std::string source_id */
    std::string target_id{}; /**< std::string target_id */

    void set_id(const std::string& id) { this->id = id; }
    void set_source_id(const std::string& source_id) { this->source_id = source_id; }
    void set_target_id(const std::string& target_id) { this->target_id = target_id; }
    friend class Graph;

public:
    void set_x(const double x) { this->x = x; }

    void set_y(const double y) { this->y = y; }

    void set_width(const double width) { this->width = width; }

    void set_height(const double height) { this->height = height; }

    [[nodiscard]] double get_x() const { return this->x; }

    [[nodiscard]] double get_y() const { return this->y; }

    [[nodiscard]] double get_width() const { return this->width; }

    [[nodiscard]] double get_height() const { return this->height; }

    [[nodiscard]] std::string get_id() const { return this->id; }

    [[nodiscard]] std::string get_source_id() const { return this->source_id; }

    [[nodiscard]] std::string get_target_id() const { return this->target_id; }

    [[nodiscard]] std::tuple<double, double> get_x_y_tuple() const
    { return std::make_tuple(this->x, this->y); }

    [[nodiscard]] std::tuple<double, double> get_width_height_tuple() const
    { return std::make_tuple(this->width, this->height); }
};

#endif //GRAPH_OBJECT_H
