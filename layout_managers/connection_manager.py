from constants.matrix_constants import MatrixDimensions
from constants.node_constants import NodePorts, NodeAttributes
from graph_objects.arrow import Arrow, ArrowWaypoint, ArrowMeta
from graph_objects.node import Node
from graph_objects.text_box import TextBox


class ConnectionManager:
    def __init__(self, node_dict: dict[str, Node], node_ports: tuple[dict[str, TextBox], dict[str, TextBox]]):
        self.node_dict: dict[str, Node] = node_dict
        self.node_ports_input: dict[str, TextBox] = node_ports[0]
        self.node_ports_output: dict[str, TextBox] = node_ports[1]
        self.connection_dict: dict[str, Arrow] = {}

    def add_connection(self, connection_data: dict) -> Arrow:
        return Arrow(
            target_x=connection_data["target-x"],
            target_y=connection_data["target-y"],
            source_x=connection_data["source-x"],
            source_y=connection_data["source-y"],
            label=connection_data["label"],
            _type=connection_data["connection-type"],
            style=connection_data["style"],
        )

    def create_connections_dict_left(self):
        for key, node in self.node_dict.items():
            if node.meta.__SPANNING_NODE__:
                continue

            target_y = self.calculate_connection_y(self.node_ports_input.get(node.meta.__ID__).y, NodePorts.height)
            source_y = target_y
            source_x = node.x + NodeAttributes.width
            connection_data = {
                "target-x": node.right_ptr.x,
                "target-y": target_y,
                "source-x": source_x,
                "source-y": source_y,
                "label": "",
                "connection-type": "",
                "style": None
            }
            arrow = self.add_connection(connection_data)
            self.connection_dict[node.meta.__ID__] = arrow

    def create_connections_dict_right(self, matrix_width: int):
        for key, node in self.node_dict.items():
            if node.meta.__SPANNING_NODE__:
                continue

            target_y = self.calculate_connection_y(self.node_ports_input.get(node.meta.__ID__).y, NodePorts.height)
            source_y = target_y

            if node.meta.__COLUMN_INDEX__ == 0:
                source_x = self.calculate_connection_x(node.left_ptr.x, matrix_width)
            else:
                source_x = self.calculate_connection_x(node.left_ptr.x, NodeAttributes.width)

            connection_data = {
                "target-x": node.x,
                "target-y": target_y,
                "source-x": source_x,
                "source-y": source_y,
                "label": "",
                "connection-type": "",
                "style": None
            }
            arrow = self.add_connection(connection_data)
            self.connection_dict[node.meta.__ID__] = arrow



    def add_connection_waypoint(
        self, x: int, y: int, waypoint_meta: ArrowMeta = None
    ) -> ArrowWaypoint:
        return ArrowWaypoint(x=x, y=y, meta=waypoint_meta)

    def calculate_connection_x(self, x: int, width: int):
        return x + width

    def calculate_connection_y(self, y: int, height: int):
        return y + (height // 2)

    def calculate_waypoints(self):
        pass
