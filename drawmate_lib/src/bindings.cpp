#include <pybind11/pybind11.h>

namespace py = pybind11;
struct LayoutConfig
{
    int x{};
    int y{};
};

PYBIND11_MODULE(example, m)
{
    py::class_<LayoutConfig>(m, "LayoutConfig")
        .def(py::init<const int, int>());
}