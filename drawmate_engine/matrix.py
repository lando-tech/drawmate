"""
Summary:
"""

# import json
from drawmate_engine.doc_builder import generate_id
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
        super().__init__(
            x=x, y=y, width=width, height=height, label=matrix_label, _type="matrix"
        )
        # Number of connections on Matrix
        self.num_connections = connections_count
        # Array to store each text box on the matrix
        self.matrix_text_boxes = []
        # Array to store each appliance attached to the matrix
        self.dtp_rects = []
        # Array to store the text boxes for the appliances attached to the matrix
        self.dtp_text_boxes = []
        # Array to store the second level appliances attached to the matrix/first level appliances
        self.second_level_dtp_rects = []
        # Array to store the third level appliances attached to the matrix/second level appliances
        self.third_level_dtp_rects = []

    def add_matrix_label(self, matrix_x, matrix_y, matrix_label: str):
        """_summary_

        Returns:
            _type_: _description_
        """
        _label = matrix_label
        _width = 200
        _height = 80
        label_x = matrix_x
        label_y = matrix_y
        label_textbox = TextBox(
            x=int(label_x),
            y=int(label_y),
            width=_width,
            height=_height,
            label=_label,
            style=MX_GRAPH_XML_STYLES["rect"],
            _type="matrix_label",
        )

        return label_textbox

    def add_matrix_textbox(self, label: str, _type: str, is_output: bool):
        """
        Summary: Creates a new instance of the TextBox class and dynamically
        sets the X and Y coordinates based on spacing and the position of the
        element the text box will be placed on.

        Args:
            label (str): The label for the text box, which will be shown on the graph object.
            _type (_type_): See README for type descriptor naming conventions.
            is_output (bool): Determines wether the text is an output.
                              If true, the text box will be placed on the right side of the object.
        """
        # Default spacing for each text box
        spacing = INPUT_OUTPUT_SPACING_MATRIX
        width = 60
        height = 30
        # The default xml style
        style = MX_GRAPH_XML_STYLES["text-box"]
        # The y coord of the parent element
        base_y = int(self.attributes["y"])
        # Add an argument to change the x coordinate offset (currently 140)

        if is_output:
            textbox_x = int(self.attributes["x"]) + 140
            textbox_y = base_y + (
                ((len(self.matrix_text_boxes) - self.num_connections) * spacing) + 145
            )
        else:
            textbox_x = int(self.attributes["x"])
            textbox_y = (
                int(self.attributes["y"])
                + (len(self.matrix_text_boxes) * spacing)
                + 145
            )

        # Instance of the text box
        textbox = TextBox(
            x=textbox_x,
            y=textbox_y,
            width=width,
            height=height,
            label=label,
            style=style,
            _type=_type,
        )
        # Append text box to array
        self.matrix_text_boxes.append(textbox)

    def create_matrix_textboxes(self, matrix_labels: list[list, list]):
        """
        Iteratively calls the add_textbox function based on the number of inputs/outputs,
        and sets the label for each, respectively.
        """
        labels_left = matrix_labels[0]
        for i in range(self.num_connections):
            self.add_matrix_textbox(
                label=f"&nbsp;&nbsp;&nbsp;{labels_left[i]}",
                _type="input",
                is_output=False,
            )

        labels_right = matrix_labels[1]
        for i in range(self.num_connections):
            self.add_matrix_textbox(
                label=f"&nbsp;&nbsp;&nbsp;{labels_right[i]}",
                _type="output",
                is_output=True,
            )

    def add_appliance_label(self, dtp_x: int, dtp_y: int, label: str):
        """_summary_

        Args:
            dtp_x (int): _description_
            dtp_y (int): _description_
            label (str): _description_

        Returns:
            _type_: _description_
        """
        label_x = dtp_x
        label_y = dtp_y
        style = MX_GRAPH_XML_STYLES["rect"]
        width = 160
        height = 40
        dtp_label = TextBox(
            x=label_x,
            y=label_y,
            width=width,
            height=height,
            label=label,
            style=style,
            _type="text-box",
        )
        return dtp_label

    def add_appliance_textbox(
        self,
        dtp_x: int,
        dtp_y: int,
        in_label: str,
        out_label: str,
    ):
        """_summary_

        Args:
            dtp_x (int): x coord of current appliance.
            dtp_y (int): y coord of current appliance.
            in_label: label for input of the appliance - DEFAULT = IN.
            out_label: label for output of the appliance - DEFAULT = OUT.
        """
        # dtp width = 160, height = 80
        # spacing = INPUT_OUTPUT_SPACING_APPLIANCE
        height = 40
        style = MX_GRAPH_XML_STYLES["text-box"]

        out_x = dtp_x + 100
        out_y = dtp_y + 40
        in_x = dtp_x
        in_y = dtp_y + 40

        if len(out_label) > 3:
            out_label = f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{out_label}"
            out_width = 80
        else:
            out_label = f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{out_label}"
            out_width = 60

        if len(in_label) > 3:
            in_label = f"&nbsp;&nbsp;{in_label}"
            in_width = 80
        else:
            in_label = f"&nbsp;&nbsp;&nbsp;{in_label}"
            in_width = 60

        output_textbox = TextBox(
            x=out_x,
            y=out_y,
            width=out_width,
            height=height,
            label=out_label,
            style=style,
            _type="text-box",
        )
        input_textbox = TextBox(
            x=in_x,
            y=in_y,
            width=in_width,
            height=height,
            label=in_label,
            style=style,
            _type="text-box",
        )
        self.dtp_text_boxes.append(input_textbox)
        self.dtp_text_boxes.append(output_textbox)

    def add_first_level_appliance(
        self, is_left: bool, has_label: bool, in_label: str, out_label: str
    ):
        """
        Summary: Creates a new instance of the Dtp class and appends it to the appropriate array.
        It also dynamically sets the Y coords based on the parent element (matrix).

        Args:
            is_left (bool): If the object is on the left side the X and Y coordinates will vary.
        """
        # Add an argument to change the x and y offset
        if is_left:
            x = int(self.attributes["x"]) - 400
            y = (
                int(self.attributes["y"])
                + (len(self.dtp_rects) * 100)
                + INPUT_OUTPUT_SPACING_APPLIANCE
            )
            dtp_rect_1 = Dtp(x=x, y=y)
            if has_label:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )
        else:
            x = int(self.attributes["x"]) + 420
            y = (
                int(self.attributes["y"])
                + ((len(self.dtp_rects) - self.num_connections) * 100)
                + INPUT_OUTPUT_SPACING_APPLIANCE
            )
            dtp_rect_1 = Dtp(x=x, y=y)
            if has_label:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )

        # Append the dtp object to the array
        self.dtp_rects.append(dtp_rect_1)

    def create_first_level_appliance(self, appliance_labels):
        """
        Iteratively calls the add_first_level_dtp function based
        on the number of left and right appliances.
        """
        left_labels = appliance_labels[0]
        right_labels = appliance_labels[1]
        has_label = True
        for i in range(self.num_connections):
            if left_labels[i][0].strip() == "":
                has_label = False
            else:
                has_label = True
            in_label_left = left_labels[i][1]
            out_label_left = left_labels[i][2]
            self.add_first_level_appliance(
                is_left=True,
                has_label=has_label,
                in_label=in_label_left,
                out_label=out_label_left,
            )

        for i in range(self.num_connections):
            if right_labels[i][0].strip() == "":
                has_label = False
            else:
                has_label = True
            in_label_right = right_labels[i][1]
            out_label_right = right_labels[i][2]
            self.add_first_level_appliance(
                is_left=False,
                has_label=has_label,
                in_label=in_label_right,
                out_label=out_label_right,
            )

    def add_second_level_appliance(
        self,
        is_left: bool,
        first_level_x: str,
        first_level_y: str,
        current_label: str,
        in_label: str,
        out_label: str,
    ):
        """
        Summary: Creates new instances of the left and right
        appliances on the second level of the graph,
        and appends them to the appropriate array.
        It also dynamically adjusts the y coordinates for proper
        spacing.

        Args:
            is_left (bool): Should the appliance be placed on the left or right side of the matrix.
            first_level_x (str): The X coord of the first level appliance closest to the element.
                                 Taken in as a string, but will be converted to an integer.
            first_level_y (str): The Y coord of the first level appliance closest to the element.
                                 Taken in as a string, but will be converted to an integer.
        """
        x_offset = 400
        y_offset = 1000
        # Add an argument to change the x and y offset or a default value
        if is_left:
            x = int(first_level_x) - x_offset
            y = int(first_level_y) + (self.num_connections * 100) - y_offset
            if current_label.strip() == "":
                pass
            else:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )
                # Debug print statements
                # print(f"Second level label left: {current_label}")
                # print(f"Second level x: {x}")
                # print(f"Second level y: {y}\n")
                # print("==============================")
            dtp_rect = Dtp(x=x, y=y)
        else:
            x = int(first_level_x) + x_offset
            y = int(first_level_y) + (self.num_connections * 100) - y_offset
            if current_label.strip() == "":
                pass
            else:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )
                # Debug print statements
                # print(f"Second level label right: {current_label}")
                # print(f"Second level x: {x}")
                # print(f"Second level y: {y}\n")
                # print("==============================")
            dtp_rect = Dtp(x=x, y=y)

        self.second_level_dtp_rects.append(dtp_rect)

    # Add third and fourth level DTP appliances
    def add_third_level_appliance(
        self,
        first_level_x: int,
        first_level_y: int,
        is_left: bool,
        current_label: str,
        in_label: str,
        out_label: str,
    ):
        """_summary_

        Args:
            first_level_x (int): _description_
            first_level_y (int): _description_
            is_left (bool): _description_
        """
        y_offset = 1000
        x_offset = 400
        if is_left:
            x = int(first_level_x) - x_offset
            y = int(first_level_y) + (self.num_connections * 100) - y_offset
            if current_label.strip() == "":
                pass
            else:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )
                # Debug print statements
                # print(f"Third level label left: {current_label}")
                # print(f"Third level x: {x}")
                # print(f"Third level y: {y}\n")
                # print("==============================")

            dtp_rect = Dtp(x=x, y=y)
        else:
            x = int(first_level_x) + x_offset
            y = int(first_level_y) + (self.num_connections * 100) - y_offset
            if current_label.strip() == "":
                pass
            else:
                self.add_appliance_textbox(
                    dtp_x=x,
                    dtp_y=y,
                    in_label=in_label,
                    out_label=out_label,
                )
                # Debug print statements
                # print(f"Third level label right: {current_label}")
                # print(f"Third level x: {x}")
                # print(f"Third level y: {y}\n")
                # print("==============================")
            dtp_rect = Dtp(x=x, y=y)

        self.third_level_dtp_rects.append(dtp_rect)

    # def add_fourth_level_appliance(self):
    #     """_summary_
    #     """
    #     pass


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
    def __init__(self, x: int, y: int, style=DEFAULT_STYLE):
        super().__init__(
            x=x, y=y, style=style, label="", _type="DTP", width=160, height=80
        )


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
        style: str,
        _type: str,
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

    def __init__(self, target_rect, source_rect, first_level: bool):
        # Dictionary to store all connections
        self.tracker = {}

        # y offset, default is set to center connection on object
        # this offset will place the connection on the IN/OUT label instead of the center of
        # the appliance
        if first_level:
            self.y_offset_source = 0
        else:
            self.y_offset_source = 20

        self.y_offset_target = 20
        # Array to store connections for later processing
        self.connections_array = []

        # Ensure left-to-right flow
        if int(source_rect.attributes["x"]) < int(target_rect.attributes["x"]):
            self.source_x = min(
                int(
                    source_rect.attributes["x"]
                ),  # + int(source_rect.attributes["width"]),
                int(target_rect.attributes["x"]),
            ) + int(source_rect.attributes["width"])

            self.target_x = int(target_rect.attributes["x"])
        else:
            self.source_x = min(
                int(source_rect.attributes["x"]), int(target_rect.attributes["x"])
            ) + int(target_rect.attributes["width"])

            self.target_x = max(
                int(source_rect.attributes["x"]), int(target_rect.attributes["x"])
            )

        self.target_y = int(target_rect.attributes["y"]) + (
            (int(target_rect.attributes["height"]) // 2) + self.y_offset_target
        )

        # print("\n==============================\n")
        # print(f"Connection: Target y = {self.target_y}")
        # print(f"Target label: {target_rect.attributes['label']}")

        self.source_y = int(source_rect.attributes["y"]) + (
            # 3715
            # 3734.47
            (int(source_rect.attributes["height"]) // 2)
            + self.y_offset_source
        )

        # print(f"Connection: Source y = {self.source_y}")
        # print(f"Source label: {source_rect.attributes['label']}")
        # print("\n==============================\n")

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
        _id = generate_id()
        self.tracker.update(dict({_id: arrow.attributes}))
        return arrow
        # self.connections_array.append(arrow)
