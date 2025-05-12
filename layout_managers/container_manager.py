from dataclasses import dataclass

from builder.doc_builder import generate_id
from constants.matrix_constants import MatrixPorts
from graph_objects.node import Node, NodeMetaData
from graph_objects.text_box import TextBox
from builder.node_meta_builder import NodeMetaBuilder
from builder.node_builder import NodeBuilder
from constants.node_constants import NodeAttributes

@dataclass
class NodeContainer:
    meta: list[NodeMetaData]
    nodes: dict[str, Node]

@dataclass
class PortContainer:
    input_ports: dict[str, TextBox]
    output_ports: dict[str, TextBox]
    node_labels: dict[str, TextBox]


class ContainerManager:
    def __init__(self):
        self.node_meta_builder = NodeMetaBuilder()
        self.node_builder = NodeBuilder()

    def build_node_container(self, node_data: dict[str, list | str], orientation: str) -> NodeContainer:
        meta = self.initialize_meta_array(node_data, orientation)
        nodes = self.initialize_node_dict(meta)
        return NodeContainer(
            meta,
            nodes,
        )

    def build_port_container(self, node_dict: dict[str, Node]):
        return PortContainer (
            self.initialize_node_port_input_dict(node_dict),
            self.initialize_node_port_output_dict(node_dict),
            self.initialize_node_label_dict(node_dict)
        )

    def initialize_meta_array(self, node_data: dict[str, list | str], orientation: str) -> list[NodeMetaData]:
        """
        Creates an array of NodeMetaData objects
        """
        meta_list = []
        for key, node in node_data.items():
            col, row = key.split("-")
            node_attributes_left = {
                "label": node[0],
                "input-labels": node[1],
                "output-labels": node[2],
                "connection-indexes-left": node[3],
                "connection-indexes-right": node[4],
            }
            meta_list.append(self.node_meta_builder.init_node_meta(node_attributes_left, int(col), int(row), orientation))

        return meta_list

    def initialize_node_dict(self, metadata_array: list[NodeMetaData], node_width: int = None, node_height: int = None) -> dict[str, Node]:
        node_dict = {}
        node_attributes = {
            "x": 0,
            "y": 0,
            "width": node_width if node_width else NodeAttributes.width,
            "height": node_height if node_height else NodeAttributes.height,
            "label": "",
            "input_label": "",
            "output_label": "",
        }
        for meta in metadata_array:
            node = self.node_builder.init_node(node_attributes, meta)
            node.attributes["label"] = meta.__LABEL__
            node.input_label = meta.__INPUT_LABEL__
            node.output_label = meta.__OUTPUT_LABEL__
            node_dict[f"{meta.__COLUMN_INDEX__}-{meta.__ROW_INDEX__}"] = node

        return node_dict

    def initialize_node_label_dict(self, node_dict: dict[str, Node]):
        node_label_dict = {}
        for key, node in node_dict.items():
            node_label = self.node_builder.init_node_label(node)
            node_label_dict[node.meta.__ID__] = node_label

        return node_label_dict

    def initialize_node_port_input_dict(self, node_dict: dict[str, Node]) -> dict[str, TextBox]:
        port_dict = {}
        for key, node in node_dict.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            if input_port_array:
                for port in input_port_array:
                    current_port = self.node_builder.init_node_input_ports(x, base_y, height, port)
                    current_port.id = str(generate_id())
                    base_y -= MatrixPorts.port_spacing
                    port_dict[current_port.id] = current_port
            else:
                current_port = self.node_builder.init_node_input_ports(x, base_y, height, node.input_label)
                current_port.id = str(generate_id())
                port_dict[current_port.id] = current_port

        return port_dict

    def initialize_node_port_output_dict(self, node_dict: dict[str, Node]) -> dict[str, TextBox]:
        port_dict = {}
        for key, node in node_dict.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            width = int(node.attributes["width"])
            if input_port_array:
                for port in input_port_array:
                    current_port = self.node_builder.init_node_output_ports(x, base_y, width, height, port)
                    current_port.id = str(generate_id())
                    base_y -= MatrixPorts.port_spacing
                    port_dict[current_port.id] = current_port
            else:
                current_port = self.node_builder.init_node_output_ports(x, base_y, width, height, node.input_label)
                current_port.id = str(generate_id())
                port_dict[current_port.id] = current_port

        return port_dict