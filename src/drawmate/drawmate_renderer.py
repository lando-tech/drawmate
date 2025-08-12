from drawmate.doc_builder import DocBuilder
from drawmate.mx_builder import MxBuilder
from drawmate.drawmate_grid_layout import DrawmateGridLayout
from drawmate.drawmate_node import DrawmateNode
from drawmate.constants import MX_GRAPH_XML_STYLES


class DrawmateRenderer(DocBuilder, MxBuilder):
    def __init__(self, output_path: str, layout_mgr: DrawmateGridLayout) -> None:
        super().__init__()
        self.output_path = output_path
        self.layout_mgr = layout_mgr

    def render_node(self, attributes: dict, __id__: str = "", has_label: bool = False):
        node_elem = self.create_mxcell(attributes, __id__=__id__, has_label=has_label)
        self.root.appendChild(node_elem)

    def render_link(self, attributes: dict, source_id, target_id):
        link_elem = self.create_mxcell_with_target(attributes, "", source_id, target_id)
        self.root.appendChild(link_elem)

    def render_graph(self):
        self.create_xml(self.output_path)

    def iterate_render_nodes(self):
        for key, node in self.layout_mgr.left_nodes.items():
            if node.label.strip() == "__SPAN__" or node.label.strip() == "":
                continue
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "label": node.label,
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            self.render_node(attr)
            self.render_ports(node)

        for key, node in self.layout_mgr.right_nodes.items():
            if node.label.strip() == "__SPAN__" or node.label.strip() == "":
                continue
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "label": node.label,
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            self.render_node(attr)
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
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            attr_r = {
                "width": port_r.width,
                "height": port_r.height,
                "x": port_r.x,
                "y": port_r.y,
                "label": port_r.label,
                "style": MX_GRAPH_XML_STYLES["rect"],
            }
            self.render_node(attr_l, port_l.id, has_label=True)
            self.render_node(attr_r, port_r.id, has_label=True)

    def iterate_render_links(self):
        port_links = self.layout_mgr.init_links()
        for key, port in port_links.items():
            attr = {
                "label": "",
                "style": MX_GRAPH_XML_STYLES["arrow"]
            }
            try:
                self.render_link(attr, port.link.source_id, port.link.target_id)
            except AttributeError:
                # print("Link does not exist for this port")
                pass


def main():
    layout_mgr = DrawmateGridLayout(
        "/home/aaron/Projects/Portfolio/drawmate/test_templates/mc_test_1.json"
    )
    layout_mgr.init_graph()
    renderer = DrawmateRenderer("/home/aaron/Documents/test.drawio", layout_mgr)
    matrix = layout_mgr.matrix
    renderer.render_node(
        {
            "width": matrix.width,
            "height": matrix.height,
            "x": matrix.x,
            "y": matrix.y,
            "label": matrix.label,
            "style": MX_GRAPH_XML_STYLES["rect"],
        }
    )
    renderer.render_ports(matrix)
    renderer.iterate_render_nodes()
    renderer.iterate_render_links()
    renderer.render_graph()


if __name__ == "__main__":
    main()
