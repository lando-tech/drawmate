#ifndef GRID_COUNTER_PAIR_H
#define GRID_COUNTER_PAIR_H

#include "grid_counter.h"

class GridCounterPair {

private:
    GridCounter m_row_counter{};
    GridCounter m_column_counter{};

public:
    // Constructors
    GridCounterPair() = default;
    GridCounterPair(int row_initial, int column_initial)
        : m_row_counter(row_initial), m_column_counter(column_initial) {}

    // Row counter access
    [[nodiscard]] GridCounter& get_row_counter() { return m_row_counter; }
    [[nodiscard]] const GridCounter& get_row_counter() const { return m_row_counter; }

    [[nodiscard]] int get_row_count() const { return m_row_counter.get_count(); }
    void set_row_count(int count) { m_row_counter.set_count(count); }
    void increment_row() { m_row_counter.increment(); }
    void reset_row() { m_row_counter.reset(); }

    // Column counter access
    [[nodiscard]] GridCounter& get_column_counter() { return m_column_counter; }
    [[nodiscard]] const GridCounter& get_column_counter() const { return m_column_counter; }

    [[nodiscard]] int get_column_count() const { return m_column_counter.get_count(); }
    void set_column_count(int count) { m_column_counter.set_count(count); }
    void increment_column() { m_column_counter.increment(); }
    void reset_column() { m_column_counter.reset(); }

    // Pair operations
    void reset_both() {
        m_row_counter.reset();
        m_column_counter.reset();
    }

    void increment_both() {
        m_row_counter.increment();
        m_column_counter.increment();
    }

    [[nodiscard]] int get_total_count() const {
        return m_row_counter.get_count() + m_column_counter.get_count();
    }

};

#endif // GRID_COUNTER_PAIR_H
