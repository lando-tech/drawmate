//
// Created by landotech on 5/16/25.
//

#ifndef GRAPH_OBJECT_H
#define GRAPH_OBJECT_H
#include <iostream>
#include <tuple>

class GraphObject
{
protected:
    double x{};
    double y{};
    double width{};
    double height{};
    std::string id{};

    void set_id(const std::string& id) { this->id = id; }
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

    [[nodiscard]] std::tuple<double, double> get_x_y_tuple() const
    { return std::make_tuple(this->x, this->y); }

    [[nodiscard]] std::tuple<double, double> get_width_height_tuple() const
    { return std::make_tuple(this->width, this->height); }
};

#endif //GRAPH_OBJECT_H
