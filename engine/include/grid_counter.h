#ifndef GRID_COUNTER_H
#define GRID_COUNTER_H

class GridCounter {

private:
    int m_count{};

public:
    // Constructors
    GridCounter() = default;
    explicit GridCounter(int initial_count) : m_count(initial_count) {}

    // Basic operations
    [[nodiscard]] int get_count() const { return m_count; }
    void set_count(int count) { m_count = count; }

    void increment() { ++m_count; }
    void decrement() { --m_count; }
    void reset() { m_count = 0; }

    // Arithmetic operations
    void add(int value) { m_count += value; }
    void subtract(int value) { m_count -= value; }

    // Comparison operations
    [[nodiscard]] bool is_zero() const { return m_count == 0; }
    [[nodiscard]] bool is_positive() const { return m_count > 0; }
    [[nodiscard]] bool is_negative() const { return m_count < 0; }

};

#endif // GRID_COUNTER_H
