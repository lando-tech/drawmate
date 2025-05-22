# from xml.dom.minidom import Element

from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder, generate_id


class DrawmateRenderer(DocBuilder, MxBuilder):
    def __init__(self):
        super().__init__()

    def draw_node(self, attributes: dict, has_label: bool = False):
        node_elem = self.create_mxcell(attributes, str(generate_id()), has_label)
        self.root.appendChild(node_elem)

    def draw_connection(self, attributes: dict, has_label: bool = False):
        connection_elem = self.create_mxcell_arrow(attributes, str(generate_id()))
        self.root.appendChild(connection_elem)