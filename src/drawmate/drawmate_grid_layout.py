from drawmate.drawmate_config import DrawmateConfig
from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_port import DrawmatePort
from drawmate.doc_builder import generate_id
from drawmate.drawmate_matrix_builder import DrawmateMatrixBuilder
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager
from drawmate.drawmate_port_configurator import DrawmatePortConfigurator
from drawmate.drawmate_node_configurator import DrawmateNodeConfigurator
from drawmate.drawmate_linker import DrawmateLinker


class DrawmateGridLayout:
    def __init__(self, config_file):
        self.total_node_count = 0
        self.config = DrawmateConfig(config_file)
        self.spacing_mgr = DrawmateSpacingManager(self.config.get_matrix_dimensions())
        self.matrix_builder = DrawmateMatrixBuilder(self.spacing_mgr)
        self.port_configurator = DrawmatePortConfigurator(self.spacing_mgr)
        self.node_configurator = DrawmateNodeConfigurator()
        self.graph_dims = self.config.get_graph_dimensions()
        self.matrix: DrawmateNode = self.init_matrix()
        self.left_nodes, self.right_nodes = self.config.build_node_dict_test(
            self.spacing_mgr.matrix_dimensions.num_connections
        )
        self.column_count_left = 0
        self.column_count_right = 0
        self.row_count_left = 0
        self.row_count_right = 0

    def get_id(self):
        __id__ = generate_id() + "-" + str(self.total_node_count)
        self.increment_total_node_count()
        return __id__

    def generate_port_ids(self, node: DrawmateNode):
        len_ports = len(node.ports_input)
        port_ids = []
        for i in range(len_ports):
            port_ids.append(self.get_id())
        return port_ids

    def init_graph(self, enable_debug: bool = False):
        self.init_nodes_left()
        self.init_nodes_right()
        if enable_debug:
            self.debug_mode()

    def init_matrix(self):
        matrix = self.matrix_builder.build_matrix(
            self.get_id(),
            self.spacing_mgr.matrix_dimensions.label,
            self.config.get_matrix_connection_labels(),
        )
        self.port_configurator.configure_ports_input(
            matrix, "C-0-0", self.generate_port_ids(matrix),
        )
        self.port_configurator.configure_ports_output(
            matrix, "C-0-0", self.generate_port_ids(matrix), is_matrix=True
        )
        return matrix

    def init_nodes_left(self):
        base_y = self.spacing_mgr.base_y
        for key, node in self.left_nodes.items():
            self.node_configurator.configure_node_left(
                self.get_id(), base_y, self.column_count_left, node, self.spacing_mgr
            )
            self.port_configurator.configure_ports_input(
                node, key, self.generate_port_ids(node)
            )
            self.port_configurator.configure_ports_output(
                node, key, self.generate_port_ids(node)
            )
            self.manage_counters_left()
            base_y = self.spacing_mgr.get_node_y(base_y, self.spacing_mgr.node_height)

    def init_nodes_right(self):
        base_y = self.spacing_mgr.base_y
        for key, node in self.right_nodes.items():
            self.node_configurator.configure_node_right(
                self.get_id(), base_y, self.column_count_right, node, self.spacing_mgr
            )
            self.port_configurator.configure_ports_input(
                node, key, self.generate_port_ids(node)
            )
            self.port_configurator.configure_ports_output(
                node, key, self.generate_port_ids(node)
            )
            self.manage_counters_right()
            base_y = self.spacing_mgr.get_node_y(base_y, self.spacing_mgr.node_height)

    def init_links(self):
        linker = DrawmateLinker(self.port_configurator.output_ports_dict, self.port_configurator.input_ports_dict)
        linker.link()
        return linker.output_ports

    def manage_counters_left(self):
        self.increment_row_count_left()
        self.reset_left_counters()

    def manage_counters_right(self):
        self.increment_row_count_right()
        self.reset_right_counters()

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

    def increment_total_node_count(self):
        self.total_node_count += 1

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
