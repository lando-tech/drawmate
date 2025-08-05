#ifndef DRAWMATE_GEOMETRY_H
#define DRAWMATE_GEOMETRY_H

#include <tuple>

class DrawmateGeometry {

private:
    double m_x{};
    double m_y{};

    double m_width{};
    double m_height{};

public:

    void set_x(double x) { this->m_x = x; }

    [[nodiscard]] const double get_x() const { return this->m_x; }

    void set_y(double y) { this->m_y = y; }

    [[nodiscard]] const double get_y() const { return this->m_y; }

    void set_width(double width) { this-> m_width = width; }

    [[nodiscard]] const double get_width() const { return this->m_width; }

    void set_height(double height) { this->m_height = height; }

    [[nodiscard]] const double get_height() const { return this->m_height; }

    std::tuple<double, double> get_x_y_tuple() const { return std::make_tuple(this->m_x, this->m_y); }

    std::tuple<double, double> get_width_height_tuple() const { return std::make_tuple(m_width, m_height); }

};

#endif
