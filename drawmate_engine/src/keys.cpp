#include <vector>
#include <sstream>
#include <string>
#include <random>
#include "node.h"
#include "graph_config.h"
#include "keys.h"

std::vector<char> get_alpha_upper()
{
  std::vector<char> alpha_upper{'A'};
  for (int i = 1; i < 26; ++i)
  {
    alpha_upper.push_back(alpha_upper[0] + i);
  }

  return alpha_upper;
}

std::vector<char> get_alpha_lower()
{
  std::vector<char> alpha_lower{'a'};
  for (int i = 1; i < 26; ++i)
  {
    alpha_lower.push_back(alpha_lower[0] + i);
  }
  return alpha_lower;
}

std::vector<char> get_alpha_upper_and_lower()
{
  std::vector<char> alpha{'A'};
  for (int i = 1; i < 26; ++i)
  {
    alpha.push_back(alpha[0] + i);
  }

  alpha.push_back('a');
  for (int i = 1; i < 26; ++i)
  {
    alpha.push_back('a' + i);
  }
  return alpha;
}

std::vector<char> get_alpha_numeric_vector()
{
  std::vector<char> alpha_numeric{'A'};

  for (int i = 1; i < 26; ++i)
  {
    alpha_numeric.push_back('A' + i);
  }

  alpha_numeric.push_back('a');
  for (int i = 1; i < 26; ++i)
  {
    alpha_numeric.push_back('a' + i);
  }

  alpha_numeric.push_back('0');
  for (int i = 1; i < 10; ++i)
  {
    alpha_numeric.push_back('0' + i);
  }
  return alpha_numeric;
}

std::string generate_export_key(int key_size)
{
  /*
   * A randomly generated key with a mix of alpha-numeric characters
   */
  std::vector<char> alpha{get_alpha_numeric_vector()};
  size_t vec_size {alpha.size()};

  std::random_device rand{};
  std::mt19937 gen(rand());
  std::uniform_int_distribution<> distrib(0, vec_size);

  std::string export_key{};

  for (int i = 0; i < key_size; ++i)
  {
    export_key.push_back(alpha.at(distrib(gen)));
  }
  return export_key;
}

std::string generate_node_key(NodeOrientation node_orientation, const int column_count, const int row_count)
{
  std::string key{};
  if (node_orientation == NodeOrientation::LEFT)
  {
    key.append("L-");
    key.append(std::to_string(column_count));
    key.append("-");
    key.append(std::to_string(row_count));
  }
  else if (node_orientation == NodeOrientation::RIGHT)
  {
    key.append("R-");
    key.append(std::to_string(column_count));
    key.append("-");
    key.append(std::to_string(row_count));
  }
  else
  {
    key.append("C-");
    key.append(std::to_string(column_count));
  }
  // std::cout << "Key: " << key << "\n";
  return key;
}

std::string generate_port_key(const std::string &parent_node_key, PortOrientation port_orientation, int port_index)
{
  std::string key_copy{parent_node_key};
  std::vector<std::string> key_toks{split_string(key_copy, '-')};
  std::string port_key{};
  port_key.append(key_toks[0]);
  port_key.append("-" + key_toks[1] + "-");
  if (port_orientation == PortOrientation::LEFT)
  {
    port_key.append("L-");
  }
  else if (port_orientation == PortOrientation::RIGHT)
  {
    port_key.append("R-");
  }
  port_key.append(std::to_string(port_index));
  return port_key;
}

std::vector<std::string> split_string(const std::string &str, char delim)
{
  /*
   * Basic utility function for splitting a string and returning a vector of string tokens.
   */
  std::vector<std::string> tokens{};
  std::stringstream ss(str);
  std::string token{};

  while (std::getline(ss, token, delim))
  {
    tokens.push_back(token);
  }
  return tokens;
}

