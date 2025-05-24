//
// Created by landotech on 5/16/25.
//

#include "../include/port.h"

Port::Port(
    const double x,
    const double y,
    const int width,
    const int height,
    const std::string& label,
    const std::string& parent_id,
    const PortType port_type,
    const PortOrientation port_orientation
    )
{
    this->set_x(x);
    this->set_y(y);
    this->set_width(width);
    this->set_height(height);
    this->label = label;
    this->set_parent_id(parent_id);
    this->port_type = port_type;
    this->port_orientation_ = port_orientation;
}
