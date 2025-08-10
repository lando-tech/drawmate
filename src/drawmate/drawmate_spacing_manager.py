from matrix_constants import MatrixDimensions

class DrawmateSpacingManager:
    def __init__(self, matrix_dimensions: MatrixDimensions) -> None:
        self.matrix_dimensions: MatrixDimensions = matrix_dimensions

        self.base_x = self.matrix_dimensions.x
        self.base_y = self.matrix_dimensions.y

        self.node_spacing_x: float
        self.node_spacing_y: float

        self.port_spacing_x: float
        self.port_spacing_y: float
