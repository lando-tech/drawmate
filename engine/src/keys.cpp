#include <vector>
#include <sstream>
#include <string>
#include <random>
#include "node.h"
#include "graph_config.h"
#include "keys.h"
#include <cassert>

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
  size_t vec_size{alpha.size()};

  std::random_device rand{};
  std::mt19937 gen(rand());
  std::uniform_int_distribution<> distrib(0, vec_size - 1);

  std::string export_key{};

  for (int i = 0; i < key_size; ++i)
  {
    export_key.push_back(alpha.at(distrib(gen)));
  }
  return export_key;
}

std::string generate_node_key_string(char node_orientation, const int column_count, const int row_count)
{
  std::string key{};
  if (node_orientation == 'L')
  {
    // "L-0-0"
    key.append("L-");
    key.append(std::to_string(column_count));
    key.append("-");
    key.append(std::to_string(row_count));
  }
  else if (node_orientation == 'R')
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

std::string generate_port_key_string(const std::string &parent_node_key, PortOrientation port_orientation, int port_index)
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

PortKey get_adjacent_port_key(const PortKey port_key)
{
  PortKey adjacent_port_key{};

  if (port_key.column == 0)
  {
    if (port_key.node_orientation == 'C')
    {
      if (port_key.port_orientation == 'L')
      {
        adjacent_port_key.node_orientation = 'L';
        adjacent_port_key.port_orientation = 'R';
        adjacent_port_key.column = port_key.column;
        adjacent_port_key.row = port_key.row;
      }
      else
      {
        adjacent_port_key.node_orientation = 'R';
        adjacent_port_key.port_orientation = 'L';
        adjacent_port_key.column = port_key.column;
        adjacent_port_key.row = port_key.row;
      }
    }
    else if (port_key.node_orientation == 'L')
    {
      if (port_key.port_orientation == 'L')
      {
        adjacent_port_key.node_orientation = 'L';
        adjacent_port_key.port_orientation = 'R';
        adjacent_port_key.column = port_key.column + 1;
        adjacent_port_key.row = port_key.row;
      }
      else
      {
        adjacent_port_key.node_orientation = 'C';
        adjacent_port_key.port_orientation = 'L';
        adjacent_port_key.column = port_key.column;
        adjacent_port_key.row = port_key.row;
      }
    }
    else if (port_key.node_orientation == 'R')
    {
      if (port_key.port_orientation == 'L')
      {
        adjacent_port_key.node_orientation = 'C';
        adjacent_port_key.port_orientation = 'R';
        adjacent_port_key.column = port_key.column;
        adjacent_port_key.row = port_key.row;
      }
      else
      {
        adjacent_port_key.node_orientation = 'R';
        adjacent_port_key.port_orientation = 'L';
        adjacent_port_key.column = port_key.column + 1;
        adjacent_port_key.row = port_key.row;
      }
    }
    return adjacent_port_key;
  }
  else
  {
    if (port_key.node_orientation == 'L')
    {
      adjacent_port_key.node_orientation = 'L';
      if (port_key.port_orientation == 'L')
      {
        adjacent_port_key.port_orientation = 'R';
        adjacent_port_key.column = port_key.column + 1;
        adjacent_port_key.row = port_key.row;
      }
      else
      {
        adjacent_port_key.port_orientation = 'L';
        adjacent_port_key.column = port_key.column - 1;
        adjacent_port_key.row = port_key.row;
      }
    }
    else
    {
      adjacent_port_key.node_orientation = 'R';
      if (port_key.port_orientation == 'L')
      {
        adjacent_port_key.port_orientation = 'R';
        adjacent_port_key.column = port_key.column - 1;
        adjacent_port_key.row = port_key.row;
      }
      else
      {
        adjacent_port_key.port_orientation = 'L';
        adjacent_port_key.column = port_key.column + 1;
        adjacent_port_key.row = port_key.row;
      }
    }
    return adjacent_port_key;
  }
}

std::string convert_node_key_internal(NodeKey node_key_internal)
{
  std::string external{};
  external.push_back(node_key_internal.orientation);
  external.append("-" + std::to_string(node_key_internal.column));
  external.append("-" + std::to_string(node_key_internal.row));
  return external;
}

std::string convert_port_key_internal(PortKey port_key_internal)
{
  std::string external{};
  external.push_back(port_key_internal.node_orientation);
  external.append(std::to_string(port_key_internal.column) + "-");
  external.push_back(port_key_internal.port_orientation);
  external.append("-" + std::to_string(port_key_internal.row));
  return external;
}

NodeKey convert_node_key_external(const std::string &node_key_external)
{
  NodeKey node_key_internal{};
  std::vector<std::string> key_toks{split_string(node_key_external, '-')};
  assert(key_toks[0][0] == 1);
  node_key_internal.orientation = key_toks[0][0];
  node_key_internal.column = std::stoi(key_toks[1]);
  node_key_internal.row = std::stoi(key_toks[2]);
  return node_key_internal;
}

PortKey convert_port_key_external(const std::string &port_key_external)
{
  PortKey port_key_internal{};
  std::vector<std::string> key_toks{split_string(port_key_external, '-')};
  assert(key_toks[0][0] == 1); 
  port_key_internal.node_orientation = key_toks[0][0];
  assert(key_toks[0][2] == 1);
  port_key_internal.port_orientation = key_toks[0][2];

  port_key_internal.column = std::stoi(key_toks[1]);
  port_key_internal.row = std::stoi(key_toks[3]);
  return port_key_internal;
}