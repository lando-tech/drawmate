from constants.node_constants import NodeAttributes
from builder.matrix_builder import MatrixBuilder
from builder.node_builder import NodeBuilder
from drawmate_engine.drawmate_config import DrawmateConfig
from drawmate_engine.drawmate_master import DrawmateMaster

drawmate_config = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
matrix_dims = drawmate_config.get_matrix_dimensions()
left_nodes, right_nodes = drawmate_config.build_node_dict(matrix_dims.num_connections)

matrix_builder = MatrixBuilder(matrix_dims)
node_builder = NodeBuilder()

drawmate = DrawmateMaster(matrix_builder, node_builder)

node_meta_left = []
node_meta_right = []

for key, node in left_nodes.items():
    col, row = key.split("-")
    node_attributes = {
        "label": node[0],
        "input-labels": node[1],
        "output-labels": node[2],
        "connection-indexes-left": node[3],
        "connection-indexes-right": node[4]
    }
    node_meta = drawmate.create_node_metadata(node_attributes, int(col), int(row), "left")
    node_meta_left.append(node_meta)

for key, node in right_nodes.items():
    col, row = key.split("-")
    node_attributes = {
        "label": node[0],
        "input-labels": node[1],
        "output-labels": node[2],
        "connection-indexes-left": node[3],
        "connection-indexes-right": node[4]
    }
    node_meta = drawmate.create_node_metadata(node_attributes, int(col), int(row), "right")
    node_meta_right.append(node_meta)


# TODO begin calculations for node placement based on the matrix and x/y spacing
start_x = matrix_dims.x + NodeAttributes.x_spacing
start_y = matrix_dims.y
for node_meta in node_meta_left:
    node_obj = drawmate.create_node(node_meta.attributes, node_meta)
    drawmate.draw_node(node_obj)
    drawmate.draw_node_label(node_obj)
    drawmate.draw_node_ports_input(node_obj.x, node_obj.y, node_obj.attributes["height"], node_obj.input_label)

for node_meta in node_meta_right:
    node_obj = drawmate.create_node(node_meta.attributes, node_meta)
    drawmate.draw_node(node_obj)
    drawmate.draw_node_label(node_obj)
    drawmate.draw_node_ports_output(node_obj.x, node_obj.y, node_obj.attributes["width"], node_obj.attributes["height"], node_obj.output_label)

# TODO begin implementing connection logic and connecting node pointers

drawmate.draw_matrix()
drawmate.draw_matrix_label()
drawmate.draw_matrix_ports(120, drawmate_config.get_matrix_connection_labels())

# drawmate.create_xml("/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml")