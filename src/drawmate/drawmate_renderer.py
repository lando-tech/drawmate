from drawmate_config import DrawmateConfig
from drawmate_node import DrawmateNode


class DrawmateRenderer:
    def __init__(self, config_file):
        self.config = DrawmateConfig(config_file)
        self.matrix_dims = self.config.get_matrix_dimensions()
        self.matrix: DrawmateNode = self.init_matrix()
        self.left_nodes, self.right_nodes = self.config.build_node_dict_test(self.matrix_dims.num_connections)

    def init_matrix(self):
        return DrawmateNode(
            self.matrix_dims.label,
            width=self.matrix_dims.width,
            height=self.matrix_dims.height
        )

if __name__ == "__main__":
    render = DrawmateRenderer("/home/landotech/Projects/drawmate/test_templates/mc_test_1.json")
    for k, v in render.left_nodes.items():
        print(k, v.label, v.ports_input[0].label, v.ports_input[0].connection_index, v.ports_output[0].label)

    for k, v in render.right_nodes.items():
        print(k, v.label, v.ports_input[0].label, v.ports_input[0].connection_index, v.ports_output[0].label)
