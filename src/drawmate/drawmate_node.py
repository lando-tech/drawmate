from .drawmate_port import DrawmatePort


class DrawmateNode:
    def __init__(self, label: str, ports_input: list[DrawmatePort], ports_output: list[DrawmatePort]) -> None:
        self.id: str
        self.label = label
        self.ports_input = ports_input
        self.ports_output = ports_output
        self.width: float = 0
        self.height: float = 0
        self.x: float = 0
        self.y: float = 0
