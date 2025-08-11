from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager


class DrawmatePortConfigurator:
    def __init__(self, spacing_mgr: DrawmateSpacingManager, pad_y=10) -> None:
        self.spacing_mgr = spacing_mgr
        self.pad_y = pad_y

    def configure_ports_input_matrix(self, matrix: DrawmateNode, port_ids: list[str]):
        base_y = matrix.y
        ports = matrix.ports_input
        for idx, port in enumerate(ports):
            port.id = port_ids[idx]
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = matrix.x
            port.y = base_y + self.spacing_mgr.label_height + self.pad_y
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height

    def configure_ports_output_matrix(self, matrix: DrawmateNode, port_ids: list[str]):
        base_y = matrix.y
        ports = matrix.ports_output
        for idx, port in enumerate(ports):
            port.id = port_ids[idx]
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = matrix.x + (matrix.width - port.width)
            port.y = base_y + self.spacing_mgr.label_height + self.pad_y
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height

    def configure_ports_input(self, node: DrawmateNode, port_ids: list[str]):
        base_y = node.y
        ports = node.ports_input
        for idx, port in enumerate(ports):
            port.id = port_ids[idx]
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = node.x
            port.y = base_y + self.spacing_mgr.label_height + self.pad_y
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height

    def configure_ports_output(self, node: DrawmateNode, port_ids: list[str]):
        base_y = node.y
        ports = node.ports_output
        for idx, port in enumerate(ports):
            port.id = port_ids[idx]
            port.height = self.spacing_mgr.port_height
            port.width = self.spacing_mgr.port_width
            port.x = node.x + port.width
            port.y = base_y + self.spacing_mgr.label_height + self.pad_y
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height
