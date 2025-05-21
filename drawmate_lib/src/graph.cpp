//
// Created by landotech on 5/16/25.
//

#include <cstdio>
#include "graph.h"

NodeType verify_node_type(const std::string& node_type_str)
{
    if (node_type_str == "video-matrix")
    {
        return NodeType::VIDEO_MATRIX;
    }
    if (node_type_str == "video-codec")
    {
        return NodeType::VIDEO_CODEC;
    }
    if (node_type_str == "audio-matrix")
    {
        return NodeType::AUDIO_MATRIX;
    }
    if (node_type_str == "audio-codec")
    {
        return NodeType::AUDIO_CODEC;
    }
    if (node_type_str == "pc")
    {
        return NodeType::PC;
    }
    if (node_type_str == "laptop")
    {
        return NodeType::LAPTOP;
    }
    if (node_type_str == "appliance")
    {
        return NodeType::APPLIANCE;
    }
    throw std::runtime_error("Invalid Node Type: " + node_type_str);
}

void Graph::verify_node_meta_key(const std::unordered_map<std::string, std::string> &node_meta_data) const
{
    for (const auto& it: this->node_meta_valid_keys_)
    {
        if (!node_meta_data.contains(it))
        {
            throw std::runtime_error("Error parsing Node metadata Dictionary! Key is invalid!");
        }
    }
}

double Graph::verify_node_height(const double port_count) const
{
    const double total_height{
        (port_count * this->layout_config_.port_height) + this->layout_config_.node_label_height + (
            (port_count - 1) * this->layout_config_.port_spacing)
    };

    if ( total_height > this->layout_config_.node_height )
    {
        return total_height;
    }
    return this->layout_config_.node_height;
}

double get_max_ports(const double port_count_left, const double port_count_right)
{
    if (port_count_left > port_count_right)
    {
        return port_count_left;
    }
    return port_count_right;
}

double Graph::calculate_x_left() const
{
    return (this->base_x_left - (this->layout_config_.node_width * this->column_count_left)) - this->layout_config_.
           node_spacing_x_axis;
}

double Graph::calculate_x_right(const double central_width) const
{
    const double base {this->layout_config_.base_x + central_width};
    const double offset {this->layout_config_.node_spacing_x_axis - this->layout_config_.node_width};
    return base + offset + (this->column_count_right * this->layout_config_.node_spacing_x_axis);
}

void Graph::increment_y_left(const double node_height)
{
    this->base_y_left = this->base_y_left + node_height + this->layout_config_.node_spacing_y_axis;
}

void Graph::increment_y_right(const double node_height)
{
    this->base_y_right = this->base_y_right + node_height + this->layout_config_.node_spacing_y_axis;
}

std::string Graph::generate_node_key(const char orientation)
{

    std::string key {};
    if (orientation == 'R')
    {
        key.append("R-");
        if (this->row_count_right == this->grid_config_.rows_right - 1)
        {
            this->row_count_right = 0;
            this->column_count_right++;
        }
        key.append(std::to_string(this->column_count_right));
        key.append("-");
        key.append(std::to_string(this->row_count_right++));
    }
    else
    {
        key.append("L-");
        if (this->row_count_left == this->grid_config_.rows_left - 1)
        {
            this->row_count_left = 0;
            this->column_count_left++;
        }
        key.append(std::to_string(this->column_count_left));
        key.append("-");
        key.append(std::to_string(this->row_count_left++));
    }
    return key;
}

void Graph::add_node_ports(const std::string &node_key, const std::vector<std::string> &port_labels_left,
                           const std::vector<std::string> &port_labels_right)
{
    const auto& node {this->nodes.at(node_key)};
    double x_left {node->get_x()};
    double y_left{
        node->get_y() + this->layout_config_.node_label_height + this->layout_config_.port_spacing
    };
    double y_right{
        node->get_y() + this->layout_config_.node_label_height + this->layout_config_.port_spacing
    };

    int port_key_left{0};
    for (const auto& it : port_labels_left)
    {
        node->add_port_left(
            std::make_unique<Port>(x_left, y_left, this->layout_config_.port_width, this->layout_config_.port_height, it,
                                   PortType::INPUT, PortOrientation::LEFT), port_key_left);
        node->get_port_ref_left(port_key_left).set_parent_id(node_key);
        y_left += this->layout_config_.port_height + this->layout_config_.port_spacing;
        port_key_left++;
    }

    int port_key_right{0};
    for (const auto& it: port_labels_right)
    {
        double x_right{ x_left + (this->layout_config_.node_width / 2)};
        node->add_port_right(
            std::make_unique<Port>(x_right, y_right, this->layout_config_.port_width, this->layout_config_.port_height, it,
                                   PortType::OUTPUT, PortOrientation::RIGHT), port_key_right);
        node->get_port_ref_right(port_key_right).set_parent_id(node_key);
        y_right += this->layout_config_.port_height + this->layout_config_.port_spacing;
        port_key_right++;
    }
}

