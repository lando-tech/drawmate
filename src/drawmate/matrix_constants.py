from dataclasses import dataclass


@dataclass
class MatrixDimensions:
    label: str
    width: int
    height: int
    x: int
    y: int
    num_connections: int
