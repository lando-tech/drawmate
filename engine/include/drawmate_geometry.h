#ifndef DRAWMATE_GEOMETRY_H
#define DRAWMATE_GEOMETRY_H

#include <tuple>

class DrawmateGeometry {

private:
    double m_x{};
    double m_y{};

public:

    void set_x(double x);

    [[nodiscard]] const double get_x();

    void set_y(double y);

    [[nodiscard]] const double get_y();

    std::tuple<double, double> get_x_y_tuple() const;

};

#endif
