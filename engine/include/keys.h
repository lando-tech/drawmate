#ifndef KEYS_H
#define KEYS_H

#include <vector>
#include <string>

enum class PortOrientation;
enum class NodeOrientation;
enum class GridOrientation;

template <typename T>
inline void hash_combine(std::size_t& seed, const T& val)
{
    seed ^= std::hash<T>{}(val) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

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
    int column{};
    int row{};

    bool operator==(const PortKey &other) const
    {
        return node_orientation == other.node_orientation && 
               port_orientation == other.port_orientation && 
               column == other.column && 
               row == other.row;
    }
};



namespace std
{
    template<>
    struct hash<PortKey>
    {
        std::size_t operator()(const PortKey &k) const
        {
            std::size_t h{0};
            hash_combine(h, k.node_orientation);
            hash_combine(h, k.port_orientation);
            hash_combine(h, k.column);
            hash_combine(h, k.row);
            return h;
        }
    };
}

std::string generate_export_key(int key_size);
std::string generate_node_key_string(char node_orientation, const int column_count, const int row_count);
std::string generate_port_key_string(const std::string &parent_node_key, PortOrientation port_orientation, int port_index);
std::vector<std::string> split_string(const std::string &str, const char dilim);

PortKey get_adjacent_port_key(PortKey port_key);

std::string convert_node_key_internal(NodeKey node_key_internal);
std::string convert_port_key_internal(PortKey port_key_internal);
NodeKey convert_node_key_external(const std::string& node_key_external);
PortKey convert_port_key_external(const std::string& port_key_external);

#endif // KEYS_H