std::string get_adjacent_port_key(const std::string &key, PortOrientation port_orientation, NodeOrientation node_orientation)
{
  std::vector<std::string> key_toks{split_string(key, '-')};
  int column{};
  int row{};
  int index{};
  std::string adjacent_key{};
  try
  {
    column = std::stoi(key_toks[1]);
    row = std::stoi(key_toks[3]);
    if (column == 0)
    {
      switch (node_orientation)
      {
      case NodeOrientation::LEFT:
        switch (port_orientation)
        {
        case PortOrientation::LEFT:
          adjacent_key.append("L-" + std::to_string(column + 1));
          adjacent_key.append("-R-" + std::to_string(row));
          break;
        case PortOrientation::RIGHT:
          adjacent_key.append("C-" + std::to_string(column));
          adjacent_key.append("-L-" + std::to_string(row));
          break;
        default:
          throw std::runtime_error("Port Orientation must be defined! get_adjacent_port_key line 52");
        }
        break;
      case NodeOrientation::RIGHT:
        switch (port_orientation)
        {
        case PortOrientation::LEFT:
          adjacent_key.append("C-" + std::to_string(column));
          adjacent_key.append("-R-" + std::to_string(row));
          break;
        case PortOrientation::RIGHT:
          adjacent_key.append("R-" + std::to_string(column + 1));
          adjacent_key.append("-L-" + std::to_string(row));
          break;
        default:
          throw std::runtime_error("Port Orientation must be defined! get_adjacent_port_key line 69");
        }
        break;
      case NodeOrientation::CENTER:
        switch (port_orientation)
        {
        case PortOrientation::LEFT:
          adjacent_key.append("L-");
          adjacent_key.append(std::to_string(column));
          adjacent_key.append("-R-");
          adjacent_key.append(std::to_string(row));
          break;
        case PortOrientation::RIGHT:
          adjacent_key.append("R-");
          adjacent_key.append(std::to_string(column));
          adjacent_key.append("-L-");
          adjacent_key.append(std::to_string(row));
          break;
        default:
          throw std::runtime_error("Port Orientation must be defined! get_adjacent_port_key line 93");
        }
        break;
      default:
        throw std::runtime_error("Node Orientation must be defined! get_adjacent_port_key line 97");
      }
    }
    else
    {
      switch (node_orientation)
      {
      case NodeOrientation::LEFT:
        adjacent_key.append("L-");
        switch (port_orientation)
        {
        case PortOrientation::LEFT:
          adjacent_key.append(std::to_string(column + 1));
          adjacent_key.append("-R-");
          adjacent_key.append(std::to_string(row));
          break;
        case PortOrientation::RIGHT:
          adjacent_key.append(std::to_string(column - 1));
          adjacent_key.append("-L-");
          adjacent_key.append(std::to_string(row));
          break;
        default:
          throw std::runtime_error("Port Orientation must be defined! get_adjacent_port_key line 120");
        }
        break;
      case NodeOrientation::RIGHT:
        adjacent_key.append("R-");
        switch (port_orientation)
        {
        case PortOrientation::LEFT:
          adjacent_key.append(std::to_string(column - 1));
          adjacent_key.append("-R-");
          adjacent_key.append(std::to_string(row));
          break;
        case PortOrientation::RIGHT:
          adjacent_key.append(std::to_string(column + 1));
          adjacent_key.append("-L-");
          adjacent_key.append(std::to_string(row));
          break;
        default:
          throw std::runtime_error("Port Orientation must be defined! get_adjacent_port_key Node orientation: Right line 137");
        }
        break;
      default:
        throw std::runtime_error("Node Orientation must be defined! get_adjacent_port_key line 140");
      }
    }
    return adjacent_key;
  }
  catch (const std::invalid_argument &e)
  {
    throw std::runtime_error("Invalid argument for key index: get_adjacent_port_key");
  }
  catch (const std::out_of_range &e)
  {
    throw std::runtime_error("Argument of out range");
  }

  throw std::runtime_error("Unexpected error occured during function: "
                           "get_adjacent_port_key(const std::string& key, PortOrientation port_orientation, NodeOrientation node_orientation)");
}

std::string get_adjacent_key(const std::string &key,
                             NodeOrientation node_orientation,
                             GridOrientation grid_orientation)
{
  /*
   * Takes in the current key, current node orientation, and the adjacency of the neighbor
   * as described in the Grid Orientation enum class. It will return the adjacent key, and
   * ensure the conversion of stoi is handled properly.
   */
  std::vector<std::string> key_toks{split_string(key, '-')};
  int column{};
  int row{};
  std::string adjacent_key{};
  try
  {
    column = std::stoi(key_toks[1]);
    row = std::stoi(key_toks[2]);
    if (node_orientation == NodeOrientation::LEFT)
    {
      adjacent_key.append("L-");
    }
    else if (node_orientation == NodeOrientation::RIGHT)
    {
      adjacent_key.append("R-");
    }
    else
    {
      adjacent_key.append("C-");
    }

    if (grid_orientation == GridOrientation::LEFT)
    {
      adjacent_key.append(std::to_string(column + 1));
      adjacent_key.append("-" + std::to_string(row));
    }
    else if (grid_orientation == GridOrientation::RIGHT)
    {
      adjacent_key.append(std::to_string(column - 1));
      adjacent_key.append("-" + std::to_string(row));
    }
    else if (grid_orientation == GridOrientation::ABOVE)
    {
      adjacent_key.append(std::to_string(column) + "-");
      adjacent_key.append(std::to_string(row - 1));
    }
    else if (grid_orientation == GridOrientation::BELOW)
    {
      adjacent_key.append(std::to_string(column) + "-");
      adjacent_key.append(std::to_string(row + 1));
    }
    return adjacent_key;
  }
  catch (const std::invalid_argument &e)
  {
    throw std::runtime_error("Invalid argument for key index");
  }
  catch (const std::out_of_range &e)
  {
    throw std::runtime_error("Argument of out range");
  }

  throw std::runtime_error("Unexpected error occured during function: "
                           "get_adjacent_key(const std::string& key)");
}

std::string get_adjacent_key_from_center(NodeOrientation node_orientation,
                                         int port_index)
{
  /*
   * Takes in the port index of the desired node, and the orientation of the desired node.
   * It will always return a node at column 0, because directly adjacent nodes, in
   * reference to the matrix, are always at column 0. Port indexes are set to match
   * the row of the parent node.
   */
  std::string adjacent_key{};
  if (node_orientation == NodeOrientation::LEFT)
  {
    adjacent_key.append("L-0-" + std::to_string(port_index));
  }
  else if (node_orientation == NodeOrientation::RIGHT)
  {
    adjacent_key.append("R-0-" + std::to_string(port_index));
  }

  return adjacent_key;
}