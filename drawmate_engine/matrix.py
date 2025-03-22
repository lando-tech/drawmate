"""
Summary: This is the matrix module, which serves as the architecture for each Node/Object
         on the graph.
"""

from constants.constants import APPLIANCE_ATTRIBUTES_SC


"""
These are the different xml styles used to control the type of object being placed on the graph.
"""
MX_GRAPH_XML_STYLES = {
    "text-box": "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;",
    "rect": "rounded=0;whiteSpace=wrap;html=1;",
    "arrow": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;exitX=1;entryY=0.5;entryDx=0;entryDy=0;",
    "arrow2": "edgeStyle=loopEdgeStyle;orthogonalloop=0;rounded=0;jettySize=auto;html=1",
    "elipse": "ellipse;whiteSpace=wrap;html=1;aspect=fixed;",
}


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
        Summary: The parent class for all graph rects. Used to pass the attributes dictionary
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


class Appliance(Rect):
    """
    Summary: This is child class of the Rect class. It inherits the attributes dictionary.
    This class manages the attributes of the appliances that will be attached to the matrix.

    Args:
        x (int): The X coord for the rect.
        y (int): The Y coord for the rect.
        style (str, optional): xml style for the graph element. Defaults to DEFAULT_STYLE.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    # Add a type argument to pass into each instance of the DTP Rect
    def __init__(
        self,
        x: int,
        y: int,
        label,
        input_label,
        output_label,
        width: int = APPLIANCE_ATTRIBUTES_SC["width"],
        height: int = APPLIANCE_ATTRIBUTES_SC["height"],
        input_label_array: list = None,
        output_label_array: list = None,
        left_ptr_array: list = None,
        right_ptr_array: list = None,
        style=DEFAULT_STYLE,
    ):
        super().__init__(
            x=x,
            y=y,
            style=style,
            label=label,
            _type="DTP",
            width=width,
            height=height,
        )
        self.x = x
        self.y = y
        self.left_ptr = None
        self.right_ptr = None
        self.input_label_array = input_label_array
        self.output_label_array = output_label_array
        self.left_ptr_array = left_ptr_array
        self.right_ptr_array = right_ptr_array
        self.input_label = input_label
        self.output_label = output_label

    def clear_label(self):
        """
        Reset the label as a blank string
        Returns:
        None
        """
        self.attributes["label"] = ""


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
        style=DEFAULT_STYLE,
    ):

        super().__init__(
            x=x, y=y, width=width, height=height, label=label, style=style, _type=_type
        )
        self.x = x
        self.y = y


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


class Connections:
    """
    Summary: Accepts an instance of a target and source rect, and manages the connections between the two objects.
    It also servers as a dispatcher for the Arrow class
    and adds an instance of the Arrow class between the source and target.

    Args:
        target_rect (Rect): An instance of a target Rect.
        source_rect (Rect): An instance of a source Rect.
        col_index   (int) : The current column index of the source/target rect
        left        (bool): If the object is on the left or right side
        mc          (bool): If the object has multiple connections
    """

    def __init__(
        self,
        source_rect: Rect,
        target_rect: Rect,
        col_index: int,
        left: bool,
        mc: bool = False,
    ):
        # y offset, default is set to center connection on object
        # this offset will place the connection on the IN/OUT label instead of the center of
        # the appliance
        if mc:
            self.offset = -40
        else:
            self.offset = 20

        self.source_x = int(source_rect.attributes["x"])
        self.target_x = int(target_rect.attributes["x"])

        if (col_index == 0 and left) or left:
            self.target_y = int(source_rect.attributes["y"]) + (
                (int(source_rect.attributes["height"]) // 2) + self.offset
            )
            self.source_y = self.target_y
        elif col_index == 0:
            self.source_y = int(target_rect.attributes["y"]) + (
                (int(target_rect.attributes["height"]) // 2) + self.offset
            )
            self.target_y = self.source_y
        else:
            self.source_y = int(source_rect.attributes["y"]) + (
                (int(source_rect.attributes["height"]) // 2) + self.offset
            )
            self.target_y = self.source_y

    def create_connection(self, label: str, _type: str):
        """
        Returns an instance of the Arrow class
        Args:
            label (str): The label for the arrow
            _type (str): The type descriptor
        """
        arrow = Arrow(
            target_x=self.target_x,
            target_y=self.target_y,
            source_x=self.source_x,
            source_y=self.source_y,
            _type=_type,
            label=label,
        )
        return arrow