void Graph::add_node(const std::unordered_map<std::string, std::string>& node_meta_data,
              const std::vector<std::string>& port_labels_left, const std::vector<std::string>& port_labels_right)
{
    const double max_ports{
        get_max_ports(static_cast<double>(port_labels_left.size()),
                     static_cast<double>(port_labels_right.size()))
    };
    double node_height {verify_node_height(max_ports)};
    double node_width {this->layout_config_.node_width};
    double x{};
    double y{};

    verify_node_meta_key(node_meta_data);

    NodeType node_type {verify_node_type(node_meta_data.at("node-type"))};
    std::string key{};
    if (node_meta_data.at("node-orientation") == "left")
    {
        x = calculate_x_left();
        y = this->base_y_left;
        key = generate_node_key('L');
        this->node_keys_left_.push_back(key);
        this->nodes[key] = std::make_unique<Node>(x, y, node_width, node_height, node_type);
        increment_y_left(node_height);
    }
    else if (node_meta_data.at("node-orientation") == "right")
    {
        x = calculate_x_right(200);
        y = this->base_y_right;
        key = generate_node_key('R');
        this->node_keys_right_.push_back(key);
        this->nodes[key] = std::make_unique<Node>(x, y, node_width, node_height, node_type);
        increment_y_right(node_height);
    }
    else
    {
        throw std::runtime_error("Please specify node-orientation as 'right' or 'left'");
    }
    add_node_ports(key, port_labels_left, port_labels_right);
    this->nodes.at(key)->set_node_label(std::make_unique<LabelNode>(x, y, this->layout_config_.node_width,
                                                  this->layout_config_.node_label_height,
                                                  node_meta_data.at("node-label")));
    this->node_keys_master_.push_back(key);
}

void Graph::add_connection(const std::string &source_node_id, const std::string &target_node_id, const int port_index_source, const int port_index_target)
{
    const auto& source_node {this->nodes.at(source_node_id)};
    const auto& target_node {this->nodes.at(target_node_id)};

    if (this->links[source_node_id].contains(port_index_source))
    {
        throw std::runtime_error("Node is already connected at that port!" + source_node_id);
    }

    this->links[source_node_id][port_index_source] = std::make_unique<Link>();
    const auto& link {this->links[source_node_id][port_index_source]};
    link->add_link(port_index_source, port_index_target,
        source_node->get_x(), source_node->get_y(), target_node->get_x(), target_node->get_y());
}

void Graph::get_nodes() const
{
    for (const auto& id : this->node_keys_master_)
    {
        const auto& node {this->nodes.at(id)};
        std::cout << "Node     ID: " << id << "\n";
        printf("Node      x: %.2f\n", node->get_x());
        printf("Node      y: %.2f\n", node->get_y());
        printf("Node  width: %.2f\n", node->get_width());
        printf("Node height: %.2f\n", node->get_height());
        printf("======================\n");
    }
}

void Graph::pretty_print_node_data(const std::string& node_id, const double node_height) const
{
    const int port_count_left {static_cast<int>(this->nodes.at(node_id)->get_port_count_left())};
    const int port_count_right {static_cast<int>(this->nodes.at(node_id)->get_port_count_right())};

    std::cout << "\n=====================\n";

    std::cout << "Node ID: " << node_id << "\n";
    std::cout << "\tlabel: " << this->nodes.at(node_id)->get_label() << "\n";
    std::cout << "\twidth: " << this->layout_config_.node_width << "\n";
    std::cout << "\theight: " << node_height << "\n";
    std::cout << "\tx = " << this->nodes.at(node_id)->get_x() << " y = " << this->nodes.at(node_id)->get_y() << "\n";
    std::cout << "\tPort count left : " << port_count_left << "\n";
    std::cout << "\tPort count right: " << port_count_right << "\n";

    std::cout << "\nLeft Side Ports:\n";
    for (int i = 0; i < port_count_left; ++i)
    {
        std::cout << "\tLabel: " << this->nodes.at(node_id)->get_port_ref_left(i).get_port_label() << "\n";
        std::cout << "\tindex " << i << "\n\tx = " << this->nodes.at(node_id)->get_port_ref_left(i).get_x();
        std::cout << " y = " << this->nodes.at(node_id)->get_port_ref_left(i).get_y() << "\n";
    }

    std::cout << "\nRight Side Ports:\n";
    for (int i = 0; i < port_count_right; ++i)
    {
        std::cout << "\tLabel: " << this->nodes.at(node_id)->get_port_ref_right(i).get_port_label() << "\n";
        std::cout << "\tindex " << i << "\n\tx = " << this->nodes.at(node_id)->get_port_ref_right(i).get_x();
        std::cout << " y = " << this->nodes.at(node_id)->get_port_ref_right(i).get_y() << "\n";
    }
    std::cout << "=====================\n";
}

Graph::Graph(const LayoutConfig &layout_config, const GridConfig grid_config)
{
    this->layout_config_ = layout_config;
    this->grid_config_ = grid_config;

    this->base_y_left = this->layout_config_.base_y;
    this->base_x_left = this->layout_config_.base_x;
    this->base_y_right = this->layout_config_.base_y;
    this->base_x_right = this->layout_config_.base_x;
}
