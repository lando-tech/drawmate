from drawmate.drawmate_port import DrawmatePort
from drawmate.drawmate_link import DrawmateLink
from drawmate.id_utils import get_adjacent_port_key

class DrawmateLinker:
    def __init__(self, output_ports_dict: dict[str, DrawmatePort], input_ports_dict: dict[str, DrawmatePort]) -> None:
        self.output_ports = output_ports_dict
        self.input_ports = input_ports_dict

    def link(self):
        for key, value in self.output_ports.items():
            adjacent_key = get_adjacent_port_key(key)
            source_id = value.id
            try:
                target_port = self.input_ports[adjacent_key]
                value.link = DrawmateLink(source_id, target_port.id)
                print(f"Output Key: {key} | Input Key {adjacent_key}")
                print("Link made")
                print()
            except KeyError:
                pass
                # raise RuntimeError("Unable to find adjacent key")
                # print(f"Unable to locate key: {adjacent_key}")
