from .drawmate_node import DrawmateNode
from .drawmate_link import DrawmateLink

class DrawmateGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, DrawmateNode] = {}
        self.ports: dict[str, DrawmateNode] = {}
        self.links: dict[str, DrawmateLink] = {}

    def add_node(self, d_node: DrawmateNode, node_id: str):
        self.nodes[node_id] = d_node

    def add_port(self, d_port: DrawmateNode, port_id: str):
        self.ports[port_id] = d_port

    def add_link(self, d_link: DrawmateLink, link_id: str):
        self.links[link_id] = d_link

    def clear_nodes(self):
        self.nodes.clear()

    def clear_ports(self):
        self.ports.clear()

    def clear_links(self):
        self.links.clear()
