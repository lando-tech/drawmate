from constants.matrix_constants import MatrixLabel
from constants.node_constants import NodeAttributes
from builder.matrix_builder import MatrixBuilder
from builder.node_builder import NodeBuilder
from drawmate_engine.drawmate_config import DrawmateConfig
from drawmate_engine.drawmate_master import DrawmateMaster
from graph_objects.node import NodeMetaData

drawmate_config = DrawmateConfig("/home/landotech/github/drawmate/test/mc_test_1.json")
matrix_dims = drawmate_config.get_matrix_dimensions()
left_nodes, right_nodes = drawmate_config.build_node_dict(matrix_dims.num_connections)

matrix_builder = MatrixBuilder(matrix_dims)
node_builder = NodeBuilder()

drawmate = DrawmateMaster(matrix_builder, node_builder)

def create_matrix():
    drawmate.draw_matrix()
    drawmate.draw_matrix_label()
    drawmate.draw_matrix_ports(120, drawmate_config.get_matrix_connection_labels())

def create_node_meta_left(left_nodes: dict) -> list[NodeMetaData]:
    node_meta_left = []

    for key, node in left_nodes.items():
        col, row = key.split("-")
        node_attributes_left = {
            "label": node[0],
            "input-labels": node[1],
            "output-labels": node[2],
            "connection-indexes-left": node[3],
            "connection-indexes-right": node[4]
        }
        node_meta = drawmate.create_node_metadata(node_attributes_left, int(col), int(row), "left")
        print(node_meta.__COLUMN_INDEX__, node_meta.__ROW_INDEX__)
        node_meta_left.append(node_meta)

    return node_meta_left

def create_node_meta_right(right_nodes: dict) -> list[NodeMetaData]:
    node_meta_right = []
    for key, node in right_nodes.items():
        col, row = key.split("-")
        node_attributes_right = {
            "label": node[0],
            "input-labels": node[1],
            "output-labels": node[2],
            "connection-indexes-left": node[3],
            "connection-indexes-right": node[4]
        }
        node_meta = drawmate.create_node_metadata(node_attributes_right, int(col), int(row), "right")
        print(node_meta.__COLUMN_INDEX__, node_meta.__ROW_INDEX__)
        node_meta_right.append(node_meta)

    return node_meta_right

def get_node_attributes() -> dict[str, int]:
    return {
        "x": matrix_dims.x,
        "y": matrix_dims.y,
        "width": NodeAttributes.width,
        "height": NodeAttributes.height,
    }

def calculate_node_x_offset(matrix_x: int, matrix_width: int, node_col: int, side: str):

    if node_col == 0 and side == "right":
        return (matrix_x + matrix_width) + NodeAttributes.x_spacing
    if node_col == 0 and side == "left":
        return matrix_x + NodeAttributes.x_spacing

    return matrix_x + (NodeAttributes.x_spacing * node_col) + NodeAttributes.width

def calculate_node_y_offset(matrix_y: int, node_row: int):
    return (matrix_y + MatrixLabel.height) + (node_row * NodeAttributes.y_spacing)


# x = node_attributes["x"]
# y = node_attributes["y"]
# label = node_attributes["label"]
# input_label = node_attributes["input_label"]
# output_label = node_attributes["output_label"]
# width = node_attributes["width"]
# height = node_attributes["height"]

def create_nodes(attributes: dict, node_meta_array: list[NodeMetaData]):
    attributes["label"] = ""
    attributes["input_label"] = ""
    attributes["output_label"] = ""

    for node_meta in node_meta_array:
        if node_meta.__SPANNING_NODE__:
            continue
        attributes["x"] = calculate_node_x_offset(matrix_dims.x, matrix_dims.width, node_meta.__COLUMN_INDEX__, node_meta.__SIDE__)
        attributes["y"] = calculate_node_y_offset(matrix_dims.y, node_meta.__ROW_INDEX__)
        print(
            f"Node {node_meta.__ID__} at ({attributes['x']}, {attributes['y']})"
        )
        node = drawmate.create_node(attributes, node_meta)
        drawmate.draw_node(node)

create_matrix()
node_meta_left = create_node_meta_left(left_nodes)
node_meta_right = create_node_meta_right(right_nodes)
create_nodes(get_node_attributes(), node_meta_left)
create_nodes(get_node_attributes(), node_meta_right)

drawmate.create_xml("/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml")