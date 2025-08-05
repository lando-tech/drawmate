#ifndef DRAWMATE_SHAPE_H
#define DRAWMATE_SHAPE_H

class DrawmateShape {


public:
    virtual void set_width(double width) const = 0;
    virtual double get_width() const = 0;

    virtual void set_height(double height) const = 0;
    virtual double get_height() const = 0;

    virtual const double get_area() const = 0;

    ~DrawmateShape() = default;

};

#endif
