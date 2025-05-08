from graph_objects.node import Node, NodeMetaData
from graph_objects.rect import Rect
from constants.constants import MX_GRAPH_XML_STYLES
from constants.node_constants import NodePorts, NodeLabels
from graph_objects.text_box import TextBox


class NodeBuilder:

    def init_node(self, node_attributes: dict, node_meta: NodeMetaData = None) -> Node:
        x = node_attributes["x"]
        y = node_attributes["y"]
        label = node_attributes["label"]
        input_label = node_attributes["input_label"]
        output_label = node_attributes["output_label"]
        width = node_attributes["width"]
        height = node_attributes["height"]
        return Node(
            x=x,
            y=y,
            label=label,
            input_label=input_label,
            output_label=output_label,
            width=width,
            height=height,
            meta=node_meta,
        )

    def init_node_label(self, node: Node) -> Rect:
        return Rect(
            x=node.x,
            y=node.y,
            width=NodeLabels.width,
            height=NodeLabels.height,
            label=node.attributes["label"],
            _type="text-box",
        )

    def init_node_input_ports(self, x: int, y: int, height: int, label: str) -> TextBox:
        input_x, input_y = self.calculate_input_offset(x, y, height)
        return TextBox(
            x=input_x,
            y=input_y,
            width=NodePorts.width,
            height=NodePorts.height,
            label=label,
            _type="text-box",
            style=MX_GRAPH_XML_STYLES["input-text-box"],
        )

    def init_node_output_ports(
        self, x: int, y: int, width: int, height: int, label: str
    ) -> TextBox:
        output_x, output_y = self.calculate_output_offset(x, y, height, width)
        return TextBox(
            x=output_x,
            y=output_y,
            width=NodePorts.width,
            height=NodePorts.height,
            label=label,
            _type="text-box",
            style=MX_GRAPH_XML_STYLES["output-text-box"],
        )

    @staticmethod
    def calculate_node_height(num_connections: int, current_height: int) -> int:
        pass

    @staticmethod
    def calculate_input_offset(x: int, y: int, height: int) -> tuple[int, int]:
        x = x + NodePorts.x_offset
        y = y + (height // 2)
        return x, y

    @staticmethod
    def calculate_output_offset(
        x: int, y: int, height: int, width: int
    ) -> tuple[int, int]:
        x = x + (width - NodePorts.width) - NodePorts.x_offset
        y = y + (height // 2)
        return x, y
