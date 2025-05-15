from constants.matrix_constants import MatrixLabel, MatrixDimensions, MatrixPorts
from constants.node_constants import NodeAttributes, NodePorts, NodeLabels
from builder.matrix_builder import MatrixBuilder
from drawmate_engine.drawmate_config import DrawmateConfig
from drawmate_engine.drawmate_master import DrawmateMaster
from graph_objects.arrow import Arrow
from graph_objects.node import Node
from graph_objects.matrix import Matrix
from graph_objects.text_box import TextBox
from graph_objects.port import Port
from layout_managers.connection_manager import ConnectionManager
from layout_managers.container_manager import ContainerManager


class VideoCodec:
    def __init__(
        self,
        drawmate: DrawmateMaster,
        matrix_dimensions: MatrixDimensions,
        num_levels: int,
    ):
        self.drawmate = drawmate
        self.matrix_builder = MatrixBuilder(matrix_dimensions)
        self.matrix: Matrix = self.matrix_builder.init_matrix()
        self.num_levels: int = num_levels

    def render_connections(self, arrow_dict: dict[str, Arrow]):
        for key, arrow in arrow_dict.items():
            self.drawmate.draw_connection(arrow)

    def render_nodes(self, node_dict: dict[str, Node], node_labels: dict[str, TextBox]):

        # print("=============================")
        for key, node in node_dict.items():
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
                self.drawmate.draw_node_label(node_labels.get(node.meta.__ID__))

    def render_node_labels(self, node_label_dict: dict[str, TextBox]):
        for key, label in node_label_dict.items():
            self.drawmate.draw_node_label(label)

    def render_node_ports_single(self, node_port_dict: dict[str, Port]):
        for key, port in node_port_dict.items():
            self.drawmate.draw_node_label(port)

    def render_node_ports_multi(self, node_port_dict: dict[str, list[Port]]):
        for key, ports in node_port_dict.items():
            for port in ports:
                self.drawmate.draw_node_label(port)

    def render_matrix(self, connection_labels: tuple[list, list]):
        self.drawmate.draw_matrix(self.matrix)
        matrix_label = self.matrix_builder.init_matrix_label()
        matrix_ports = self.matrix_builder.init_matrix_ports(
            spacing=MatrixPorts.port_spacing, connection_labels=connection_labels
        )
        self.drawmate.draw_matrix_label(matrix_label)
        self.drawmate.draw_matrix_ports(matrix_ports)

    def compute_node_data_left(
        self, node_dict_left: dict[str, Node], node_labels_dict: dict[str, TextBox]
    ):
        self.create_node_pointers_left(node_dict_left)
        self.calculate_node_position_left(node_dict_left, node_labels_dict)

    def compute_node_ports_left(self, port_dict: dict[str, Port]):
        for key, port in port_dict.items():
            x, y = int(port.parent.attributes["x"]), int(port.parent.attributes["y"])

    def create_node_pointers_left(
        self, node_dict_left: dict[str, Node]
    ):
        for key, node in node_dict_left.items():
            col, row = key.split("-")
            if node.meta.__COLUMN_INDEX__ == 0:
                node.right_ptr = self.matrix
                node.left_ptr = node_dict_left.get(f"{int(col) + 1}-{row}")
            elif node.meta.__COLUMN_INDEX__ == self.num_levels:
                node.right_ptr = node_dict_left.get(f"{int(col) - 1}-{row}")
                node.left_ptr = None

            else:
                node.right_ptr = node_dict_left.get(f"{int(col) - 1}-{row}")
                node.left_ptr = node_dict_left.get(f"{int(col) + 1}-{row}")

    def create_node_pointers_right(self, node_dict_right: dict[str, Node]):

        for key, node in node_dict_right.items():
            col, row = key.split("-")
            if node.meta.__COLUMN_INDEX__ == 0:
                node.left_ptr = self.matrix
                node.right_ptr = node_dict_right.get(f"{int(col) + 1}-{row}")
            elif node.meta.__COLUMN_INDEX__ == self.num_levels:
                node.left_ptr = node_dict_right.get(f"{int(col) - 1}-{row}")
                node.right_ptr = None
            else:
                node.left_ptr = node_dict_right.get(f"{int(col) - 1}-{row}")
                node.right_ptr = node_dict_right.get(f"{int(col) + 1}-{row}")

    def calculate_node_position_left(
        self, node_dict_left: dict[str, Node], node_labels_dict: dict[str, TextBox]
    ):

        # base_y = self.matrix.y
        for key, node in node_dict_left.items():
            node_label = node_labels_dict.get(node.meta.__ID__)
            col, row = key.split("-")
            # node.attributes["x"], node.attributes["y"] = x, y
            previous_node = node_dict_left.get(f"{col}-{int(row) - 1}")

            if int(row) == 0:
                base_y = self.matrix.y
                y = self.calculate_node_y(base_y, 0, 0)
                node.attributes["y"] = y
                height = int(node.attributes["height"])
            elif node.meta.__SPANNING_NODE__:
                base_y = self.matrix.y
                y = self.calculate_node_y(base_y, 0, 0)
                node.attributes["y"] = y
            else:
                base_y = previous_node.attributes["y"]
                y = self.calculate_node_y(base_y, height)
                node.attributes["y"] = y
                height = int(node.attributes.get("height"))

            x = self.calculate_node_x_left(node.right_ptr.x)
            node.attributes["x"] = x

            node_label.attributes["x"] = x
            node_label.attributes["y"] = y
            # print(f"Node {col}-{row} -- y = {node.y} | x = {node.x}")
            # base_y += NodeAttributes.y_spacing + int(node.attributes["height"])

    def calculate_node_position_right(self, node_dict_right: dict[str, Node]):
        base_y_right = self.matrix.y
        for key, node in node_dict_right.items():
            col, row = key.split("-")
            # print(f"Node {node.meta.__COLUMN_INDEX__} {node.meta.__ROW_INDEX__} Left pointer: {node.left_ptr}")
            x = self.calculate_node_x_right(int(col))
            # y = self.calculate_node_y(int(row))
            node.attributes["x"], node.attributes["y"] = x, base_y_right
            node.x, node.y = x, base_y_right
            base_y_right += NodeAttributes.y_spacing + int(node.attributes["height"])
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
        base_y: int,
        node_height: int,
        node_spacing: int = NodeAttributes.y_spacing,
    ):
        return base_y + node_height + node_spacing

    def calculate_port_y(self):
        pass

    def calculate_port_x(self):
        pass


