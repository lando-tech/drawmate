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

    void set_x(double x);

    [[nodiscard]] const double get_x();

    void set_y(double y);

    [[nodiscard]] const double get_y();

    void set_width(double width);

    [[nodiscard]] const double get_width();

    void set_height(double height);

    [[nodiscard]] const double get_height();

    std::tuple<double, double> get_x_y_tuple() const;

    std::tuple<double, double> get_width_height_tuple() const;

};

#endif
