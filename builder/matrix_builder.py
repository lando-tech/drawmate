from constants.matrix_constants import MatrixDimensions, MatrixPorts, MatrixLabel
from graph_objects.matrix import Matrix, MatrixMeta
from builder.doc_builder import generate_id
from graph_objects.text_box import TextBox


class MatrixBuilder:
    def __init__(self, matrix_dimensions: MatrixDimensions):
        self.matrix_dimensions = matrix_dimensions
        self.verify_matrix_height()

    def init_matrix_meta(self):
        return MatrixMeta(__ID__=str(generate_id()))

    def init_matrix(self) -> Matrix:
        meta = self.init_matrix_meta()
        return Matrix(
            connections_count=self.matrix_dimensions.num_connections,
            matrix_label=self.matrix_dimensions.label,
            width=self.matrix_dimensions.width,
            height=self.matrix_dimensions.height,
            x=self.matrix_dimensions.x,
            y=self.matrix_dimensions.y,
            meta=meta,
        )

    def init_matrix_label(self):
        return TextBox(
            x=self.matrix_dimensions.x,
            y=self.matrix_dimensions.y,
            width=self.matrix_dimensions.width,
            height=MatrixLabel.height,
            label=self.matrix_dimensions.label,
            _type="matrix",
            style="rounded=0;whiteSpace=wrap;html=1;",
        )

    def init_matrix_ports(
        self, spacing: int, connection_labels: tuple[list, list]
    ) -> list[TextBox]:
        ports = []
        left_side, right_side = connection_labels
        max_len = self.matrix_dimensions.num_connections

        left_ports_x = self.calculate_port_offset_left(
            matrix_x=self.matrix_dimensions.x
        )
        right_ports_x = self.calculate_port_offset_right(
            matrix_x=self.matrix_dimensions.x, matrix_width=self.matrix_dimensions.width
        )
        y = self.matrix_dimensions.y + MatrixPorts.y_offset

        for i in range(max_len):
            left_text_box = TextBox(
                x=left_ports_x,
                y=y,
                width=MatrixPorts.port_width,
                height=MatrixPorts.port_height,
                label=left_side[i],
                _type="text-box",
            )
            right_text_box = TextBox(
                x=right_ports_x,
                y=y,
                width=MatrixPorts.port_width,
                height=MatrixPorts.port_height,
                label=right_side[i],
                _type="text-box",
            )
            ports.append(left_text_box)
            ports.append(right_text_box)
            y += spacing

        return ports

    def verify_matrix_height(self):
        """
        Verifies the matrix height is enough to accommodate all the ports.
        """
        total_height: int = (
            self.matrix_dimensions.num_connections * MatrixPorts.y_offset
            + MatrixPorts.port_height
        )
        # Ensure padding at the bottom of the matrix
        pad_y_bottom: int = MatrixPorts.port_height
        if self.matrix_dimensions.height < total_height:
            difference: int = total_height - self.matrix_dimensions.height
            self.matrix_dimensions.height = (
                self.matrix_dimensions.height + difference + pad_y_bottom
            )

    @staticmethod
    def calculate_port_offset_left(matrix_x: int):
        return matrix_x + MatrixPorts.x_offset

    @staticmethod
    def calculate_port_offset_right(matrix_x: int, matrix_width: int):
        return (matrix_x + matrix_width) - (
            MatrixPorts.port_width + MatrixPorts.x_offset
        )
