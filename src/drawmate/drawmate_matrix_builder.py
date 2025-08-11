from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_port_configurator import DrawmatePortConfigurator
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager


class DrawmateMatrixBuilder:
    def __init__(self, spacing_mgr: DrawmateSpacingManager) -> None:
        self.spacing_mgr = spacing_mgr
        self.port_builder = DrawmatePortConfigurator(spacing_mgr)

    def build_matrix(
        self,
        __id__,
        label,
        conn_labels: tuple[list[str], list[str]],
    ):
        matrix = DrawmateNode(
            label,
            self.spacing_mgr.matrix_width,
            self.spacing_mgr.matrix_height,
            self.spacing_mgr.base_x,
            self.spacing_mgr.base_y,
        )
        matrix.id = __id__
        self.build_matrix_ports(matrix, conn_labels)
        return matrix

    @staticmethod
    def build_matrix_ports(
        matrix: DrawmateNode, conn_labels: tuple[list[str], list[str]]
    ):
        ports = conn_labels
        matrix.add_port_input(ports[0], [0] * len(ports[0]))
        matrix.add_port_output(ports[1], [0] * len(ports[1]))
