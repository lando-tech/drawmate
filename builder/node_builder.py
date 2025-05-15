from constants.matrix_constants import MatrixPorts
from graph_objects.node import Node, NodeMetaData
from graph_objects.rect import Rect
from constants.node_constants import NodePorts, NodeLabels, NodeAttributes


class NodeBuilder:

    def init_node(self, node_attributes: dict, node_meta: NodeMetaData = None) -> Node:
        x = node_attributes["x"]
        y = node_attributes["y"]
        label = node_attributes["label"]
        input_label = node_attributes["input_label"]
        output_label = node_attributes["output_label"]
        width = node_attributes["width"]

        if node_meta:
            if node_meta.__INPUT_LABEL_ARRAY__ or node_meta.__OUTPUT_LABEL_ARRAY__:
                height = self.calculate_node_height(
                    len(node_meta.__INPUT_LABEL_ARRAY__), int(node_attributes["height"])
                )
            else:
                height = node_attributes["height"]
        else:
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
            width=int(node.attributes["width"]),
            height=NodeLabels.height,
            label=node.attributes["label"],
            _type="text-box",
        )

    @staticmethod
    def calculate_node_height(num_connections: int, current_height: int) -> int:
        total_height = (
            (num_connections * NodePorts.height)
            + NodeLabels.height # Account for the label at the top
            + NodeAttributes.y_spacing
        )
        return max(current_height, total_height)
