from drawmate.drawmate_port import DrawmatePort


class DrawmateNode:
    def __init__(
        self,
        label: str,
        width: float = 0.0,
        height: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
    ) -> None:
        self.id: str
        self.label = label
        self.ports_input: list[DrawmatePort] = []
        self.ports_output: list[DrawmatePort] = []
        self.width: float = width
        self.height: float = height
        self.x: float = x
        self.y: float = y

    def add_port_input(
        self, port_labels: str | list[str], connection_indexes: list[int] | list[str]
    ):
        if isinstance(port_labels, list):
            for idx, port in enumerate(port_labels):
                if isinstance(connection_indexes[0], str):
                    self.ports_input.append(DrawmatePort(port, idx))
                else:
                    self.ports_input.append(DrawmatePort(port, connection_indexes[idx]))
        else:
            if isinstance(connection_indexes[0], str):
                self.ports_input.append(DrawmatePort(port_labels, 0))

    def add_port_output(
        self, port_labels: str | list[str], connection_indexes: list[int] | list[str]
    ):
        if isinstance(port_labels, list):
            for idx, port in enumerate(port_labels):
                if isinstance(connection_indexes[0], str):
                    self.ports_output.append(DrawmatePort(port, idx))
                else:
                    self.ports_output.append(
                        DrawmatePort(port, connection_indexes[idx])
                    )
        else:
            self.ports_output.append(DrawmatePort(port_labels, 0))
