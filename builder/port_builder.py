from graph_objects.matrix import Matrix
from graph_objects.node import Node
from graph_objects.port import Port


class PortBuilder:
    def __init__(self):
        pass

    def init_port(self, x: int, y: int, width: int, height: int, label: str, parent: Node | Matrix, mx_graph_style: str) -> Port:
        port = Port(
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent,
            label=label,
            style=mx_graph_style,
        )
        return port

    def init_port_cluster(self):
        pass
