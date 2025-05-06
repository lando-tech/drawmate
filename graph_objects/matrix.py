from constants.constants import MX_GRAPH_XML_STYLES
from graph_objects.rect import Rect
from dataclasses import dataclass


@dataclass
class MatrixMeta:
    __ID__: str


class Matrix(Rect):
    """
    Summary:
    The Matrix class is used to make Matrix objects on the graph. The matrix
    is the center/focal point of the graph. All objects will be placed on the
    graph based on the position and size of the matrix.

    Args:
        connections_count (int): Number of connections on the matrix.
        width (int): The width of the matrix.
        height (int): The height of the matrix.
        x (int): The X coord of the top left corner of the matrix.
        y (int): The Y coord of the top left corner of the matrix.
    """

    # The default xml style
    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    def __init__(
        self,
        connections_count: int,
        matrix_label: str,
        width: int,
        height: int,
        x: int,
        y: int,
        meta: MatrixMeta = None,
        style=DEFAULT_STYLE,
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            label=matrix_label,
            _type="matrix",
            style=style,
        )
        self.num_connections = connections_count
        self.x = x
        self.y = y
        self.meta = meta
