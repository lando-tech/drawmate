#ifndef KEYS_H
#define KEYS_H

#include <vector>
#include <string>

enum class PortOrientation;
enum class NodeOrientation;
enum class GridOrientation;

struct NodeKey
{
    char orientation{};
    int column{};
    int row{};

    bool operator==(const NodeKey &other) const
    {
        return orientation == other.orientation && column == other.column && row == other.row;
    }
};

namespace std
{
    template <>
    struct hash<NodeKey>
    {
        size_t operator()(const NodeKey &k) const
        {
            return (hash<char>()(k.orientation) << 1) ^
                   (hash<int>()(k.column) << 2) ^
                   (hash<int>()(k.row) << 3);
        }
    };
}

struct PortKey
{
    char node_orientation{};
    char port_orientation{};
    int node_row{};
    int column{};
    int row{};

    bool operator==(const PortKey &other) const
    {
        return node_orientation == other.node_orientation && port_orientation == other.port_orientation && node_row == other.node_row && column == other.column && row == other.row;
    }
};

namespace std
{
    template <>
    struct hash<PortKey>
    {
        size_t operator()(const PortKey &k) const
        {
            return (hash<char>()(k.node_orientation) << 1) ^
                   (hash<char>()(k.port_orientation) << 2) ^
                   (hash<int>()(k.node_row) << 3) ^
                   (hash<int>()(k.column) << 4) ^
                   (hash<int>()(k.row) << 5);
        }
    };
}

std::string generate_export_key(int key_size);
NodeKey convert_node_key_internal(const std::string& node_key_str);
std::string generate_node_key_string(char node_orientation, const int column_count, const int row_count);
std::string generate_port_key_string(const std::string &parent_node_key, PortOrientation port_orientation, int port_index);
std::vector<std::string> split_string(const std::string &str, const char dilim);
std::string get_adjacent_port_key_string(const std::string &key,
                                  PortOrientation port_orientation,
                                  NodeOrientation node_orientation);
PortKey get_adjacent_port_key(PortKey port_key);
std::string get_adjacent_key_string(const std::string &key,
                             NodeOrientation node_orientation,
                             GridOrientation grid_orientation);
std::string get_adjacent_key_string_from_center(NodeOrientation node_orientation,
                                         int port_index);

#endif // KEYS_H