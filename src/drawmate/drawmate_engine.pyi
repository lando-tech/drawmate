from __future__ import annotations
import typing
__all__ = ['CentralNodeConfig', 'Graph', 'GridConfig', 'Label', 'LayoutConfig', 'Link', 'Node', 'NodeConfig', 'Port', 'PortConfig', 'WaypointLinks']
class CentralNodeConfig:
    """
    
            The CentralNodeConfig class is used to pass the width, height, and label height of the central node on the Graph.
        
    """
    def __init__(self, width: float, height: float, label_height: float) -> None:
        ...
class Graph:
    """
    
            The Graph class builds and manages diagram models, handling all node, port, and link objects.
    
            The Graph class maintains containers for nodes, ports, and links, as well as their lightweight export structs for Python integration.
            It tracks layout, grid, and node positions, manages creation and storage, and provides functions to ensure data consistency between C++ and Python.
            All state and ownership of objects are tightly controlled within the Graph class.
    
            Args:
                layout_config (LayoutConfig): Layout configuration for node and port positioning.
                grid_config (GridConfig): Grid configuration specifying columns and rows.
                central_node_config (CentralNodeConfig): Configuration for the central node.
                node_config (NodeConfig): Configuration for node dimensions.
                port_config (PortConfig): Configuration for port dimensions.
    
            Methods:
                add_node(node_meta_data, port_labels_left, port_labels_right, connection_indexes_left, connection_indexes_right)
                    Adds a node to the graph with the specified metadata, port labels, and connection indexes.
    
                connect_nodes()
                    Connects nodes in the graph by adding outgoing links.
    
                get_nodes()
                    Returns a dictionary of node exports representing all nodes in the graph.
    
                get_ports()
                    Returns a dictionary of port exports representing all ports in the graph.
    
                get_links()
                    Returns a list of link exports representing all links in the graph.
    
                get_node_ids()
                    Returns a list of all node IDs in the graph.
    
                get_node_ids_left()
                    Returns a list of node IDs on the left side of the graph.
    
                get_node_ids_right()
                    Returns a list of node IDs on the right side of the graph.
    
                debug_print_node_data()
                    Prints debug information for all nodes in the graph.
            
    """
    def __init__(self, layout_config: LayoutConfig, grid_config: GridConfig, central_node_config: CentralNodeConfig, node_config: NodeConfig, port_config: PortConfig) -> None:
        """
                    Constructs a Graph object.
        
                    Args:
                        layout_config (LayoutConfig): Layout configuration for node and port positioning.
                        grid_config (GridConfig): Grid configuration specifying columns and rows.
                        central_node_config (CentralNodeConfig): Configuration for the central node.
                        node_config (NodeConfig): Configuration for node dimensions.
                        port_config (PortConfig): Configuration for port dimensions.
        """
    def add_node(self, node_meta_data: dict[str, str], port_labels_left: list[str], port_labels_right: list[str], connection_indexes_left: list[int], connection_indexes_right: list[int]) -> None:
        """
                    Adds a node to the graph with the specified metadata, port labels, and connection indexes.
                    Args:
                        node_meta_data (dict): Metadata for the node, including label, type, and orientation.
                        port_labels_left (list): Labels for ports on the left side of the node.
                        port_labels_right (list): Labels for ports on the right side of the node.
                        connection_indexes_left (list): Connection indexes for left ports.
                        connection_indexes_right (list): Connection indexes for right ports.
        """
    @typing.overload
    def connect_nodes(self) -> None:
        """
                    Connects nodes in the graph by adding outgoing links.
        """
    @typing.overload
    def connect_nodes(self) -> None:
        """
                    Connects nodes in the graph by adding outgoing links.
        """
    def get_links(self) -> list[Link]:
        """
                    Returns a list of link exports representing all links in the graph.
        """
    def get_node_ids(self) -> list[str]:
        """
                    Returns a list of all node IDs in the graph.
        """
    def get_node_ids_left(self) -> list[str]:
        """
                    Returns a list of node IDs on the left side of the graph.
        """
    def get_node_ids_right(self) -> list[str]:
        """
                    Returns a list of node IDs on the right side of the graph.
        """
    def get_nodes(self) -> dict[str, Node]:
        """
                    Returns a dictionary of node exports representing all nodes in the graph.
        """
    def get_ports(self) -> dict[str, Port]:
        """
                    Returns a dictionary of port exports representing all ports in the graph.
        """
