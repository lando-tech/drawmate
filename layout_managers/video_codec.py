from constants.matrix_constants import MatrixPorts, MatrixLabel
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

        # print("\nLeft Side:")
        # print("=============================")
        for key, node in self.node_dict_left.items():
            if node.meta.__SPANNING_NODE__:
                continue
            else:
                # print(
                #     f"Node ID ({node.meta.__ID__})\ncolumn {node.meta.__COLUMN_INDEX__} row {node.meta.__ROW_INDEX__}"
                # )
                # print(f"x = {node.x} | y = {node.y}")
                # print(f"matrix x = {self.matrix.x}")
                # print("=============================")
                self.drawmate.draw_node(node)
                self.drawmate.draw_node_label(node)

        # print("\nRight Side:")
        # print("=============================")
        for key, node in self.node_dict_right.items():
            if node.meta.__SPANNING_NODE__:
                continue
            else:
                # print(
                #     f"Node ID ({node.meta.__ID__})\ncolumn {node.meta.__COLUMN_INDEX__} row {node.meta.__ROW_INDEX__}"
                # )
                # print(f"x = {node.x} | y = {node.y}")
                # print(f"matrix x = {self.matrix.x}")
                # print("=============================")
                self.drawmate.draw_node(node)
                self.drawmate.draw_node_label(node)

    def render_node_input_ports(self):
        for key, node in self.node_dict_left.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            if input_port_array:
                for port in input_port_array:
                    self.drawmate.draw_node_ports_input(x, base_y, height, port)
                    base_y -= MatrixPorts.port_spacing
            if node.input_label:
                self.drawmate.draw_node_ports_input(x, base_y, height, node.input_label)

        for key, node in self.node_dict_right.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            if input_port_array:
                for port in input_port_array:
                    self.drawmate.draw_node_ports_input(x, base_y, height, port)
                    base_y -= MatrixPorts.port_spacing
            if node.input_label:
                self.drawmate.draw_node_ports_input(x, base_y, height, node.input_label)

    def render_node_output_ports(self):
        for key, node in self.node_dict_left.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            width = int(node.attributes["width"])
            if input_port_array:
                for port in input_port_array:
                    self.drawmate.draw_node_ports_output(x, base_y, width, height, port)
                    base_y -= MatrixPorts.port_spacing
            if node.input_label:
                self.drawmate.draw_node_ports_output(x, base_y, width, height, node.input_label)

        for key, node in self.node_dict_right.items():
            input_port_array = node.meta.__INPUT_LABEL_ARRAY__
            x = node.x
            base_y = node.y
            height = int(node.attributes["height"])
            if input_port_array:
                for port in input_port_array:
                    self.drawmate.draw_node_ports_input(x, base_y, height, port)
                    base_y -= MatrixPorts.port_spacing
            if node.input_label:
                self.drawmate.draw_node_ports_input(x, base_y, height, node.input_label)

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

    def create_nodes(self):
        self.initialize_node_arrays()
        self.create_node_pointers()
        self.calculate_node_position()

    def initialize_node_arrays(self, node_width: int = None, node_height: int = None):
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
                node.input_label = node_meta.__INPUT_LABEL__
                node.output_label = node_meta.__OUTPUT_LABEL__
                self.node_dict_left[
                    f"{node_meta.__COLUMN_INDEX__}-{node_meta.__ROW_INDEX__}"
                ] = node
        if self.node_meta_array_right:
            for node_meta in self.node_meta_array_right:
                node = self.drawmate.create_node(node_attributes, node_meta)
                node.input_label = node_meta.__INPUT_LABEL__
                node.output_label = node_meta.__OUTPUT_LABEL__
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

    def calculate_node_position(self):
        if not self.node_dict_left and not self.node_dict_right:
            print("Please initialize nodes first!")
            return

        if self.node_dict_left:
            for key, node in self.node_dict_left.items():
                col, row = key.split("-")
                x = self.calculate_node_x_left(node.right_ptr.x)
                y = self.calculate_node_y(int(row))
                node.attributes["x"], node.attributes["y"] = x, y
                node.x, node.y = x, y
                # print(f"Node {col}-{row} -- y = {node.y} | x = {node.x}")

        if self.node_dict_right:
            for key, node in self.node_dict_right.items():
                col, row = key.split("-")
                # print(f"Node {node.meta.__COLUMN_INDEX__} {node.meta.__ROW_INDEX__} Left pointer: {node.left_ptr}")
                x = self.calculate_node_x_right(node.left_ptr.x, int(col))
                y = self.calculate_node_y(int(row))
                node.attributes["x"], node.attributes["y"] = x, y
                node.x, node.y = x, y
                # print(f"Node {col}-{row} -- y = {node.y} | x = {node.x}")

    def calculate_node_x_left(
        self,
        pointer_x: int,
        node_spacing: int = NodeAttributes.x_spacing,
    ) -> int:
        return pointer_x - node_spacing

    def calculate_node_x_right(
        self,
        node_column: int,
        node_spacing: int = NodeAttributes.x_spacing,
        node_width: int = NodeAttributes.width,
    ):
        base = self.matrix.x + int(self.matrix.attributes["width"])
        offset = node_spacing - node_width
        return base + offset + (node_column * node_spacing)

    def calculate_node_y(
        self,
        node_row: int,
        node_spacing: int = NodeAttributes.y_spacing,
    ):
        base = self.matrix.y + (MatrixLabel.height // 2)
        return base + (node_row * node_spacing)


drawmate_config = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_3.json")
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
video.render_nodes()
video.render_node_input_ports()
video.render_node_output_ports()
video.render_matrix(drawmate_config.get_matrix_connection_labels())
video.drawmate.create_xml("/home/landotech/Desktop/output.drawio")
