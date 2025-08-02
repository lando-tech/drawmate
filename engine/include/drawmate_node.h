#ifndef DRAWMATE_NODE_H
#define DRAWMATE_NODE_H

#include "drawmate_geometry.h"
#include <tuple>

class AbstractDrawmateNode {

protected:
    long m_id{};

    double m_width{};

    double m_height{};

    DrawmateGeometry m_geometry{};

public:
    virtual long get_id() const = 0;

    virtual void set_id(const double id) = 0;

    virtual double get_width() const = 0;

    virtual void set_width(const double width) = 0;

    virtual double get_height() const = 0;

    virtual double set_height(const double height) = 0;

    virtual std::tuple<double, double> get_width_height_tuple() const = 0;

    virtual void set_geometry(DrawmateGeometry geometry) = 0;

    virtual DrawmateGeometry& get_geometry() const = 0;

    virtual double get_x() const = 0;

    virtual void set_x(double x) = 0;

    virtual double get_y() const = 0;

    virtual ~AbstractDrawmateNode() = default;

};

#endif
