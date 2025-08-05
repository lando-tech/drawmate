#ifndef DRAWMATE_RECT_NODE_H
#define DRAWMATE_RECT_NODE_H
#include "abstract_drawmate_node.h"
#include <string>

class DrawmateNodeRect : public AbstractDrawmateNode {

private:
    long m_id{};

    std::string m_label{};
    double m_area{};


public:
    void set_id(const long id) override { this->m_id = id; }
    const long get_id() const override { return this->m_id; }

    void calculate_area() { this->set_area(this->get_width() * this->get_height()); };
    void set_area(double area) { this->m_area = area; }
    double get_area() const { return this->m_area; }

};


#endif
