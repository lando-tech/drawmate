from constants.constants import MX_GRAPH_XML_STYLES


class Rect:
    """
    The Rect class is the parent class for all objects on the graph.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        _type: str,
        style=DEFAULT_STYLE,
    ):
        """
        Summary: The parent class for all graph graph_objects. Used to pass the attributes dictionary
        to all children.

        Args:
            x (int): X coordinate for the top left corner of the rect.
            y (int): Y coordinate for the top left corner of the rect.
            width (int): Width of the rect.
            height (int): Height of the rect.
            label (str): The label of the rect.
            _type (str): The type descriptor: See README for type naming convention.
            style (str, optional): xml style type. Defaults to DEFAULT_STYLE.
        """
        self.attributes = {
            "x": f"{x}",
            "y": f"{y}",
            "width": f"{width}",
            "height": f"{height}",
            "label": label,
            "style": style,
            "type": _type,
        }
        self.x = x
        self.y = y


class ArrowRect:
    """
    The ArrowRect class is the base class for connections/arrows on the graph.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["arrow"]

    def __init__(
        self,
        target_x: int,
        target_y: int,
        source_x: int,
        source_y: int,
        label: str,
        _type: str,
        style=DEFAULT_STYLE,
    ) -> None:
        """
        Summary: The parent rect for all connections/arrows on the graph. Since the
        connections have additional attributes, this class allows for better management
        of connection elements.

        Args:
            target_x (int): The target X coord of the arrow.
            target_y (int): The target Y coord of the arrow.
            source_x (int): The source X coord of the arrow.
            source_y (int): The source Y coord of the arrow.
            label (str): A label for the arrow. If no label is needed, pass an empty string.
            _type (str): The type descriptor: See README for type naming convention.
            style (str, optional): The xml style type. Defaults to DEFAULT_STYLE.
        """
        self.attributes = {
            "target_x": target_x,
            "target_y": target_y,
            "source_x": source_x,
            "source_y": source_y,
            "label": label,
            "style": style,
            "type": _type,
        }
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y
