from dataclasses import dataclass

from constants.matrix_constants import MatrixPorts, MatrixLabel


@dataclass
class NodeAttributes:
    width: int = 160
    height: int = 80
    x_spacing: int = 400
    y_spacing: int = 20


@dataclass
class NodeLabels:
    width: int = NodeAttributes.width
    height: int = MatrixLabel.height


@dataclass
class NodePorts:
    width: int = 80
    height: int = 40
    spacing: int = 40
    y_offset: int = 45
    x_offset: int = 0
