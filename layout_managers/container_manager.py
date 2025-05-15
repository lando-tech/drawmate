from dataclasses import dataclass

from constants.constants import MX_GRAPH_XML_STYLES
from graph_objects.node import Node, NodeMetaData
from graph_objects.text_box import TextBox
from graph_objects.port import Port
from builder.node_meta_builder import NodeMetaBuilder
from builder.node_builder import NodeBuilder
from builder.port_builder import PortBuilder
from builder.doc_builder import generate_id
from constants.node_constants import NodeAttributes, NodePorts


@dataclass
class NodeContainer:
    meta: list[NodeMetaData]
    nodes: dict[str, Node]
    node_labels: dict[str, TextBox]


@dataclass
class PortContainerSingle:
    input_ports: dict[str, Port]
    output_ports: dict[str, Port]


@dataclass
class PortContainerMulti:
    input_ports: dict[str, list[Port]]
    output_ports: dict[str, list[Port]]


class ContainerManager:
    def __init__(self):
        self.node_meta_builder = NodeMetaBuilder()
        self.node_builder = NodeBuilder()
        self.port_builder = PortBuilder()

    def build_node_container(
        self, node_data: dict[str, list | str], orientation: str
    ) -> NodeContainer:
        meta = self.initialize_meta_array(node_data, orientation)
        nodes = self.initialize_node_dict(meta)
        node_labels = self.initialize_node_label_dict(nodes)
        return NodeContainer(
            meta,
            nodes,
            node_labels
        )

    def initialize_meta_array(
        self, node_data: dict[str, list | str], orientation: str
    ) -> list[NodeMetaData]:
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
            meta_list.append(
                self.node_meta_builder.init_node_meta(
                    node_attributes_left, int(col), int(row), orientation
                )
            )

        return meta_list

    def initialize_node_dict(
        self,
        metadata_array: list[NodeMetaData],
        node_width: int = None,
        node_height: int = None,
    ) -> dict[str, Node]:
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

    def build_port_container_single(
        self, node_dict: dict[str, Node]
    ) -> PortContainerSingle:
        return PortContainerSingle(
            self.initialize_single_port_input_dict(node_dict),
            self.initialize_single_port_output_dict(node_dict),
        )

    def build_port_container_multi(
        self, node_dict: dict[str, Node]
    ) -> PortContainerMulti:
        return PortContainerMulti(
            self.initialize_multi_port_input_dict(node_dict),
            self.initialize_multi_port_output_dict(node_dict),
        )

    def initialize_single_port_input_dict(
        self, node_dict: dict[str, Node]
    ) -> dict[str, Port]:
        port_dict = {}
        for key, node in node_dict.items():
            multi_left, multi_right = (
                node.meta.__MULTI_CONNECTION_LEFT__,
                node.meta.__MULTI_CONNECTION_RIGHT__,
            )
            spanning = node.meta.__SPANNING_NODE__
            if multi_left or multi_right or spanning:
                # print("Skipping multi connection input")
                continue
            x = int(node.attributes["x"])
            base_y = int(node.attributes["y"])
            height = int(node.attributes["height"])
            # current_port = self.node_builder.init_node_input_ports(
            #     x, base_y, height, node.input_label
            # )
            current_port = self.port_builder.init_port(x, base_y, NodePorts.width, NodePorts.height, node.input_label, node, MX_GRAPH_XML_STYLES["text-box-filled"])
            current_port.id = str(generate_id())
            port_dict[node.meta.__ID__] = current_port

        return port_dict

    def initialize_single_port_output_dict(
        self, node_dict: dict[str, Node]
    ) -> dict[str, Port]:
        port_dict = {}
        for key, node in node_dict.items():
            multi_left, multi_right = (
                node.meta.__MULTI_CONNECTION_LEFT__,
                node.meta.__MULTI_CONNECTION_RIGHT__,
            )
            spanning = node.meta.__SPANNING_NODE__
            if multi_left or multi_right or spanning:
                # print("Skipping multi connection output")
                continue
            x = node.attributes["x"]
            base_y = node.attributes["y"]
            height = int(node.attributes["height"])
            width = int(node.attributes["width"])
            # current_port = self.node_builder.init_node_output_ports(
            #     x, base_y, width, height, node.input_label
            # )
            current_port = self.port_builder.init_port(x, base_y, NodePorts.width, NodePorts.height, node.input_label, node, MX_GRAPH_XML_STYLES["text-box-filled"])
            current_port.id = str(generate_id())
            port_dict[node.meta.__ID__] = current_port

        return port_dict

    def initialize_multi_port_input_dict(
        self, node_dict: dict[str, Node]
    ) -> dict[str, list[Port]] | None:
        port_dict = {}
        for key, node in node_dict.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = int(node.attributes["x"])
            base_y = int(node.attributes["y"])
            height = int(node.attributes["height"])
            if input_port_array:
                port_array = []
                for port in input_port_array:
                    current_port = self.port_builder.init_port(x, base_y, NodePorts.width, NodePorts.height,
                                                               port, node,
                                                               MX_GRAPH_XML_STYLES["text-box-filled"])
                    current_port.id = str(generate_id())
                    # TODO This variable should be passed in to avoid mutation
                    base_y -= NodePorts.height
                    port_array.append(current_port)
                port_dict[node.meta.__ID__] = port_array

        return port_dict

    def initialize_multi_port_output_dict(
        self, node_dict: dict[str, Node]
    ) -> dict[str, list[Port]] | None:
        port_dict = {}
        for key, node in node_dict.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = int(node.attributes["x"])
            base_y = int(node.attributes["y"])
            height = int(node.attributes["height"])
            width = int(node.attributes["width"])
            if input_port_array:
                port_array = []
                for port in input_port_array:
                    current_port = self.port_builder.init_port(x, base_y, NodePorts.width, NodePorts.height,
                                                               port, node,
                                                               MX_GRAPH_XML_STYLES["text-box-filled"])
                    current_port.id = str(generate_id())
                    # TODO This variable should be passed in to avoid data mutation
                    base_y -= NodePorts.height
                    port_array.append(current_port)
                port_dict[node.meta.__ID__] = port_array

        return port_dict
