# # TODO Should these calculations be somewhere outside of the builder?
# @staticmethod
# def calculate_node_height(num_connections: int, current_height: int) -> int:
#     total_height = (
#             (num_connections * NodePorts.height)
#             + NodeLabels.height  # Account for the label at the top
#             + NodePorts.height
#     )
#     return max(current_height, total_height)
#
#
# @staticmethod
# def calculate_input_offset(x: int, y: int, height: int) -> tuple[int, int]:
#     x = x + NodePorts.x_offset
#     y = y + (height - NodePorts.height)
#     return x, y
#
#
# @staticmethod
# def calculate_output_offset(
#         x: int, y: int, height: int, width: int
# ) -> tuple[int, int]:
#     x = x + (width - NodePorts.width) - NodePorts.x_offset
#     y = y + (height - NodePorts.height)
#     return x, y
#
#
# # TODO Should these calculations be outside of the builder?
# def verify_matrix_height(self):
#     """
#     Verifies the matrix height is enough to accommodate all the ports.
#     """
#     total_height: int = (
#         self.matrix_dimensions.num_connections * MatrixPorts.port_spacing
#         + MatrixPorts.port_height
#     )
#     # Ensure padding at the bottom of the matrix
#     pad_y_bottom: int = MatrixPorts.port_height * 2
#     if self.matrix_dimensions.height < total_height:
#         difference: int = total_height - self.matrix_dimensions.height
#         self.matrix_dimensions.height = (
#             self.matrix_dimensions.height + difference + pad_y_bottom
#         )
#
# @staticmethod
# def calculate_port_offset_left(matrix_x: int):
#     return matrix_x + MatrixPorts.x_offset
#
# @staticmethod
# def calculate_port_offset_right(matrix_x: int, matrix_width: int):
#     return (matrix_x + matrix_width) - (
#         MatrixPorts.port_width + MatrixPorts.x_offset
#     )
