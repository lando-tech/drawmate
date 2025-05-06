from constants.constants import APPLIANCE_ATTRIBUTES_SC, MATRIX_LABEL
from drawmate_engine.drawmate_config import MatrixDimensions
from graph_objects.matrix import Matrix, MatrixMeta
from builder.doc_builder import generate_id
from graph_objects.text_box import TextBox


class MatrixBuilder:
    def __init__(self, matrix_dimensions: MatrixDimensions):
        self.matrix_dimensions = matrix_dimensions
        self.verify_matrix_dimensions()

    def init_matrix_meta(self):
        return MatrixMeta(__ID__=str(generate_id()))

    def init_matrix(self) -> Matrix:
        meta = self.init_matrix_meta()
        return Matrix(
            connections_count=self.matrix_dimensions.num_connections,
            matrix_label=self.matrix_dimensions.labels,
            width=self.matrix_dimensions.width,
            height=self.matrix_dimensions.height,
            x=self.matrix_dimensions.x,
            y=self.matrix_dimensions.y,
            meta=meta,
        )

    def init_matrix_label(self):
        return TextBox(
            x=self.matrix_dimensions.x,
            y=self.matrix_dimensions.y - MATRIX_LABEL["y_offset"],
            width=self.matrix_dimensions.width,
            height=MATRIX_LABEL["height"],
            label=self.matrix_dimensions.labels,
            _type="matrix"
        )

    def verify_matrix_dimensions(self):
        """
        Verifies the matrix dimensions being passed in are the proper size.
        It also verifies the starting X and Y coordinates are in a proper location,
        relative to the size of the graph.
        """
        # Starts +70 on the y-axis (which puts it below the matrix y) and increments that spacing by +120
        initial_y_offset: int = 70
        label_height: int = 20
        total_height: int = (
                (self.matrix_dimensions.num_connections * (APPLIANCE_ATTRIBUTES_SC["height"] + label_height))
                + initial_y_offset
        )
        pad_y_bottom: int = 50
        if self.matrix_dimensions.height < total_height:
            difference: int = total_height - self.matrix_dimensions.height
            self.matrix_dimensions.height = self.matrix_dimensions.height + difference + pad_y_bottom
