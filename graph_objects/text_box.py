from graph_objects.rect import Rect
from constants.constants import MX_GRAPH_XML_STYLES


class TextBox(Rect):
    """
    Summary: This class is a child of the Rect class and manages the attributes for each
    instance of a text box on the graph.

    Args:
        x (int): The X coord for the rect.
        y (int): The Y coord for the rect.
        width (int): Width of the rect.
        height (int): Height of the rect.
        label (str): Label for the textbox.
        style (str): The style of the textbox.
        _type (str): The type descriptor: See README for type naming convention.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["text-box"]

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        _type: str,
        _id: str = None,
        style=DEFAULT_STYLE,
    ):

        super().__init__(
            x=x, y=y, width=width, height=height, label=label, style=style, _type=_type
        )
        self.x = x
        self.y = y
        self.id = _id
