"""
Summary:
"""

# import json
from utils.pathfinder import PathFinder

# Instance of the pathfinder class for directory navigation
pf = PathFinder()

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

"""
This value is used to set the input and output spacing on the relative
matrix on the graph.
"""
INPUT_OUTPUT_SPACING_MATRIX = 100
INPUT_OUTPUT_SPACING_APPLIANCE = 100


class Rect:
    """_summary_"""

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


class ArrowRect:
    """_summary_"""

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


class Matrix(Rect):
    """
    Summary:
    The matrix is the focal point for the diagram/template. The main role of the matrix is to
    create all the elements that will directly or indirectly be connected to it. The matrix
    acts as the starting point for all other elements to be drawn around it. Multiple instances
    of the matrix may be created, and each matrix will manage its own connections.

    Args:
        connections_count (int): Number of connections on the matrix.
        width (int): The width of the matrix.
        height (int): The height of the matrix.
        x (int): The X coord of the top left corner of the matrix.
        y (int): The Y coord of the top left corner of the matrix.
    """

    def __init__(
        self,
        connections_count: int,
        matrix_label: str,
        width: int,
        height: int,
        x: int,
        y: int,
    ):
        super().__init__(x=x, y=y, width=width, height=height, label="", _type="matrix")
        self.num_connections = connections_count


class Dtp(Rect):
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
        self, x: int, y: int, label, input_label, output_label, style=DEFAULT_STYLE
    ):
        super().__init__(
            x=x, y=y, style=style, label=label, _type="DTP", width=160, height=90
        )
        self.left_ptr = None
        self.right_ptr = None
        self.input_label = input_label
        self.output_label = output_label

    def clear_label(self):
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
    WIDTH = 60
    HEIGHT = 30

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


class Connections:
    """
    Summary: Accepts an instance of a target and source rect, and manages the connections between the two objects.
    It also servers as a dispatcher for the Arrow class and adds the instance of the Arrow class between the source and target.

    Args:
        target_rect (Rect): An instance of a target Rect.
        source_rect (Rect): An instance of a source Rect.
    """

    def __init__(
        self, source_rect: Rect, target_rect: Rect, col_index: int, left: bool
    ):
        # y offset, default is set to center connection on object
        # this offset will place the connection on the IN/OUT label instead of the center of
        # the appliance
        self.y_offset_source = 20
        self.y_offset_target = 20
        self.source_x = int(source_rect.attributes["x"])
        self.target_x = int(target_rect.attributes["x"])

        if (col_index == 0 and left) or left:
            self.target_y = int(source_rect.attributes["y"]) + (
                (int(source_rect.attributes["height"]) // 2) + self.y_offset_target
            )
            self.source_y = self.target_y
        elif col_index == 0:
            self.source_y = int(target_rect.attributes["y"]) + (
                # 3715
                # 3734.47
                (int(target_rect.attributes["height"]) // 2)
                + self.y_offset_source
            )
            self.target_y = self.source_y
        else:
            self.source_y = int(source_rect.attributes["y"]) + (
                # 3715
                # 3734.47
                (int(source_rect.attributes["height"]) // 2)
                + self.y_offset_source
            )
            self.target_y = self.source_y

    def create_connection(self, label: str, _type: str):
        """_summary_

        Args:
            label (str): _description_
            _type (str): _description_
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
