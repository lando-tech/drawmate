import sys
import os

from drawmate_renderer.drawmate_config import DrawmateConfig

config_file = "/home/landotech/easyrok/drawmate/test_templates/mc_test_1.json"
dc = DrawmateConfig(config_file)
matrix_dims = dc.get_matrix_dimensions()
nodes_left, nodes_right = dc.build_node_dict(matrix_dims.num_connections)

sys.path.append(os.path.abspath("/drawmate_lib/build"))
import drawmate

def set_layout_config(layout_config):
    # Set Base x/y
    layout_config.base_x = float(matrix_dims.x)
    layout_config.base_y = float(matrix_dims.y)

    # Set Node Layout
    layout_config.node_width = 160.0
    layout_config.node_height = 60.0
    layout_config.node_label_height = 20.0
    layout_config.node_spacing_x_axis = 400.0
    layout_config.node_spacing_y_axis = 20.0

    # Set Port Layout
    layout_config.port_width = 30.0
    layout_config.port_height = 20.0
    layout_config.port_spacing = 10.0

def set_grid_config(grid_config):
    grid_config.num_columns_left = dc.num_levels
    grid_config.num_columns_right = dc.num_levels
    grid_config.num_rows_left = matrix_dims.num_connections
    grid_config.num_rows_right = matrix_dims.num_connections

lc = drawmate.LayoutConfig()
gc = drawmate.GridConfig()
set_layout_config(lc)
set_grid_config(gc)

graph = drawmate.Graph(lc, gc)

for k, v in nodes_left.items():

    if v[0].strip() == "__SPAN__" or v[0].strip() == "":
        continue

    node_meta = {
        "node-type": "appliance",
        "node-label": v[0],
        "node-orientation": "left"
    }
    if isinstance(v[1], list):
        port_labels_left = v[1]
    else:
        port_labels_left = list(v[1])

    if isinstance(v[2], list):
        port_labels_right = v[2]
    else:
        port_labels_right = list(v[2])

    graph.add_node(node_meta, port_labels_left, port_labels_right)

for k, v in nodes_right.items():

    if v[0].strip() == "__SPAN__" or v[0].strip() == "":
        continue

    node_meta = {
        "node-type": "appliance",
        "node-label": v[0],
        "node-orientation": "right"
    }
    if isinstance(v[1], list):
        port_labels_left = v[1]
    else:
        port_labels_left = list(v[1])

    if isinstance(v[2], list):
        port_labels_right = v[2]
    else:
        port_labels_right = list(v[2])

    graph.add_node(node_meta, port_labels_left, port_labels_right)

node_ids = graph.get_node_ids()
print(node_ids)