if __name__ == "__main__":

    # Parse inputs
    drawmate_config = DrawmateConfig(
        "/home/landotech/easyrok/drawmate/test_templates/xtp_crosspoint_6400.json"
    )
    matrix_dims = drawmate_config.get_matrix_dimensions()
    left_nodes, right_nodes = drawmate_config.build_node_dict(
        matrix_dims.num_connections
    )

    # Master Renderer to be used by layout managers
    drawmate_master = DrawmateMaster()

    # Builds containers of graph objects
    container_mgr = ContainerManager()

    """
    Each container is a dataclass with dictionaries of Nodes, NodeMetadata, and Node Labels.
    All dimensions (width, height) are set to defaults defined in node_constants.py and positions 
    (x, y) are set to 0. 
    Computations on placement and resizing should be made elsewhere to avoid data 
    mutation in the wrong place.
    """
    node_containers_left = container_mgr.build_node_container(left_nodes, "left")
    node_containers_right = container_mgr.build_node_container(right_nodes, "right")

    video = VideoCodec(drawmate_master, matrix_dims, drawmate_config.num_levels)
    video.drawmate.set_graph_values(dx=4000, dy=4000, page_width=4000, page_height=4000)
    video.compute_node_data_left(node_containers_left.nodes, node_containers_left.node_labels)
    video.render_matrix(drawmate_config.get_matrix_connection_labels())
    video.render_nodes(node_containers_left.nodes, node_containers_left.node_labels)

    node_ports_left_single = container_mgr.build_port_container_single(
        node_containers_left.nodes
    )
    node_ports_right_single = container_mgr.build_port_container_single(
        node_containers_right.nodes
    )

    node_ports_left_multi = container_mgr.build_port_container_multi(
        node_containers_left.nodes
    )
    node_ports_right_multi = container_mgr.build_port_container_multi(
        node_containers_right.nodes
    )
    #
    # video.render_nodes(node_containers_left.nodes, node_ports_left_single.node_labels)
    # video.render_nodes(node_containers_right.nodes, node_ports_right_single.node_labels)
    #
    video.render_node_ports_single(node_ports_left_single.input_ports)
    video.render_node_ports_single(node_ports_left_single.output_ports)
    video.render_node_ports_multi(node_ports_left_multi.input_ports)
    video.render_node_ports_multi(node_ports_left_multi.output_ports)

    # video.render_node_ports_single(node_ports_right_single.input_ports)
    # video.render_node_ports_single(node_ports_right_single.output_ports)
    # video.render_node_ports_multi(node_ports_right_multi.input_ports)
    # video.render_node_ports_multi(node_ports_right_multi.output_ports)
    #
    # connection_mgr_left = ConnectionManager(
    #     node_containers_left.nodes,
    #     (node_ports_left_single.input_ports, node_ports_left_single.output_ports),
    #     (node_ports_left_multi.input_ports, node_ports_left_multi.output_ports),
    # )
    # connection_mgr_left.create_connections_dict_left_single()
    # connection_mgr_left.create_connections_dict_left_multi()
    # video.render_connections(connection_mgr_left.connection_dict_single)
    # video.render_connections(connection_mgr_left.connection_dict_multi)
    #
    # connection_mgr_right = ConnectionManager(
    #     node_containers_right.nodes,
    #     (node_ports_right_single.input_ports, node_ports_right_single.output_ports),
    #     (node_ports_right_multi.input_ports, node_ports_right_multi.output_ports),
    # )
    # connection_mgr_right.create_connections_dict_right_single(matrix_dims.width)
    # connection_mgr_right.create_connections_dict_right_multi(matrix_dims.width)
    # video.render_connections(connection_mgr_right.connection_dict_single)
    # video.render_connections(connection_mgr_right.connection_dict_multi)

    output_file: str = "/home/landotech/Desktop/output.drawio"
    video.drawmate.create_xml(output_file)
    print(f"Template saved @ {output_file}")
