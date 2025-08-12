from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager
from drawmate.drawmate_port import DrawmatePort
from drawmate.id_utils import get_key_row, get_key_column, get_key_orientation, get_port_key_orientation, get_port_key_row

class DrawmatePortConfigurator:
    def __init__(self, spacing_mgr: DrawmateSpacingManager, pad_y=10) -> None:
        self.spacing_mgr = spacing_mgr
        self.pad_y = pad_y
        self.input_ports_dict: dict[str, DrawmatePort] = {}
        self.output_ports_dict: dict[str, DrawmatePort] = {}

    def configure_ports_input(self, node: DrawmateNode, node_key, port_ids: list[str], is_matrix: bool = False):
        base_y = node.y
        ports = node.ports_input
        port_row = get_key_row(node_key)
        for idx, port in enumerate(ports):
            self.configure_port_dimensions(port, port_ids[idx])
            self.configure_port_x_y(port, base_y, node.x, node.width)
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height
            port_key = self.get_port_key('L', port_row, node_key)
            # print(port_key)
            if self.input_ports_dict.__contains__(port_key):
                pass
            else:
                self.input_ports_dict[port_key] = port
            port_row += 1

    def configure_ports_output(self, node: DrawmateNode, node_key, port_ids: list[str], is_matrix: bool = False):
        base_y = node.y
        ports = node.ports_output
        port_row = get_key_row(node_key)
        for idx, port in enumerate(ports):
            self.configure_port_dimensions(port, port_ids[idx])
            self.configure_port_x_y(port, base_y, node.x, node.width, is_output=True, is_matrix=is_matrix)
            base_y += self.spacing_mgr.port_spacing_y + self.spacing_mgr.label_height
            port_key = self.get_port_key('R', port_row, node_key)
            # print(port_key)
            if self.output_ports_dict.__contains__(port_key):
                pass
            else:
                self.output_ports_dict[port_key] = port
            port_row += 1

    def configure_port_dimensions(self, port: DrawmatePort, port_id):
        port.id = port_id
        port.height = self.spacing_mgr.port_height
        port.width = self.spacing_mgr.port_width

    def configure_port_x_y(self, port: DrawmatePort, base_y, node_x, node_width, is_output: bool = False, is_matrix: bool = False):
        if is_output and is_matrix:
            port.x = node_x + (node_width - port.width)
        elif is_output:
            port.x = node_x + port.width
        else:
            port.x = node_x
        port.y = base_y + self.spacing_mgr.label_height + self.pad_y


    def get_port_key(self, port_orientation, port_row, node_key):
        column = get_key_column(node_key)
        # row = get_key_row(node_key)
        orientation = get_key_orientation(node_key)
        return f"{orientation}-{column}-{port_row}-{port_orientation}-{port_row}"
