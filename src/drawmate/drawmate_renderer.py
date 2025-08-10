from drawmate_config import DrawmateConfig
from drawmate_node import DrawmateNode
from drawmate_spacing_manager import DrawmateSpacingManager


class DrawmateRenderer:
    def __init__(self, config_file):
        self.config = DrawmateConfig(config_file)
        self.spacing_mgr = DrawmateSpacingManager(self.config.get_matrix_dimensions())
        self.graph_dims = self.config.get_graph_dimensions()
        self.matrix: DrawmateNode = self.init_matrix()
        self.left_nodes, self.right_nodes = self.config.build_node_dict_test(
            self.spacing_mgr.matrix_dimensions.num_connections
        )

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

    def add_matrix_ports(self, matrix: DrawmateNode):
        ports = self.config.get_matrix_connection_labels()
        matrix.add_port_input(ports[0], [0] * len(ports[0]))
        matrix.add_port_output(ports[1], [0] * len(ports[1]))

    def emplace_left_nodes(self):
        i = 0
        base_y = self.spacing_mgr.base_y
        for key, node in self.left_nodes.items():
            node.height = self.spacing_mgr.get_node_height(len(node.ports_input))
            node.x = (
                self.spacing_mgr.base_x
                + (i * node.width)
                + self.spacing_mgr.node_spacing_x
            )
            node.y = base_y + node.height + self.spacing_mgr.node_spacing_y
            base_y = self.spacing_mgr.reset_base_y(node.y)
            i += 1

    def emplace_right_nodes(self):
        pass


if __name__ == "__main__":
    render = DrawmateRenderer(
        "/home/aaron/Projects/Portfolio/drawmate/test_templates/mc_test_1.json"
    )
    render.emplace_left_nodes()
    print(render.matrix.label, render.matrix.ports_input[0].label, render.matrix.x, render.matrix.y)
    for k, v in render.left_nodes.items():
        if v.label == "__SPAN__":
            continue
        print(
            k,
            v.label,
            v.ports_input[0].label,
            v.ports_input[0].connection_index,
            v.ports_output[0].label,
            v.x,
            v.y
        )

    # for k, v in render.right_nodes.items():
    #     print(
    #         k,
    #         v.label,
    #         v.ports_input[0].label,
    #         v.ports_input[0].connection_index,
    #         v.ports_output[0].label,
    #     )
