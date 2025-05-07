from dataclasses import dataclass


@dataclass
class NodeAttributes:
    width: int = 160
    height: int = 210
    x_spacing: int = 400
    y_spacing: int = 120


@dataclass
class NodeLabels:
    width: int = NodeAttributes.width
    height: int = 40


@dataclass
class NodePorts:
    width: int = 60
    height: int = 40
    y_offset: int = 45
    x_offset: int = 5
