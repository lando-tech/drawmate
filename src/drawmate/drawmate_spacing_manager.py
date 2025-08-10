from matrix_constants import MatrixDimensions
from dataclasses import dataclass

DEFAULT_SPACING_Y = 23.33
DEFAULT_SPACING_X = 250
DEFAULT_NODE_HEIGHT = DEFAULT_SPACING_Y * 33.33
DEFAULT_NODE_WIDTH = 120



class DrawmateSpacingManager:
    def __init__(self, matrix_dimensions: MatrixDimensions) -> None:

        self.node_spacing_x: float = DEFAULT_SPACING_X
        self.node_spacing_y: float = DEFAULT_SPACING_Y

        self.port_spacing_x: float = 0
        self.port_spacing_y: float = DEFAULT_NODE_HEIGHT

        self.node_height: float = DEFAULT_NODE_HEIGHT
        self.node_width: float = DEFAULT_NODE_WIDTH

        self.port_height: float = self.node_spacing_y
        self.port_width: float = self.node_width / 2

        self.label_height: float = self.node_spacing_y

        self.matrix_dimensions: MatrixDimensions = matrix_dimensions

        self.matrix_height = self.get_node_height(
            self.matrix_dimensions.num_connections
        )
        self.matrix_width = self.matrix_dimensions.width

        self.base_x = self.matrix_dimensions.x
        self.base_y = self.matrix_dimensions.y
        self.max_y = self.base_y + self.matrix_height

        self.base_height = self.matrix_height

    def get_node_height(self, port_count):
        return (
            (self.port_height * port_count)
            + (self.port_spacing_y * (port_count - 1))
            + (self.label_height + self.port_height)
        )

    def reset_base_y(self, external_base_y):
        if external_base_y > self.max_y:
            return self.base_y
        else:
            return external_base_y
