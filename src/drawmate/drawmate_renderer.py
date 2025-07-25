# from xml.dom.minidom import Element
# import sys
# import os
# from .pathfinder import PathFinder

# pf = PathFinder()
# root_dir = pf.get_project_dir()
# sys.path.insert(0, f"{root_dir}/engine/build")
# os.path.join(os.path.dirname(__file__), 'drawmate_engine.cpython-313-x86_64-linux-gnu.so')
import drawmate_engine
from .mx_builder import MxBuilder
from .doc_builder import DocBuilder
from .drawmate_config import DrawmateConfig
from .constants import MX_GRAPH_XML_STYLES


class DrawmateRenderer(DocBuilder, MxBuilder):
    def __init__(self, config_file):
        super().__init__()
        self.set_graph_values(4000, 4000, 4000, 4000)
        self.config = DrawmateConfig(config_file)
        self.matrix_dims = self.config.get_matrix_dimensions()
        self.graph = self.init_graph()
        self.node_meta_tuple = self.config.build_node_dict(self.matrix_dims.num_connections)
        self.left_nodes = self.node_meta_tuple[0]
        self.right_nodes = self.node_meta_tuple[1]

    def draw_node(self, attributes: dict, _id:str, has_label: bool = False):
        node_elem = self.create_mxcell(attributes, _id, has_label)
        self.root.appendChild(node_elem)

    def draw_node_with_target(self, attributes: dict, __id__: str, source_id: str, target_id: str, has_label: bool = False):
        node_elem = self.create_mxcell_with_target(attributes, __id__, source_id, target_id)
        self.root.appendChild(node_elem)

    def draw_connection(self, attributes: dict, __id__: str, has_label: bool = False):
        connection_elem = self.create_mxcell_arrow(attributes, __id__=__id__, has_label=has_label)
        self.root.appendChild(connection_elem)

    def init_graph(self):
        # TODO Fix Pylance warnings, stub file is present, but not being recognized
        # TODO Port spacing, node spacing (y), label and port height(s) should be a calculated ration based on
        # the height of the Nodes. Remove these from the user facing exports
        layout_config = drawmate_engine.LayoutConfig( # type: ignore
            base_x=2000.0,
            base_y=2000.0,
            node_spacing_x_axis=250.0,
            node_spacing_y_axis=23.33,
            port_spacing=70.0
        )
        grid_config = drawmate_engine.GridConfig( # type: ignore
            # TODO Add bounds checking to ensure these variables are accurate on the backend to ensure graph integrity
            columns_left=self.config.num_levels,
            columns_right=self.config.num_levels,
            rows_left=self.matrix_dims.num_connections,
            rows_right=self.matrix_dims.num_connections
        )
        central_node_config = drawmate_engine.CentralNodeConfig( # type: ignore
            width=200.0,
            height=200.0,
            label_height=23.33
        )
        node_config = drawmate_engine.NodeConfig( # type: ignore
            width=120.0,
            height=70.0,
            label_height=23.33,
        )
        port_config = drawmate_engine.PortConfig( # type: ignore
            # TODO Port width should be calculated on the backend to ensure proper placement.
            # Calculation is 1/2 the width of the node
            port_width=60.0,
            port_height=23.33
        )
        graph = drawmate_engine.Graph(layout_config, grid_config, central_node_config, node_config, port_config) # type: ignore
        return graph

    def init_matrix(self):
        matrix_meta = {
            "node-type": "video-matrix",
            "node-orientation": "center",
            "node-label": self.matrix_dims.label
        }
        conn_indexes_left = [i for i in range(self.matrix_dims.num_connections)]
        conn_indexes_right = [i for i in range(self.matrix_dims.num_connections)]
        matrix_ports_left, matrix_ports_right = self.config.get_matrix_connection_labels()

        self.graph.add_node(matrix_meta, matrix_ports_left, matrix_ports_right, conn_indexes_left, conn_indexes_right)

    def init_nodes(self, orientation: str):
        if orientation == "left":
            nodes = self.left_nodes
        else:
            nodes = self.right_nodes

        for k, v in nodes.items():

            # col = int(k.split("-")[1])
            row = int(k.split("-")[2])

            node_meta = {}
            if v[0].strip() == "__SPAN__" or v[0].strip() == "":
                node_meta["node-type"] = "__SPAN__"
            else:
                node_meta["node-type"] = "appliance"
            node_meta["node-orientation"] = orientation
            node_meta["node-label"] = v[0]

            if isinstance(v[1], list):
                port_labels_left = v[1]
            else:
                port_labels_left = [v[1]]

            if isinstance(v[2], list):
                port_labels_right = v[2]
            else:
                port_labels_right = [v[2]]

            if len(v[3]) > 1:
                conn_indexes_left = v[3]
            else:
                conn_indexes_left = [row]

            if len(v[4]) > 1:
                conn_indexes_right = v[4]
            else:
                conn_indexes_right = [row]

            self.graph.add_node(node_meta, port_labels_left, port_labels_right, conn_indexes_left, conn_indexes_right) # type: ignore

    def link_nodes(self, has_label: bool = False):
        # Only call after all nodes have been added to the graph
        self.graph.connect_nodes()
        links = self.graph.get_links()
        # print(links)
        for link in links:
            link_attributes = {
                "source_x": link.source_x,
                "source_y": link.source_y,
                "target_x": link.target_x,
                "target_y": link.target_y,
                "style": MX_GRAPH_XML_STYLES["arrow"],
                "label": link.label #type: ignore
            }
            self.draw_connection(link_attributes, link._id, has_label)

    def render_nodes(self):
        nodes_export = self.graph.get_nodes()
        node_ids = self.graph.get_node_ids()
        for i in node_ids:
            try:
                node = nodes_export.get(i)
            except IndexError:
                continue

            # print(node.source_id)

            attributes = {
                "x": node.x, # type: ignore
                "y": node.y, # type: ignore
                "label": node.name, # type: ignore
                "width": node.width, # type: ignore
                "height": node.height, # type: ignore
                "style": MX_GRAPH_XML_STYLES["rect"]
            }
            label_attributes = {
                "x": node.label.x, # type: ignore
                "y": node.label.y, # type: ignore
                "label": node.label.name, # type: ignore
                "width": node.label.width, # type: ignore
                "height": node.label.height, # type: ignore
                "style": MX_GRAPH_XML_STYLES["text-box-filled"]
            }

            self.draw_node(attributes, node.source_id) # type: ignore
            self.draw_node(label_attributes, node.label.source_id, has_label=True) # type: ignore

        ports = self.graph.get_ports()
        for key, port in ports.items():

            port_attributes = {
                "x": port.x,
                "y": port.y,
                "label": port.name,
                "width": port.width,
                "height": port.height,
                "style": MX_GRAPH_XML_STYLES["text-box"]
            }
            # print(port.source_id)
            self.draw_node(port_attributes, port.source_id, has_label=True)

    def test_nodes(self):
        # for key, node in self.graph.get_nodes().items():
        #     print(key, node)

        self.graph.connect_nodes()
        links = self.graph.get_links()
        for link in links:
            print(link.source_id, link.target_id)



# if __name__ == "__main__":
#     config_file = f"{root_dir}/test_templates/mc_test_1.json"
#     output_file = "/home/landotech/Desktop/output.drawio"
#     draw = DrawmateRenderer(config_file)
#     draw.init_matrix()
#     draw.init_nodes("left")
#     draw.init_nodes("right")
#     # draw.test_nodes()
#     draw.render_nodes()
#     draw.link_nodes()
#     draw.create_xml(output_file)
#     print(f"Template creation successful. File saved @ {output_file}")
