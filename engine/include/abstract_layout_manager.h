#ifndef ABSTRACT_LAYOUT_MANAGER_H
#define ABSTRACT_LAYOUT_MANAGER_H

#include <tuple>

class AbstractLayoutManager {

private:

    double m_base_x{};
    double m_base_y{};

    double m_max_node_spacing{};
    double m_min_node_spacing{};

public:

    // Base position getters/setters
    [[nodiscard]] virtual double get_base_x() const = 0;
    virtual void set_base_x(double base_x) = 0;

    [[nodiscard]] virtual double get_base_y() const = 0;
    virtual void set_base_y(double base_y) = 0;

    [[nodiscard]] virtual std::tuple<double, double> get_base_x_y_tuple() const = 0;
    virtual void set_base_position(double base_x, double base_y) = 0;

    // Node spacing getters/setters
    [[nodiscard]] virtual double get_max_node_spacing() const = 0;
    virtual void set_max_node_spacing(double max_spacing) = 0;

    [[nodiscard]] virtual double get_min_node_spacing() const = 0;
    virtual void set_min_node_spacing(double min_spacing) = 0;

    [[nodiscard]] virtual std::tuple<double, double> get_spacing_range_tuple() const = 0;
    virtual void set_spacing_range(double min_spacing, double max_spacing) = 0;

    // Virtual destructor
    virtual ~AbstractLayoutManager() = default;

};

#endif
