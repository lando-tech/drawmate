from drawmate.doc_builder import DocBuilder
from drawmate.mx_builder import MxBuilder
from drawmate.drawmate_grid_layout import DrawmateGridLayout
from drawmate.constants import MX_GRAPH_XML_STYLES


class DrawmateRenderer(DocBuilder, MxBuilder):
    def __init__(self, output_path: str, layout_mgr: DrawmateGridLayout) -> None:
        super().__init__()
        self.output_path = output_path
        self.layout_mgr = layout_mgr

    def render_node(self, attributes: dict, __id__: str = "", has_label: bool = False):
        print(attributes.get("x"), attributes.get("y"))
        node_elem = self.create_mxcell(attributes, __id__=__id__, has_label=has_label)
        self.root.appendChild(node_elem)

    def render_graph(self):
        self.create_xml(self.output_path)

    def iterate_render_nodes(self):
        for key, node in self.layout_mgr.left_nodes.items():
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "label": node.label,
                "style": MX_GRAPH_XML_STYLES["rect"]
            }
            self.render_node(attr)

        for key, node in self.layout_mgr.right_nodes.items():
            attr = {
                "width": node.width,
                "height": node.height,
                "x": node.x,
                "y": node.y,
                "label": node.label,
                "style": MX_GRAPH_XML_STYLES["rect"]
            }
            self.render_node(attr)

def main():
    layout_mgr = DrawmateGridLayout("/home/aaron/Projects/Portfolio/drawmate/test_templates/mc_test_1.json")
    layout_mgr.init_graph(enable_debug=True)
    renderer = DrawmateRenderer("/home/aaron/Documents/test.drawio", layout_mgr)
    matrix = layout_mgr.matrix
    renderer.render_node({
        "width": matrix.width,
        "height": matrix.height,
        "x": matrix.x,
        "y": matrix.y,
        "label": matrix.label,
        "style": MX_GRAPH_XML_STYLES["rect"]
    })
    renderer.iterate_render_nodes()
    renderer.render_graph()

if __name__ == "__main__":
    main()

