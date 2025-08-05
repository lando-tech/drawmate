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
    [[nodiscard]] double get_base_x() const { return m_base_x; }
    void set_base_x(double base_x) { m_base_x = base_x; }

    [[nodiscard]] double get_base_y() const { return m_base_y; }
    void set_base_y(double base_y) { m_base_y = base_y; }

    [[nodiscard]] std::tuple<double, double> get_base_x_y_tuple() const {
        return std::make_tuple(m_base_x, m_base_y);
    }
    void set_base_position(double base_x, double base_y) {
        m_base_x = base_x;
        m_base_y = base_y;
    }

    // Node spacing getters/setters
    [[nodiscard]] double get_max_node_spacing() const { return m_max_node_spacing; }
    void set_max_node_spacing(double max_spacing) { m_max_node_spacing = max_spacing; }

    [[nodiscard]] double get_min_node_spacing() const { return m_min_node_spacing; }
    void set_min_node_spacing(double min_spacing) { m_min_node_spacing = min_spacing; }

    [[nodiscard]] std::tuple<double, double> get_spacing_range_tuple() const {
        return std::make_tuple(m_min_node_spacing, m_max_node_spacing);
    }
    void set_spacing_range(double min_spacing, double max_spacing) {
        m_min_node_spacing = min_spacing;
        m_max_node_spacing = max_spacing;
    }

    // Virtual destructor
    virtual ~AbstractLayoutManager() = default;

};

#endif
