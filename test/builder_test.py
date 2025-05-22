import sys
import os

from constants.constants import MX_GRAPH_XML_STYLES
from drawmate_renderer.drawmate_config import DrawmateConfig
from drawmate_renderer.drawmate_renderer import DrawmateRenderer

drawmate_ren = DrawmateRenderer()
config_file = "/home/landotech/easyrok/drawmate/test_templates/mc_test_1.json"
output_file = "/home/landotech/Desktop/output.drawio"
dc = DrawmateConfig(config_file)
matrix_dims = dc.get_matrix_dimensions()
nodes_left, nodes_right = dc.build_node_dict(matrix_dims.num_connections)

sys.path.append(os.path.abspath("../drawmate_engine"))
import drawmate

def init_graph():
    layout_config = drawmate.LayoutConfig(
        base_x=2000.0,
        base_y=2000.0,
        node_spacing_x_axis=250.0,
        node_spacing_y_axis=20.0,
        port_spacing=60.0
    )
    grid_config = drawmate.GridConfig(
        columns_left=3,
        columns_right=3,
        rows_left=8,
        rows_right=8
    )
    central_node_config = drawmate.CentralNodeConfig(
        width=200.0,
        height=200.0,
        label_height=20.0
    )
    node_config = drawmate.NodeConfig(
        width=120.0,
        height=60.0,
        label_height=20.0,
    )
    port_config = drawmate.PortConfig(
        port_width=60.0,
        port_height=20.0
    )
    graph = drawmate.Graph(layout_config, grid_config, central_node_config, node_config, port_config)
    return graph


def init_matrix(graph):
    matrix_meta = {
        "node-type": "video-matrix",
        "node-orientation": "center",
        "node-label": matrix_dims.label
    }

    matrix_ports_left, matrix_ports_right = dc.get_matrix_connection_labels()

    graph.add_node(matrix_meta, matrix_ports_left, matrix_ports_right)

def init_connection(graph, source_id, target_id, port_index_source, port_index_target):
    graph.add_connection(source_id, target_id, port_index_source, port_index_target)

def init_nodes(graph):
    for k, v in nodes_left.items():

        # col = k.split("-")[1]
        # row = k.split("-")[2]
        node_meta = {}
        if v[0].strip() == "__SPAN__" or v[0].strip() == "":
            node_meta["node-type"] = "__SPAN__"
        else:
            node_meta["node-type"] = "appliance"
        node_meta["node-orientation"] = "left"
        node_meta["node-label"] = v[0]

        if isinstance(v[1], list):
            port_labels_left = v[1]
        else:
            port_labels_left = [v[1]]

        if isinstance(v[2], list):
            port_labels_right = v[2]
        else:
            port_labels_right = [v[2]]

        graph.add_node(node_meta, port_labels_left, port_labels_right)

    for k, v in nodes_right.items():

        # col = k.split("-")[1]
        # row = k.split("-")[2]
        node_meta = {}
        if v[0].strip() == "__SPAN__" or v[0].strip() == "":
            node_meta["node-type"] = "__SPAN__"
        else:
            # print(col, row)
            node_meta["node-type"] = "appliance"
        node_meta["node-orientation"] = "right"
        node_meta["node-label"] = v[0]

        if isinstance(v[1], list):
            port_labels_left = v[1]
        else:
            port_labels_left = [v[1]]

        if isinstance(v[2], list):
            port_labels_right = v[2]
        else:
            port_labels_right = [v[2]]

        graph.add_node(node_meta, port_labels_left, port_labels_right)

    nodes_export = graph.get_nodes()
    node_ids = graph.get_node_ids()
    side = None
    col = None
    row = None
    for i in node_ids:
        node = nodes_export.get(i)
        if len(i) < 4:
            pass
        else:
            side = i.split("-")[0]
            col = i.split("-")[1]
            row = i.split("-")[2]
            # graph.add_connection(i, "C-0", 0, 0)
            # links = graph.get_links()
            # for link in links:
            #     print(link.source_x)
            #     print(link.has_waypoints)

        attributes = {
            "x": node.x,
            "y": node.y,
            "label": node.label,
            "width": node.width,
            "height": node.height,
            "style": MX_GRAPH_XML_STYLES["rect"]
        }
        label_attributes = {
            "x": node.label.x,
            "y": node.label.y,
            "label": node.label.name,
            "width": node.label.width,
            "height": node.label.height,
            "style": MX_GRAPH_XML_STYLES["text-box-filled"]
        }

        # print(f"Node {i}: {node.label}:")
        # print(f"x = {node.x} y = {node.y}")
        # print()
        print(i)
        drawmate_ren.draw_node(attributes)
        drawmate_ren.draw_node(label_attributes, has_label=True)

        for port in node.ports_left:

            port_attributes = {
                "x": port.x,
                "y": port.y,
                "label": port.name,
                "width": port.width,
                "height": port.height,
                "style": MX_GRAPH_XML_STYLES["text-box"]
            }
            drawmate_ren.draw_node(port_attributes, has_label=True)

        for index, port in enumerate(node.ports_right):

            if side and col and row:
                if side == "L" and col == "0":
                    graph.add_connection(i, "C-0", index, index)
                    print("connection added")

            port_attributes = {
                "x": port.x,
                "y": port.y,
                "label": port.name,
                "width": port.width,
                "height": port.height,
                "style": MX_GRAPH_XML_STYLES["text-box"]
            }
            drawmate_ren.draw_node(port_attributes, has_label=True)

    links = graph.get_links()
    for link in links:
        link_attributes = {
            "source_x": link.source_x,
            "source_y": link.source_y,
            "target_x": link.target_x,
            "target_y": link.target_y,
            "style": MX_GRAPH_XML_STYLES["arrow"],
            "label": ""
        }
        drawmate_ren.draw_connection(link_attributes)


if __name__ == "__main__":
    graph = init_graph()
    init_matrix(graph)
    init_nodes(graph)
    drawmate_ren.create_xml(output_file)