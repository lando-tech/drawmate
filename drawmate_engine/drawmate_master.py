from xml.dom.minidom import Element

# from drawmate_engine.drawmate_config import DrawmateConfig
from builder.node_builder import NodeBuilder
from builder.node_meta_builder import NodeMetaBuilder
from builder.matrix_builder import MatrixBuilder
from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder
from graph_objects.matrix import Matrix
from graph_objects.node import Node, NodeMetaData
from graph_objects.text_box import TextBox
from graph_objects.rect import Rect


class DrawmateMaster(DocBuilder, MxBuilder):
    def __init__(self, matrix_builder: MatrixBuilder, node_builder: NodeBuilder):
        super().__init__()
        self.matrix_builder: MatrixBuilder = matrix_builder
        self.node_builder: NodeBuilder = node_builder

    def draw_matrix(self) -> None:
        matrix_obj: Matrix = self.matrix_builder.init_matrix()
        matrix_elem: Element = self.create_mxcell(
            data=matrix_obj.attributes, __id__=matrix_obj.meta.__ID__, has_label=False
        )
        self.root.appendChild(matrix_elem)

    def draw_matrix_label(self) -> None:
        matrix_label: TextBox = self.matrix_builder.init_matrix_label()
        matrix_label_elem: Element = self.create_mxcell(data=matrix_label.attributes)
        self.root.appendChild(matrix_label_elem)

    def draw_matrix_ports(self, spacing: int, connection_labels: tuple[list[str], list[str]]) -> None:
        """
        Draws and initializes the matrix ports and attaches them to the root element.

        This function leverages the matrix builder to initialize a set of matrix
        ports based on the provided spacing and connection labels. Each generated
        port is then used to create an mxCell, which is appended to the root element
        of the object.

        Args:
            spacing (int): Integer value that determines the spacing between matrix ports.
            connection_labels (tuple[list[str], list[str]]: A tuple containing two lists. Each list represents
                the labels for the connections in the matrix.

        """
        matrix_ports: list[TextBox] = self.matrix_builder.init_matrix_ports(
            spacing=spacing, connection_labels=connection_labels
        )
        for port in matrix_ports:
            self.root.appendChild(self.create_mxcell(data=port.attributes))

    def draw_node(self, node: Node) -> None:
        node_elem: Element = self.create_mxcell(node.attributes, __id__=node.meta.__ID__, has_label=False)
        self.root.appendChild(node_elem)

    def draw_node_label(self, node: Node) -> None:
        node_label: Rect = self.node_builder.init_node_label(node)
        node_label_elem: Element = self.create_mxcell(data=node_label.attributes)
        self.root.appendChild(node_label_elem)

    def draw_node_ports_input(self, x: int, y: int, height: int, label: str) -> None:
        node_port: TextBox = self.node_builder.init_node_input_ports(x, y, height, label)
        node_port_elem: Element = self.create_mxcell(data=node_port.attributes)
        self.root.appendChild(node_port_elem)

    def draw_node_ports_output(self, x: int, y: int, width: int, height: int, label: str) -> None:
        node_port: TextBox = self.node_builder.init_node_output_ports(x, y, width, height, label)
        node_port_elem: Element = self.create_mxcell(data=node_port.attributes)
        self.root.appendChild(node_port_elem)

    def create_node(self, node_attributes: dict, node_meta: NodeMetaData = None) -> Node:
        return self.node_builder.init_node(node_attributes, node_meta)

    def create_node_metadata(self, node_attributes: dict, col_index: int, row_index: int, side: str) -> NodeMetaData:
        """Creates a node metadata object with the provided attributes.

        Args:
            node_attributes (dict): Dictionary containing node attributes with the following structure:
                {
                    "label": str,                     # Node label - __SPAN__ if the node is a span or a blank string
                    "input-labels": str | list[str],  # Input port label(s)
                    "output-labels": str | list[str], # Output port label(s)
                    "connection-indexes-left": list[int | str],  # Left connection indices ("NONE" for no connection)
                    "connection-indexes-right": list[int | str]  # Right connection indices ("NONE" for no connection)
                }
            col_index (int): Column index of the node in the grid
            row_index (int): Row index of the node in the grid
            side (str): Side of the matrix ("left" or "right")

        Returns:
            NodeMetaData: Initialized node metadata object

        Example:
            node_attributes = {
                "label": "AV Appliance",
                "input-labels": ["HDMI", "HDMI"],
                "output-labels": ["HDMI", "HDMI"],
                "connection-indexes-left": ["NONE"],
                "connection-indexes-right": [1, 3]
            }
            metadata = create_node_metadata(node_attributes, 0, 1, "left")
        """
        node_meta_builder = NodeMetaBuilder()
        return node_meta_builder.init_node_meta(
            node_attributes=node_attributes,
            col_index=col_index,
            row_index=row_index,
            side=side
        )


# if __name__ == "__main__":
#     dc = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
#     matrix_builder: MatrixBuilder = MatrixBuilder(dc.get_matrix_dimensions())
#     node_builder: NodeBuilder = NodeBuilder()
#     dm = DrawmateMaster(matrix_builder, node_builder)
#     dm.draw_matrix()
#     dm.draw_matrix_label()
#     dm.draw_matrix_ports(120, dc.get_matrix_connection_labels())
#     dm.create_xml("/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml")
