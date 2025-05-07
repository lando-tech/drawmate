from dataclasses import dataclass


@dataclass
class MatrixDimensions:
    label: str
    width: int
    height: int
    x: int
    y: int
    num_connections: int


@dataclass
class MatrixLabel:
    width: int
    height: int = 80
    y_offset: int = height // 2


@dataclass
class MatrixPorts:
    port_spacing: int = 120
    port_width: int = 60
    port_height: int = 40
    y_offset: int = MatrixLabel.height + port_height
    x_offset: int = 5
