#ifndef DRAWMATE_WAYPOINT_H
#define DRAWMATE_WAYPOINT_H

#include <tuple>

class DrawmateWaypoint {

private:
    double m_x{};
    double m_y{};
    long m_id{};

public:
    // Constructors
    DrawmateWaypoint() = default;
    DrawmateWaypoint(long id, double x, double y)
        : m_id(id), m_x(x), m_y(y) {}

    // ID getters/setters
    [[nodiscard]] long get_id() const { return m_id; }
    void set_id(long id) { m_id = id; }

    // Position getters/setters
    [[nodiscard]] double get_x() const { return m_x; }
    void set_x(double x) { m_x = x; }

    [[nodiscard]] double get_y() const { return m_y; }
    void set_y(double y) { m_y = y; }

    [[nodiscard]] std::tuple<double, double> get_x_y_tuple() const {
        return std::make_tuple(m_x, m_y);
    }

    void set_position(double x, double y) {
        m_x = x;
        m_y = y;
    }

};

#endif // DRAWMATE_WAYPOINT_H
