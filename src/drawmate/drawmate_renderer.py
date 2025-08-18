from drawmate.doc_builder import DocBuilder
from drawmate.mx_builder import MxBuilder
from drawmate.drawmate_grid_layout import DrawmateGridLayout
from drawmate.drawmate_node import DrawmateNode
from drawmate.constants import MX_GRAPH_XML_STYLES
from drawmate.id_utils import get_key_row, get_key_column, get_key_orientation


class DrawmateRenderer(DocBuilder, MxBuilder):
    def __init__(self, output_path: str, layout_mgr: DrawmateGridLayout) -> None:
        super().__init__()
        self.output_path = output_path
        self.layout_mgr = layout_mgr

    def render_node(self, attributes: dict, __id__: str = "", has_label: bool = False):
        node_elem = self.create_mxcell(attributes, __id__=__id__, has_label=has_label)
        self.root.appendChild(node_elem)

    def render_link(
        self, attributes: dict, source_id, target_id, has_label: bool = False
    ):
        link_elem = self.create_mxcell_with_target(
            attributes, "", source_id, target_id, has_label=has_label
        )
        self.root.appendChild(link_elem)

    def render_graph(self, add_timestamp: bool = False):
        self.create_xml(self.output_path, add_timestamp=add_timestamp)

    def iterate_render_nodes(self, label_height):
        for key, node in self.layout_mgr.left_nodes.items():
            if node.label.strip() == "__SPAN__" or node.label.strip() == "":
                continue
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            self.render_node(attr)
            self.render_node(
                {
                    "width": node.width,
                    "height": label_height,
                    "label": node.label,
                    "x": node.x,
                    "y": node.y,
                    "style": MX_GRAPH_XML_STYLES["rect"],
                },
                has_label=True,
            )
            self.render_ports(node)

        for key, node in self.layout_mgr.right_nodes.items():
            if node.label.strip() == "__SPAN__" or node.label.strip() == "":
                continue
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            self.render_node(attr)
            self.render_node(
                {
                    "width": node.width,
                    "height": label_height,
                    "label": node.label,
                    "x": node.x,
                    "y": node.y,
                    "style": MX_GRAPH_XML_STYLES["rect"],
                },
                has_label=True,
            )
            self.render_ports(node)

    def render_ports(self, node: DrawmateNode):
        ports_input = node.ports_input
        ports_output = node.ports_output
        for port_l, port_r in zip(ports_input, ports_output):
            attr_l = {
                "width": port_l.width,
                "height": port_l.height,
                "x": port_l.x,
                "y": port_l.y,
                "label": port_l.label,
                "style": MX_GRAPH_XML_STYLES["text-box"],
            }
            attr_r = {
                "width": port_r.width,
                "height": port_r.height,
                "x": port_r.x,
                "y": port_r.y,
                "label": port_r.label,
                "style": MX_GRAPH_XML_STYLES["text-box"],
            }
            self.render_node(attr_l, port_l.id, has_label=True)
            self.render_node(attr_r, port_r.id, has_label=True)

    def iterate_render_links(self):
        port_links = self.layout_mgr.init_links()
        for key, port in port_links.items():
            attr = {
                "label": self.create_link_label(key),
                "style": MX_GRAPH_XML_STYLES["arrow"],
            }
            try:
                self.render_link(
                    attr, port.link.source_id, port.link.target_id, has_label=True
                )
            except AttributeError:
                # print("Link does not exist for this port")
                pass

    def create_link_label(self, key):
        key_row = get_key_row(key)
        key_col = get_key_column(key)
        key_orientation = get_key_orientation(key)
        if key_orientation == "L":
            if key_row + 1 >= 10:
                return f"0{key_col}{key_row + 1}"
            return f"0{key_col}0{key_row + 1}"
        elif key_orientation == "R":
            if key_row + 1 >= 10:
                return f"1{key_col+1}{key_row + 1}"
            return f"1{key_col+1}0{key_row + 1}"
        elif key_orientation == "C":
            if key_row + 1 >= 10:
                return f"1{key_col}{key_row + 1}"
            return f"1{key_col}0{key_row + 1}"


def create_diagram(input_path, output_path, add_timestamp: bool = False):
    layout_mgr = DrawmateGridLayout(input_path)
    layout_mgr.init_graph()
    renderer = DrawmateRenderer(output_path, layout_mgr)
    matrix = layout_mgr.matrix
    renderer.render_node(
        {
            "width": matrix.width,
            "height": matrix.height,
            "x": matrix.x,
            "y": matrix.y,
            "style": MX_GRAPH_XML_STYLES["rect"],
        }
    )
    renderer.render_node(
        {
            "width": matrix.width,
            "height": layout_mgr.spacing_mgr.label_height,
            "x": matrix.x,
            "y": matrix.y - layout_mgr.spacing_mgr.label_height,
            "label": matrix.label,
            "style": MX_GRAPH_XML_STYLES["rect"],
        },
        has_label=True,
    )
    renderer.render_ports(matrix)
    renderer.iterate_render_nodes(layout_mgr.spacing_mgr.label_height)
    renderer.iterate_render_links()
    renderer.render_graph(add_timestamp=add_timestamp)
