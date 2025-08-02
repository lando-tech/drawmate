#ifndef ANCHOR_GRID_LAYOUT_H
#define ANCHOR_GRID_LAYOUT_H

#include "abstract_layout_manager.h"
#include "grid_counter_pair.h"

class AnchorGridLayout : public AbstractLayoutManager {

private:

    int m_central_node_count{};

    GridCounterPair m_left_counters{};   // left = row, right = column for left side
    GridCounterPair m_right_counters{};  // left = row, right = column for right side

    int m_base_y_left{};
    int m_base_y_right{};

    int m_base_x_left{};
    int m_base_x_right{};

    int m_base_node_height{};
    int m_max_node_height{};

public:

    // Override abstract base class methods
    [[nodiscard]] double get_base_x() const override;
    void set_base_x(double base_x) override;

    [[nodiscard]] double get_base_y() const override;
    void set_base_y(double base_y) override;

    [[nodiscard]] std::tuple<double, double> get_base_x_y_tuple() const override;
    void set_base_position(double base_x, double base_y) override;

    [[nodiscard]] double get_max_node_spacing() const override;
    void set_max_node_spacing(double max_spacing) override;

    [[nodiscard]] double get_min_node_spacing() const override;
    void set_min_node_spacing(double min_spacing) override;

    [[nodiscard]] std::tuple<double, double> get_spacing_range_tuple() const override;
    void set_spacing_range(double min_spacing, double max_spacing) override;

    // Central node count
    [[nodiscard]] int get_central_node_count() const { return m_central_node_count; }
    void set_central_node_count(int count) { m_central_node_count = count; }

    // Left side counter access (row/column pair for left side)
    [[nodiscard]] GridCounterPair& get_left_counters() { return m_left_counters; }
    [[nodiscard]] const GridCounterPair& get_left_counters() const { return m_left_counters; }

    // Right side counter access (row/column pair for right side)
    [[nodiscard]] GridCounterPair& get_right_counters() { return m_right_counters; }
    [[nodiscard]] const GridCounterPair& get_right_counters() const { return m_right_counters; }

    // Convenience accessors for specific counters
    // Left side counters
    [[nodiscard]] GridCounter& get_left_row_counter() { return m_left_counters.get_row_counter(); }
    [[nodiscard]] GridCounter& get_left_column_counter() { return m_left_counters.get_column_counter(); }

    // Right side counters
    [[nodiscard]] GridCounter& get_right_row_counter() { return m_right_counters.get_row_counter(); }
    [[nodiscard]] GridCounter& get_right_column_counter() { return m_right_counters.get_column_counter(); }    // Base position getters/setters (left/right specific)
    [[nodiscard]] int get_base_y_left() const { return m_base_y_left; }
    void set_base_y_left(int y) { m_base_y_left = y; }

    [[nodiscard]] int get_base_y_right() const { return m_base_y_right; }
    void set_base_y_right(int y) { m_base_y_right = y; }

    [[nodiscard]] int get_base_x_left() const { return m_base_x_left; }
    void set_base_x_left(int x) { m_base_x_left = x; }

    [[nodiscard]] int get_base_x_right() const { return m_base_x_right; }
    void set_base_x_right(int x) { m_base_x_right = x; }

    // Node height getters/setters
    [[nodiscard]] int get_base_node_height() const { return m_base_node_height; }
    void set_base_node_height(int height) { m_base_node_height = height; }

    [[nodiscard]] int get_max_node_height() const { return m_max_node_height; }
    void set_max_node_height(int height) { m_max_node_height = height; }

    // Convenience method for resetting all counters
    void reset_all_counters() {
        m_left_counters.reset_both();
        m_right_counters.reset_both();
    }

};

#endif