class GridConfig:
    """
    
            The GridConfig class is used to pass the number of columns and rows for both left and right sides of the grid to the Graph object.
            
    """
    def __init__(self, columns_left: int, columns_right: int, rows_left: int, rows_right: int) -> None:
        """
                    Constructs a GridConfig object.
                    Args:
                        columns_left (int): Number of columns on the left side of the grid.
                        columns_right (int): Number of columns on the right side of the grid.
                        rows_left (int): Number of rows on the left side of the grid.
                        rows_right (int): Number of rows on the right side of the grid.
        """
    @property
    def num_columns_left(self) -> int:
        """
        Number of columns on the left side of the grid.
        """
    @num_columns_left.setter
    def num_columns_left(self, arg0: int) -> None:
        ...
    @property
    def num_columns_right(self) -> int:
        """
        Number of columns on the right side of the grid.
        """
    @num_columns_right.setter
    def num_columns_right(self, arg0: int) -> None:
        ...
    @property
    def num_rows_left(self) -> int:
        """
        Number of rows on the left side of the grid.
        """
    @num_rows_left.setter
    def num_rows_left(self, arg0: int) -> None:
        ...
    @property
    def num_rows_right(self) -> int:
        """
        Number of rows on the right side of the grid.
        """
    @num_rows_right.setter
    def num_rows_right(self, arg0: int) -> None:
        ...
class Label:
    """
    
            The LabelExport class is used to export label information for nodes on the Graph.
            It contains the label name, source and target IDs, and position dimensions.
            These attributes are read-only to ensure the integrity of the Graph.
            
    """
    def __init__(self) -> None:
        ...
    @property
    def height(self) -> float:
        """
        The height of the label.
        """
    @property
    def name(self) -> str:
        """
        The name of the label.
        """
    @property
    def source_id(self) -> str:
        """
        The source ID of the label.
        """
    @property
    def target_id(self) -> str:
        """
        The target ID of the label.
        """
    @property
    def width(self) -> float:
        """
        The width of the label.
        """
    @property
    def x(self) -> float:
        """
        The x-coordinate of the label.
        """
    @property
    def y(self) -> float:
        """
        The y-coordinate of the label.
        """
class LayoutConfig:
    """
    
            The LayoutConfig class is used to pass base axis parameters and axis spacing to the Graph object.
            
    """
    def __init__(self, base_x: float, base_y: float, node_spacing_x_axis: float, node_spacing_y_axis: float, port_spacing: float) -> None:
        """
                    Constructs a LayoutConfig object.
                    Args:
                        base_x (float): The base x-axis coordinate.
                        base_y (float): The base y-axis coordinate.
                        node_spacing_x_axis (float): Horizontal spacing between nodes.
                        node_spacing_y_axis (float): Vertical spacing between nodes.
                        port_spacing (float): Spacing between ports on a node.
        """
    @property
    def base_x(self) -> float:
        """
        The base x-axis coordinate.
        """
    @base_x.setter
    def base_x(self, arg0: float) -> None:
        ...
    @property
    def base_y(self) -> float:
        """
        The base y-axis coordinate.
        """
    @base_y.setter
    def base_y(self, arg0: float) -> None:
        ...
    @property
    def node_spacing_x_axis(self) -> float:
        """
        Horizontal spacing between nodes
        """
    @node_spacing_x_axis.setter
    def node_spacing_x_axis(self, arg0: float) -> None:
        ...
    @property
    def node_spacing_y_axis(self) -> float:
        """
        Vertical spacing between nodes.
        """
    @node_spacing_y_axis.setter
    def node_spacing_y_axis(self, arg0: float) -> None:
        ...
    @property
    def port_spacing(self) -> float:
        """
        Spacing between ports on a node.
        """
    @port_spacing.setter
    def port_spacing(self, arg0: float) -> None:
        ...
