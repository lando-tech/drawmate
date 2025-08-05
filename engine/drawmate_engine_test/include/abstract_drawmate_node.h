#ifndef ABSTRACT_DRAWMATE_NODE_H
#define ABSTRACT_DRAWMATE_NODE_H

#include "drawmate_geometry.h"
#include "drawmate_node_spec.h"
#include <tuple>

class AbstractDrawmateNode {

private:
    long m_id{};

    DrawmateGeometry m_geometry{};
    NodeOrientation m_orientation{};
    bool m_is_grid_based{false};

public:
    [[nodiscard]] virtual const long get_id() const = 0;

    virtual void set_id(const long id) = 0;

    [[nodiscard]] double get_width() const { return this->m_geometry.get_width(); }

    void set_width(const double width) { this->m_geometry.set_width(width); };

    [[nodiscard]] double get_height() const { return this->m_geometry.get_height(); }

    void set_height(const double height) { this->m_geometry.set_height(height); }

    [[nodiscard]] std::tuple<double, double> get_width_height_tuple() const {
        return this->m_geometry.get_width_height_tuple();
    }

    void set_geometry(DrawmateGeometry geometry) { this->m_geometry = geometry; }

    [[nodiscard]] DrawmateGeometry& get_geometry() { return this->m_geometry; }

    [[nodiscard]] const DrawmateGeometry& get_geometry() const { return this->m_geometry; }

    [[nodiscard]] double get_x() const { return this->m_geometry.get_x(); }

    void set_x(double x) { this->m_geometry.set_x(x); }

    [[nodiscard]] double get_y() const { return this->m_geometry.get_y(); }

    void set_y(double y) { this->m_geometry.set_y(y); }

    [[nodiscard]] std::tuple<double, double> get_x_y_tuple() const {
        return this->m_geometry.get_x_y_tuple();
    }

    void set_node_orientation(NodeOrientation orientation) {
        this->m_orientation = orientation;
        this->m_is_grid_based = true;
    }

    NodeOrientation get_node_orientation() { return this->m_orientation; }

    virtual ~AbstractDrawmateNode() = default;

};

#endif
