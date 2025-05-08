from constants.matrix_constants import MatrixPorts
from constants.node_constants import NodeAttributes
from builder.matrix_builder import MatrixBuilder
from builder.node_builder import NodeBuilder
from drawmate_engine.drawmate_config import DrawmateConfig
from drawmate_engine.drawmate_master import DrawmateMaster
from graph_objects.node import NodeMetaData, Node
from graph_objects.matrix import Matrix


class VideoCodec:
    def __init__(self, drawmate: DrawmateMaster, num_levels: int):
        self.drawmate = drawmate
        self.matrix: Matrix = self.drawmate.create_matrix()
        self.num_levels: int = num_levels
        self.node_meta_array_left: list[NodeMetaData] = []
        self.node_meta_array_right: list[NodeMetaData] = []
        self.node_dict_left: dict[str, Node] = {}
        self.node_dict_right: dict[str, Node] = {}

    def render_nodes(self):
        for key, node in self.node_dict_left.items():
            if node.meta.__SPANNING_NODE__:
                continue
            else:
                print(f"x = {node.x} | y = {node.y}")
                self.drawmate.draw_node(node)

        for key, node in self.node_dict_right.items():
            if node.meta.__SPANNING_NODE__:
                continue
            else:
                print(f"x = {node.x} | {node.y}")
                self.drawmate.draw_node(node)

    def render_matrix(
        self,
        port_labels: tuple[list[str], list[str]],
        port_spacing: int = MatrixPorts.port_spacing,
    ):
        self.drawmate.draw_matrix(self.matrix)
        self.drawmate.draw_matrix_label()
        self.drawmate.draw_matrix_ports(port_spacing, port_labels)

    def create_node_meta_array(self, node_data: dict[str, list | str], side: str):
        """
        Creates metadata for nodes on the specified side based on the provided node data.

        This method processes the given `node_data` dictionary to generate a list
        of `NodeMetaData` objects. It processes each node's attributes, including
        labels and connection indexes, and converts the necessary details into `NodeMetaData`
        objects using the `drawmate.create_node_metadata` function.

        Args:
            node_data (dict[str, list | str]): A dictionary containing the node data,
                where keys are string identifiers (formatted as "col-row") and values are lists
                or strings representing respective node attributes.
            side (str): A string representing the side information, typically used
                in node metadata creation.
        """

        for key, node in node_data.items():
            col, row = key.split("-")
            node_attributes_left = {
                "label": node[0],
                "input-labels": node[1],
                "output-labels": node[2],
                "connection-indexes-left": node[3],
                "connection-indexes-right": node[4],
            }
            node_meta = self.drawmate.create_node_metadata(
                node_attributes_left, int(col), int(row), side
            )
            if side == "left":
                self.node_meta_array_left.append(node_meta)
            else:
                self.node_meta_array_right.append(node_meta)

    def create_nodes(self, node_width: int = None, node_height: int = None):
        node_attributes = {
            "x": 0,
            "y": 0,
            "width": node_width if node_width else NodeAttributes.width,
            "height": node_height if node_height else NodeAttributes.height,
            "label": "",
            "input_label": "",
            "output_label": "",
        }

        if not self.node_meta_array_left and not self.node_meta_array_right:
            print("Please create node meta arrays first.")
            return

        if self.node_meta_array_left:
            for node_meta in self.node_meta_array_left:
                node = self.drawmate.create_node(node_attributes, node_meta)
                self.node_dict_left[
                    f"{node_meta.__COLUMN_INDEX__}-{node_meta.__ROW_INDEX__}"
                ] = node
        if self.node_meta_array_right:
            for node_meta in self.node_meta_array_right:
                node = self.drawmate.create_node(node_attributes, node_meta)
                self.node_dict_right[
                    f"{node_meta.__COLUMN_INDEX__}-{node_meta.__ROW_INDEX__}"
                ] = node

    def create_node_pointers(self):
        if not self.node_dict_left and not self.node_meta_array_right:
            print("Please initialize the left and right node dictionaries first")
            return

        if self.node_dict_left:
            for key, node in self.node_dict_left.items():
                col, row = key.split("-")
                if node.meta.__COLUMN_INDEX__ == 0:
                    node.right_ptr = self.matrix
                    node.left_ptr = self.node_dict_left.get(f"{int(col) + 1}-{row}")
                elif node.meta.__COLUMN_INDEX__ == self.num_levels:
                    node.right_ptr = self.node_dict_left.get(f"{int(col) - 1}-{row}")
                    node.left_ptr = None
                else:
                    node.right_ptr = self.node_dict_left.get(f"{int(col) - 1}-{row}")
                    node.left_ptr = self.node_dict_left.get(f"{int(col) + 1}-{row}")

        if self.node_dict_right:
            for key, node in self.node_dict_right.items():
                col, row = key.split("-")
                if node.meta.__COLUMN_INDEX__ == 0:
                    node.left_ptr = self.matrix
                    node.right_ptr = self.node_dict_left.get(f"{int(col) + 1}-{row}")
                elif node.meta.__COLUMN_INDEX__ == self.num_levels:
                    node.left_ptr = self.node_dict_left.get(f"{int(col) - 1}-{row}")
                    node.right_ptr = None
                else:
                    node.left_ptr = self.node_dict_left.get(f"{int(col) - 1}-{row}")
                    node.right_ptr = self.node_dict_left.get(f"{int(col) + 1}-{row}")

    def create_node_connections(self):
        pass

    def calculate_node_position(self):
        if not self.node_dict_left and not self.node_dict_right:
            print("Please initialize nodes first!")
            return

        if self.node_dict_left:
            for key, node in self.node_dict_left.items():
                col, row = key.split("-")
                x = self.calculate_node_x_left(node.right_ptr.x)
                y = self.matrix.y
                node.attributes["x"] = x
                node.attributes["y"] = y
                node.x = x
                node.y = y
                # print(f"Node {col}-{row} -- y = {node.y} | x = {node.x}")

        if self.node_dict_right:
            for key, node in self.node_dict_right.items():
                col, row = key.split("-")
                x = self.calculate_node_x_right(node.left_ptr.x, int(col))
                y = self.matrix.y
                node.attributes["x"] = x
                node.attributes["y"] = y
                node.x = x
                node.y = y
                # print(f"Node {col}-{row} -- y = {node.y} | x = {node.x}")

    def calculate_node_x_left(
        self,
        pointer_x: int,
        node_spacing: int = NodeAttributes.x_spacing,
    ) -> int:
        return pointer_x - node_spacing

    def calculate_node_x_right(
        self,
        pointer_x: int,
        node_column: int,
        node_spacing: int = NodeAttributes.x_spacing,
        node_width: int = NodeAttributes.width
    ):
        if node_column == 0:
            return self.matrix.x + node_spacing + node_width
        else:
            return pointer_x + node_spacing + node_width

    def calculate_node_y(
        self,
        node_row: int,
        node_height: int = NodeAttributes.height,
        node_spacing: int = NodeAttributes.y_spacing,
        matrix_y: int = 0,
    ):
        pass


drawmate_config = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
matrix_dims = drawmate_config.get_matrix_dimensions()
left_nodes, right_nodes = drawmate_config.build_node_dict(matrix_dims.num_connections)
matrix_builder = MatrixBuilder(matrix_dims)
node_builder = NodeBuilder()
drawmate_master = DrawmateMaster(matrix_builder, node_builder)

video = VideoCodec(drawmate_master, drawmate_config.num_levels)
video.drawmate.set_graph_values(dx=4000, dy=4000, page_width=4000, page_height=4000)
video.create_node_meta_array(left_nodes, "left")
video.create_node_meta_array(right_nodes, "right")
video.create_nodes()
video.create_node_pointers()
video.calculate_node_position()
video.render_nodes()
video.render_matrix(drawmate_config.get_matrix_connection_labels())
video.drawmate.create_xml("/home/landotech/Desktop/output.drawio")
