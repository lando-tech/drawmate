#ifndef DRAWMATE_GEOMETRY_H
#define DRAWMATE_GEOMETRY_H

#include <tuple>

class DrawmateGeometry {

private:
    double m_x{};
    double m_y{};

public:

    void set_x(double x) { this->m_x = x; }

    [[nodiscard]] const double get_x() const { return this->m_x; }

    void set_y(double y) { this->m_y = y; }

    [[nodiscard]] const double get_y() const { return this->m_y; }

    std::tuple<double, double> get_x_y_tuple() const { return std::make_tuple(this->m_x, this->m_y); }


};

#endif
