from xml.dom.minidom import Element

from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder
from graph_objects.arrow import Arrow
from graph_objects.matrix import Matrix
from graph_objects.node import Node
from graph_objects.text_box import TextBox


class DrawmateMaster(DocBuilder, MxBuilder):
    def __init__(self):
        super().__init__()

    def draw_matrix(self, matrix: Matrix) -> None:
        matrix_elem: Element = self.create_mxcell(
            data=matrix.attributes, __id__=matrix.meta.__ID__, has_label=False
        )
        self.root.appendChild(matrix_elem)

    def draw_matrix_label(self, matrix_label: TextBox) -> None:
        matrix_label_elem: Element = self.create_mxcell(data=matrix_label.attributes)
        self.root.appendChild(matrix_label_elem)

    def draw_matrix_ports(self, matrix_ports: list[TextBox]) -> None:
        for port in matrix_ports:
            self.root.appendChild(self.create_mxcell(data=port.attributes))

    def draw_node(self, node: Node) -> None:
        node_elem: Element = self.create_mxcell(
            node.attributes, __id__=node.meta.__ID__, has_label=False
        )
        self.root.appendChild(node_elem)

    def draw_node_label(self, node_label: TextBox) -> None:
        node_label_elem: Element = self.create_mxcell(data=node_label.attributes)
        self.root.appendChild(node_label_elem)

    def draw_node_ports_input(self, node_port: TextBox):
        node_port_elem: Element = self.create_mxcell(data=node_port.attributes)
        self.root.appendChild(node_port_elem)

    def draw_connection(self, connection_arrow: Arrow):
        connection_elem = self.create_mxcell_arrow(connection_arrow.attributes)
        self.root.appendChild(connection_elem)