class Link:
    """
    
            The LinkExport class is used to export link information between nodes on the Graph.
            It contains the source and target coordinates, as well as the IDs of the connected nodes/ports.
            These attributes are read-only to ensure the integrity of the Graph.
        
    """
    def __init__(self) -> None:
        ...
    @property
    def _id(self) -> str:
        """
        The ID of the link.
        """
    @property
    def has_waypoints(self) -> bool:
        """
        Indicates if the link has waypoints.
        """
    @property
    def source_id(self) -> str:
        """
        The source ID of the link.
        """
    @property
    def source_x(self) -> float:
        """
        The x-coordinate of the source node.
        """
    @property
    def source_y(self) -> float:
        """
        The y-coordinate of the source node.
        """
    @property
    def target_id(self) -> str:
        """
        The target ID of the link.
        """
    @property
    def target_x(self) -> float:
        """
        The x-coordinate of the target node.
        """
    @property
    def target_y(self) -> float:
        """
        The y-coordinate of the target node.
        """
    @property
    def waypoints(self) -> list[WaypointLinks]:
        """
        The waypoints of the link.
        """
class Node:
    """
    
            The NodeExport class is used to export node information on the Graph.
            It contains the node's label, position, dimensions, and IDs for the source and target.
            These attributes are read-only to ensure the integrity of the Graph.
        
    """
    def __init__(self) -> None:
        ...
    @property
    def height(self) -> float:
        """
        The height of the node.
        """
    @property
    def label(self) -> Label:
        """
        The label object of the node.
        """
    @property
    def name(self) -> str:
        """
        The label/name of the node.
        """
    @property
    def source_id(self) -> str:
        """
        The source ID of the node.
        """
    @property
    def target_id(self) -> str:
        """
        The target ID of the node.
        """
    @property
    def width(self) -> float:
        """
        The width of the node.
        """
    @property
    def x(self) -> float:
        """
        The x-coordinate of the node.
        """
    @property
    def y(self) -> float:
        """
        The y-coordinate of the node.
        """
class NodeConfig:
    """
    
            The NodeConfig class is used to pass the width, height, and label height of each node on the Graph.
            
    """
    def __init__(self, width: float, height: float, label_height: float) -> None:
        """
                    Constructs a NodeConfig object.
                    Args:
                        width (float): The width of the node.
                        height (float): The height of the node.
                        label_height (float): The height of the label on the node.
        """
class Port:
    """
    
            The PortExport class is used to export port information on the Graph.
            It contains the position and dimensions of the port, as well as the IDs of the connected ports.
            These attributes are read-only to ensure the integrity of the Graph.
        
    """
    def __init__(self) -> None:
        ...
    @property
    def height(self) -> float:
        """
        The height of the port.
        """
    @property
    def name(self) -> str:
        """
        The name of the port.
        """
    @property
    def source_id(self) -> str:
        """
        The source ID of the port.
        """
    @property
    def target_id(self) -> str:
        """
        The target ID of the port.
        """
    @property
    def width(self) -> float:
        """
        The width of the port.
        """
    @property
    def x(self) -> float:
        """
        The x-coordinate of the port.
        """
    @property
    def y(self) -> float:
        """
        The y-coordinate of the port.
        """
class PortConfig:
    """
    
            The PortConfig class is used to pass the width and height of each port on the Graph.
        
    """
    def __init__(self, port_width: float, port_height: float) -> None:
        """
                    Constructs a PortConfig object.
                    Args:
                        port_width (float): The width of each port.
                        port_height (float): The height of each port.
        """
    @property
    def port_height(self) -> float:
        """
        The height of each port.
        """
    @port_height.setter
    def port_height(self, arg0: float) -> None:
        ...
    @property
    def port_width(self) -> float:
        """
        The width of each port.
        """
    @port_width.setter
    def port_width(self, arg0: float) -> None:
        ...
class WaypointLinks:
    """
    
            The WaypointLinks class is used to export waypoint information for links on the Graph.
            It contains the x and y coordinates of the waypoints.
            These attributes are read-only to ensure the integrity of the Graph.
        
    """
    def __init__(self) -> None:
        ...
    @property
    def source_x(self) -> float:
        """
        The x-coordinate of the waypoint.
        """
    @property
    def source_y(self) -> float:
        """
        The y-coordinate of the waypoint.
        """
    @property
    def target_x(self) -> float:
        """
        The x-coordinate of the target waypoint.
        """
    @property
    def target_y(self) -> float:
        """
        The y-coordinate of the target waypoint.
        """
