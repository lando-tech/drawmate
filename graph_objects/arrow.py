from graph_objects.rect import ArrowRect
from constants.constants import MX_GRAPH_XML_STYLES


class Arrow(ArrowRect):
    """
    Summary: This class is a child of the ArrowRect class and inherits the attributes dictionary.
    It is used to manage each arrow/connection and its attributes.

    Args:
        target_x (int): Target X coord.
        target_y (int): Target Y coord.
        source_x (int): Source X coord.
        source_y (int): Source Y coord
        label (str): Label for the arrow/connection, if none pass an empty string.
        _type (str): The type descriptor: See README for type naming convention.
        style (str, optional): xml style for arrows/connections. Defaults to DEFAULT_STYLE.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["arrow2"]

    def __init__(
        self,
        target_x: int,
        target_y: int,
        source_x: int,
        source_y: int,
        label: str,
        _type: str,
        style=DEFAULT_STYLE,
    ):

        super().__init__(
            target_x=target_x,
            target_y=target_y,
            source_x=source_x,
            source_y=source_y,
            label=label,
            _type=_type,
            style=style,
        )
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y
