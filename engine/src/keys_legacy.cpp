
/*
 * This is the monstrosity that made the first version of my system work.
 * I couldn't get rid of it entirely, because it was a thing of beauty and horror.
 * This is the reason why I moved to struct based keys, a hard lesson learned from 
 * the hell below. If anyone is reading this, I hope you get a laugh and can appreciate
 * my journey of learning C++ and building engines. Cheers!
 */
/* std::string get_adjacent_port_key_string(const std::string &key, PortOrientation port_orientation, NodeOrientation node_orientation)
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

std::string get_adjacent_key_string(const std::string &key,
                             NodeOrientation node_orientation,
                             GridOrientation grid_orientation)
{
  /*
   * Takes in the current key, current node orientation, and the adjacency of the neighbor
   * as described in the Grid Orientation enum class. It will return the adjacent key, and
   * ensure the conversion of stoi is handled properly.
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

std::string get_adjacent_key_string_from_center(NodeOrientation node_orientation,
                                         int port_index)
{
  /*
   * Takes in the port index of the desired node, and the orientation of the desired node.
   * It will always return a node at column 0, because directly adjacent nodes, in
   * reference to the matrix, are always at column 0. Port indexes are set to match
   * the row of the parent node.
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
*/