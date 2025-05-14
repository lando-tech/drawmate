from dataclasses import dataclass


@dataclass
class NodeAttributes:
    width: int = 160
    height: int = 80
    x_spacing: int = 400
    y_spacing: int = height + 20


@dataclass
class NodeLabels:
    width: int = NodeAttributes.width
    height: int = 40


@dataclass
class NodePorts:
    width: int = 60
    height: int = 40
    spacing: int = 40
    y_offset: int = 45
    x_offset: int = 10
