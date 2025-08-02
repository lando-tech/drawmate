#ifndef DRAWMATE_GEOMETRY_H
#define DRAWMATE_GEOMETRY_H

class DrawmateGeometry {

private:
    double m_x{};
    double m_y{};

public:

    void set_x(double x);

    const double get_x();

    void set_y(double y);

    const double get_y();

};

#endif
