from constants.node_constants import NodePorts, NodeAttributes
from builder.doc_builder import generate_id
from graph_objects.arrow import Arrow, ArrowWaypoint, ArrowMeta
from graph_objects.node import Node
from graph_objects.text_box import TextBox


class ConnectionManager:
    def __init__(
        self,
        node_dict: dict[str, Node],
        node_ports_single: tuple[dict[str, TextBox], dict[str, TextBox]],
        node_ports_multi: tuple[dict[str, list[TextBox]], dict[str, list[TextBox]]]
    ):
        self.node_dict: dict[str, Node] = node_dict
        self.node_ports_input: dict[str, TextBox] = node_ports_single[0]
        self.node_ports_output: dict[str, TextBox] = node_ports_single[1]
        self.node_ports_input_multi: dict[str, list[TextBox]] = node_ports_multi[0]
        self.node_ports_output_multi: dict[str, list[TextBox]] = node_ports_multi[1]
        self.connection_dict_single: dict[str, Arrow] = {}
        self.connection_dict_multi: dict[str, Arrow] = {}

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

    def create_connection_single(self, target_x, target_y, source_x, source_y, _id: str):
        connection_data = {
            "target-x": target_x,
            "target-y": target_y,
            "source-x": source_x,
            "source-y": source_y,
            "label": "",
            "connection-type": "",
            "style": None,
        }
        arrow = self.add_connection(connection_data)
        self.connection_dict_single[_id] = arrow

    def create_connection_multi(self, target_x, target_y, source_x, source_y, _id: str):
        connection_data = {
            "target-x": target_x,
            "target-y": target_y,
            "source-x": source_x,
            "source-y": source_y,
            "label": "",
            "connection-type": "",
            "style": None,
        }
        arrow = self.add_connection(connection_data)
        self.connection_dict_multi[_id] = arrow

    def create_connections_dict_left_single(self):
        for key, node in self.node_dict.items():
            multi_left = node.meta.__MULTI_CONNECTION_LEFT__
            multi_right = node.meta.__MULTI_CONNECTION_RIGHT__
            spanning = node.meta.__SPANNING_NODE__
            if multi_left or multi_right or spanning:
                continue

            target_y = self.calculate_connection_y(
                self.node_ports_input.get(node.meta.__ID__).y, NodePorts.height
            )
            target_x = node.right_ptr.x
            source_y = target_y
            source_x = node.x + NodeAttributes.width
            self.create_connection_single(
                target_x, target_y, source_x, source_y, node.meta.__ID__
            )

    def create_connections_dict_right_single(self, matrix_width: int):
        for key, node in self.node_dict.items():
            multi_left = node.meta.__MULTI_CONNECTION_LEFT__
            multi_right = node.meta.__MULTI_CONNECTION_RIGHT__
            spanning = node.meta.__SPANNING_NODE__
            if multi_left or multi_right or spanning:
                continue
            target_y = self.calculate_connection_y(
                self.node_ports_input.get(node.meta.__ID__).y, NodePorts.height
            )
            target_x = node.x
            source_y = target_y

            if node.meta.__COLUMN_INDEX__ == 0:
                source_x = self.calculate_connection_x(node.left_ptr.x, matrix_width)
            else:
                source_x = self.calculate_connection_x(
                    node.left_ptr.x, NodeAttributes.width
                )

            self.create_connection_single(
                target_x, target_y, source_x, source_y, node.meta.__ID__
            )

    def create_connections_dict_left_multi(self):
        for key, node in self.node_dict.items():
            if not self.node_ports_input_multi.get(node.meta.__ID__):
                continue
            for port in self.node_ports_input_multi.get(node.meta.__ID__):
                target_y = self.calculate_connection_y(port.y, NodePorts.height)
                target_x = node.right_ptr.x
                source_y = target_y
                source_x = node.x + NodeAttributes.width
                self.create_connection_multi(target_x, target_y, source_x, source_y, str(generate_id()))

    def create_connections_dict_right_multi(self, matrix_width: int):
        for key, node in self.node_dict.items():
            if not self.node_ports_input_multi.get(node.meta.__ID__):
                continue
            for port in self.node_ports_input_multi.get(node.meta.__ID__):
                target_y = self.calculate_connection_y(port.y, NodePorts.height)
                target_x = node.x
                source_y = target_y
                if node.meta.__COLUMN_INDEX__ == 0:
                    source_x = self.calculate_connection_x(node.left_ptr.x, matrix_width)
                else:
                    source_x = self.calculate_connection_x(node.left_ptr.x, NodeAttributes.width)

                self.create_connection_multi(target_x, target_y, source_x, source_y, str(generate_id()))

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
