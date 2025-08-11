from drawmate.drawmate_config import DrawmateConfig
from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_port import DrawmatePort
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager


class DrawmateGridLayout:
    def __init__(self, config_file):
        self.config = DrawmateConfig(config_file)
        self.spacing_mgr = DrawmateSpacingManager(self.config.get_matrix_dimensions())
        self.graph_dims = self.config.get_graph_dimensions()
        self.matrix: DrawmateNode = self.init_matrix()
        self.left_nodes, self.right_nodes = self.config.build_node_dict_test(
            self.spacing_mgr.matrix_dimensions.num_connections
        )
        self.column_count_left = 0
        self.column_count_right = 0
        self.row_count_left = 0
        self.row_count_right = 0

    def init_graph(self, enable_debug: bool = False):
        self.emplace_left_nodes()
        self.emplace_right_nodes()
        if enable_debug:
            self.debug_mode()

    def init_matrix(self):
        matrix = DrawmateNode(
            self.spacing_mgr.matrix_dimensions.label,
            width=self.spacing_mgr.matrix_width,
            height=self.spacing_mgr.matrix_height,
            x=self.spacing_mgr.base_x,
            y=self.spacing_mgr.base_y,
        )
        self.add_matrix_ports(matrix)
        return matrix

    def init_node_left(self, node: DrawmateNode, base_y):
        node.height = self.spacing_mgr.get_node_height(len(node.ports_input))
        node.width = self.spacing_mgr.node_width
        node.x = self.spacing_mgr.get_node_x_left(self.column_count_left)
        node.y = base_y

    def init_node_right(self, node: DrawmateNode, base_y):
        node.height = self.spacing_mgr.get_node_height(len(node.ports_input))
        node.width = self.spacing_mgr.node_width
        node.x = self.spacing_mgr.get_node_x_right(self.column_count_right)
        node.y = base_y

    def init_ports_input(self, node: DrawmateNode):
        base_y = node.y
        ports = node.ports_input
        for port in ports:
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = node.x
            port.y = base_y + self.spacing_mgr.label_height
            base_y += self.spacing_mgr.port_spacing_y

    def init_ports_output(self, node: DrawmateNode):
        base_y = node.y
        ports = node.ports_output
        for port in ports:
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = node.x + node.width
            port.y = base_y
            base_y += self.spacing_mgr.port_spacing_y

    def add_matrix_ports(self, matrix: DrawmateNode):
        ports = self.config.get_matrix_connection_labels()
        matrix.add_port_input(ports[0], [0] * len(ports[0]))
        matrix.add_port_output(ports[1], [0] * len(ports[1]))

    def emplace_left_nodes(self):
        base_y = self.spacing_mgr.base_y
        for key, node in self.left_nodes.items():
            self.init_node_left(node, base_y)
            self.init_ports_input(node)
            self.init_ports_output(node)
            self.increment_row_count_left()
            self.reset_left_counters()
            base_y = self.spacing_mgr.get_node_y(base_y, node.height)

    def emplace_right_nodes(self):
        base_y = self.spacing_mgr.base_y
        for key, node in self.right_nodes.items():
            self.init_node_right(node, base_y)
            self.init_ports_input(node)
            self.init_ports_output(node)
            self.increment_row_count_right()
            self.reset_right_counters()
            base_y = self.spacing_mgr.get_node_y(base_y, node.height)

    def reset_left_counters(self):
        if self.row_count_left >= self.spacing_mgr.matrix_dimensions.num_connections:
            self.row_count_left = 0
            self.increment_column_count_left()

    def reset_right_counters(self):
        if self.row_count_right >= self.spacing_mgr.matrix_dimensions.num_connections:
            self.row_count_right = 0
            self.increment_column_count_right()

    def increment_column_count_left(self):
        self.column_count_left += 1

    def increment_row_count_left(self):
        self.row_count_left += 1

    def increment_column_count_right(self):
        self.column_count_right += 1

    def increment_row_count_right(self):
        self.row_count_right += 1

    def debug_mode(self):
        self.pretty_print_node(self.matrix)
        self.iterate_left_nodes()
        self.iterate_right_nodes()

    def iterate_left_nodes(self):
        print()
        print("+++++          LEFT NODES          +++++")
        print()
        for key, node in self.left_nodes.items():
            if node.label == "__SPAN__" or node.label == "":
                pass
            else:
                self.pretty_print_node(node)
                for l_port, r_port in zip(node.ports_input, node.ports_output):
                    self.pretty_print_port(l_port)
                    self.pretty_print_port(r_port)

    def iterate_right_nodes(self):
        print()
        print("+++++          RIGHT NODES          +++++")
        print()
        for key, node in self.right_nodes.items():
            if node.label == "__SPAN__" or node.label == "":
                pass
            else:
                self.pretty_print_node(node)
                for l_port, r_port in zip(node.ports_input, node.ports_output):
                    self.pretty_print_port(l_port)
                    self.pretty_print_port(r_port)
                print()

    @staticmethod
    def pretty_print_node(node: DrawmateNode):
        print(f"Node           : {node.label}")
        print(f"#Ports (ea)    : {len(node.ports_input)}")
        print(f"Height         : {node.height}")
        print(f"Width          : {node.width}")
        print(f"X              : {node.x}")
        print(f"Y              : {node.y}")
        print("=========================================")

    @staticmethod
    def pretty_print_port(port: DrawmatePort):
        print(f"\tPort           : {port.label}")
        print(f"\tHeight         : {port.height}")
        print(f"\tWidth          : {port.width}")
        print(f"\tX              : {port.x}")
        print(f"\tY              : {port.y}")
        print("=========================================")
