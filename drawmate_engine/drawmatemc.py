"""
This is the main entry point for the templating engine.
It contains the core logic for making a basic diagram.
Use this module as a template to implement various network topologies and connection logic.
"""

from drawmate_engine.drawmate_config import DrawmateConfig

from graph_objects.rect import Rect
from graph_objects.matrix import Matrix
from graph_objects.appliance import Appliance, ApplianceMetadata
from graph_objects.connections import Connection
from graph_objects.text_box import TextBox
from drawmate_engine.doc_builder import DocBuilder, MxObject, generate_id
from drawmate_engine.drawmate_config import MatrixDimensions
from constants.constants import (
    MATRIX_CONNECTIONS,
    MATRIX_LABEL,
    # ARROW_CONNECTIONS,
    APPLIANCE_ATTRIBUTES_SC,
    APPLIANCE_ATTRIBUTES_MC,
    APPLIANCE_INPUT,
    APPLIANCE_OUTPUT,
    APPLIANCE_INPUT_OUTPUT_DIMS,
)


class DrawmateMc(DocBuilder):
    """
    This class serves as a basic template to construct a generic AV/Audio/Network diagram,
    with an instance of the Matrix class serving as the center of the infrastructure.
    """

    def __init__(self, input_file: str, output_file: str):
        super().__init__()
        # JSON input file
        self.input_file = input_file
        # File to write the output
        self.output_file = output_file
        # An instance of the DrawmateConfig class
        self.dc = DrawmateConfig(template_path=self.input_file)
        # The multidimensional array return from the drawmate_config module
        self.matrix_array = self.dc.build_matrix_array()
        # Create an instance of the Matrix class
        self.matrix = self.create_matrix()
        self.node_dict = {}
        self.connections_array: list[Connection] = []

    def create_mxobject(
        self, data: dict, is_arrow: bool = False, has_label: bool = True
    ):
        """
        Summary:
            Creates the document structure for the xml object, appending each
            node to the appropriate parent.

        Args:
            data (dict): The attributes of an instance of the Rect class or one of its children.
            is_arrow (bool): Check if the Rect is an ArrowRect.
            has_label (bool): If a label should be added, or a blank string placed instead
        """
        # Create object node
        mx_obj = MxObject()
        if not has_label:
            mx_obj.set_object_values("", data["type"])
        else:
            mx_obj.set_object_values(data["label"], data["type"])
        # If the rect being passed in is an arrow, adjust methods accordingly
        if is_arrow:
            # Create mxCell object
            cell = mx_obj.MxCell()
            cell.set_mxcell_values_point(data["style"], data["label"])

            # Append mxCell to mxObject
            cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
            mx_obj.mx_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = cell.MxGeometry()
            geo.set_geometry_values_point()
            geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)

            # Append mxGeometry to mxCell
            cell_elem.appendChild(geo_elem)

            # Call to the create_mxpoint function
            self.create_mxpoint(
                mx_geo=geo, mx_geo_elem=geo_elem, mx_obj=mx_obj, data=data
            )

        else:
            # Create mxCell object
            cell = mx_obj.MxCell()
            if not has_label:
                cell.set_mxcell_values(value="", style=data["style"])
            else:
                cell.set_mxcell_values(value=data["label"], style=data["style"])
            # Append mxCell to mxObject
            cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
            mx_obj.mx_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = cell.MxGeometry()
            geo.set_geometry_values(data["x"], data["y"], data["width"], data["height"])

            # Append mxGeometry to mxCell
            geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)
            cell_elem.appendChild(geo_elem)

        # Get root element of xml
        # Append mxObject to root
        self.root.appendChild(mx_obj.mx_object)

    def create_mxpoint(self, mx_geo, mx_geo_elem, mx_obj, data: dict):
        """
        Summary:
            Creates the xml structure for, and instantiates the mxPoint object.

        Args:
            mx_geo (mxGeometry): An instance of the mxGeometry class.
            mx_geo_elem (mxGeometryElement): An instance of the mxGeometry xml element.
            mx_obj (mxObject): An instance of the mxObject class.
            data (dict): An attribute dictionary from the instance of the Arrow class.
        """
        # Set source mxPoint element
        source_point = mx_geo.MxPoint()
        source_point.set_mxpoint_source(data["source_x"], data["source_y"])
        source_element = mx_obj.create_xml_element("mxPoint", source_point.attributes)
        mx_geo_elem.appendChild(source_element)

        # Set target mxPoint element
        target_point = mx_geo.MxPoint()
        target_point.set_mxpoint_target(data["target_x"], data["target_y"])
        target_elem = mx_obj.create_xml_element("mxPoint", target_point.attributes)
        mx_geo_elem.appendChild(target_elem)

    def build_graph(self):
        """
        Dispatches each method to create the graph/xml document
        Returns:
        None
        """
        # Set Graph values
        self.set_graph_values(dx=4000, dy=4000, page_width=4000, page_height=4000)
        # Initialize the matrix
        matrix_array = self.dc.build_matrix_array()
        # Process nodes
        self.node_dict = self.process_nodes(matrix_array)
        # Create Node pointers
        self.create_node_ptrs(self.node_dict["left_side"], left=True)
        self.create_node_ptrs(self.node_dict["right_side"], left=False)
        # Create Connections for Nodes
        self.create_connections()
        # Create nodes
        self.create_nodes(self.node_dict["left_side"])
        self.create_nodes(self.node_dict["right_side"])
        # Create Label input/output textbox for each node
        self.create_node_in_out_textbox(self.node_dict["left_side"])
        self.create_node_in_out_textbox(self.node_dict["right_side"])
        # Create label textboxes for each node
        self.create_node_label(self.node_dict["left_side"])
        self.create_node_label(self.node_dict["right_side"])
        # Create the matrix object
        self.create_mxobject(self.matrix.attributes, has_label=False)
        self.create_matrix_label()
        self.create_matrix_connections()
        # Create final XML Document
        self.create_xml(output_file_path=self.output_file)

    def create_matrix(self) -> Matrix:
        """
        Create the matrix object
        Returns:
            Matrix: An instance of the Matrix class
        """
        matrix_attrib = self.dc.get_matrix_dimensions()
        self.check_matrix_dimensions(matrix_attrib)
        return Matrix(
            x=matrix_attrib.x,
            y=matrix_attrib.y,
            width=matrix_attrib.width,
            height=matrix_attrib.height,
            connections_count=matrix_attrib.num_connections,
            matrix_label=matrix_attrib.labels,
        )

    def create_matrix_connections(self):
        """
        Create the connection labels for the matrix
        Returns:
        None
        """
        # Left and right side labels
        left_side, right_side = self.dc.get_matrix_connection_labels()
        # Total number of connections
        max_len = self.matrix.num_connections
        # Height and Width of the textbox
        width = MATRIX_CONNECTIONS["width"]
        height = MATRIX_CONNECTIONS["height"]
        # Starting x and y values
        left_x = int(self.matrix.attributes["x"]) + MATRIX_CONNECTIONS["x_offset_left"]
        right_x = (
            int(self.matrix.attributes["x"]) + MATRIX_CONNECTIONS["x_offset_right"]
        )
        y = int(self.matrix.attributes["y"]) + MATRIX_CONNECTIONS["y_offset"]

        for i in range(max_len):
            left_text_box = TextBox(
                x=left_x,
                y=y,
                width=width,
                height=height,
                label=left_side[i],
                _type="text-box",
            )
            right_text_box = TextBox(
                x=right_x,
                y=y,
                width=width,
                height=height,
                label=right_side[i],
                _type="text-box",
            )
            self.create_mxobject(left_text_box.attributes)
            self.create_mxobject(right_text_box.attributes)
            y += MATRIX_CONNECTIONS["label_spacing"]

    def create_matrix_label(self):
        """
        Create the label for the matrix
        Returns:
        None
        """
        x = int(self.matrix.attributes["x"])
        y = int(self.matrix.attributes["y"]) - MATRIX_LABEL["y_offset"]
        width = int(self.matrix.attributes["width"])
        height = MATRIX_LABEL["height"]
        m_label = self.matrix.attributes["label"]
        matrix_text_box = TextBox(
            x=x,
            y=y,
            width=width,
            height=height,
            label=m_label,
            _type="matrix",
            style="rounded=0;whiteSpace=wrap;html=1;",
        )
        self.create_mxobject(matrix_text_box.attributes)

    def process_nodes(
        self, matrix_arr: tuple[list, list]
    ) -> dict[str, list[Appliance]]:
        """
        Process the nodes and configure the x and y spacing. This method will then
        dispatch the nodes to the create_node_array method.
        Args:
            matrix_arr: Matrix Array of left and right nodes.

        Returns:
            dict[str, list[Appliance]]: A dictionary with a list of right and left side Appliance object arrays.
        """

        node_dict = {}
        x_spacing = APPLIANCE_ATTRIBUTES_SC["x_spacing"]
        y_spacing = APPLIANCE_ATTRIBUTES_SC["y_spacing"]
        left_x = int(self.matrix.attributes["x"]) - x_spacing
        right_x = int(self.matrix.attributes["x"]) + x_spacing
        start_y = int(self.matrix.attributes["y"]) - (y_spacing - 25)
        left_nodes = matrix_arr[0]
        right_nodes = matrix_arr[1]
        node_dict["left_side"] = self.create_node_array(
            left_nodes, left_x, start_y, x_spacing, y_spacing, True,
        )
        node_dict["right_side"] = self.create_node_array(
            right_nodes, right_x, start_y, x_spacing, y_spacing, False,
        )
        return node_dict

    def create_node_array(
        self, node_arr: list, x, start_y, x_spacing, y_spacing, left: bool, debug: bool = False
    ) -> list[Appliance]:
        """
        Creates the Appliance nodes for the left and right sides of the matrix.
        Args:
            debug : if debug print statements are needed
            node_arr: The multidimensional array of objects, which will be instantiated as Appliance objects
            x: The starting x coordinate
            start_y: The starting y coordinate (the matrix y - spacing/offset)
            x_spacing: The x spacing for each row on the grid
            y_spacing: The y spacing for each object on the grid
            left: If the multidimensional array belongs to the left or right side of the grid

        Returns:
                list[Appliance]: A list of Appliance objects
        """
        if not left:
            x += 40

        # Array of Appliance objects
        appliance_array = []
        # Max number of appliances per row on the graph
        max_per_column = self.matrix.num_connections

        # Get the side of the matrix the node is to be placed
        side = "left" if left else "right"
        column_index = 0
        for index, item in enumerate(node_arr):
            # Set starting y coordinate
            y = start_y
            if index > 0:
                x = x - x_spacing if left else x + x_spacing

            # Iterate through sublist of Node data
            for r_index, row in enumerate(item):

                __ID__ = generate_id()
                meta = ApplianceMetadata(__SIDE__=side, __ID__=str(__ID__))
                meta.__ROW_INDEX__ = self.get_corresponding_index(r_index, max_per_column)
                meta.__COLUMN_INDEX__ = column_index

                if meta.__ROW_INDEX__ == max_per_column - 1:
                    column_index += 1

                label = row[0]
                if label == "__SPAN__":
                    meta.__SPANNING_NODE__ = True
                else:
                    meta.__SPANNING_NODE__ = False

                l_input = row[1]
                r_output = row[2]

                if isinstance(l_input, list):
                    meta.__INPUT_LABELS__ = l_input
                    l_input = None

                if isinstance(r_output, list):
                    meta.__OUTPUT_LABELS__ = r_output
                    r_output = None

                connections_left = row[3]
                connections_right = row[4]
                meta.__CONNECTION_INDEXES_LEFT__ = connections_left
                meta.__CONNECTION_INDEXES_RIGHT__ = connections_right

                if connections_left[0] == "NONE" and connections_right[0] == "NONE":
                    y += y_spacing
                    width = APPLIANCE_ATTRIBUTES_SC["width"]
                    height = APPLIANCE_ATTRIBUTES_SC["height"]
                else:
                    if connections_left[0] != "NONE":
                        meta.__MULTI_CONNECTION_LEFT__ = True
                    else:
                        meta.__MULTI_CONNECTION_LEFT__ = False
                    if connections_right[0] != "NONE":
                        meta.__MULTI_CONNECTION_RIGHT__ = True
                    else:
                        meta.__MULTI_CONNECTION_RIGHT__ = False

                    y += y_spacing
                    width = APPLIANCE_ATTRIBUTES_MC["width"]
                    height = APPLIANCE_ATTRIBUTES_MC["height"]

                appliance_node = Appliance(
                    x=x,
                    y=y,
                    label=label,
                    input_label=l_input,
                    output_label=r_output,
                    width=width,
                    height=height,
                    meta=meta
                )

                if debug:
                    self.debug_print(appliance_node)

                appliance_array.append(appliance_node)

        return appliance_array

    def create_nodes(self, appliance_array: list[Appliance]):
        """
        Creates the mxobject instance for each node iteratively
        Args:
            appliance_array: A list of Appliance objects

        Returns:
            None
        """
        for index, node in enumerate(appliance_array):
            if node.attributes["label"].strip() == "":
                continue
            if node.attributes["label"].strip() == "__SPAN__":
                continue
            else:
                self.create_mxobject(node.attributes, has_label=False)

    def create_node_in_out_textbox(self, appliance_array: list[Appliance], debug: bool = False) -> None:
        """
        Create the textbox objects for the input and output labels for each node
        Args:
            appliance_array: The array of left or right side Appliance objects

        Returns:
            None
        """

        for node in appliance_array:
            label_buffer = 15
            spacing = int(node.attributes["height"]) / 2 + label_buffer
            # Input attributes
            input_x = int(node.x) + APPLIANCE_INPUT["x_offset"]
            input_y = int(node.y) + APPLIANCE_INPUT["y_offset"]
            # Output attributes
            output_x = int(node.x) + APPLIANCE_OUTPUT["x_offset"]
            output_y = int(node.y) + APPLIANCE_OUTPUT["y_offset"]
            # width and height
            width = APPLIANCE_INPUT_OUTPUT_DIMS["width"]
            height = APPLIANCE_INPUT_OUTPUT_DIMS["height"]

            if node.meta.__SPANNING_NODE__:
                continue
            # If a single label, meaning a single in/out connection
            elif node.input_label and node.output_label:
                self.dispatch_in_out_textbox(
                    input_x, input_y, width, height, node.input_label
                )
                self.dispatch_in_out_textbox(
                    output_x, output_y, width, height, node.output_label
                )

            elif len(node.meta.__INPUT_LABELS__) > 1 and len(node.meta.__OUTPUT_LABELS__) > 1:

                for index, item in enumerate(node.meta.__INPUT_LABELS__):

                    input_label = item
                    output_label = node.meta.__OUTPUT_LABELS__[index]

                    self.dispatch_in_out_textbox(
                        input_x, input_y, width, height, input_label
                    )
                    self.dispatch_in_out_textbox(
                        output_x, output_y, width, height, output_label
                    )

                    input_y += spacing
                    output_y += spacing
            else:
                pass

    def dispatch_in_out_textbox(self, x, y, width, height, label):
        text_box = TextBox(
            x=x, y=y, width=width, height=height, label=label, _type="textbox"
        )
        self.create_mxobject(text_box.attributes)

    def create_node_label(self, appliance_array: list[Appliance]):
        """
        Create labels for each node/appliance
        Args:
            appliance_array: A list of either left-side or right-side appliances/nodes

        Returns:
            None
        """

        for a_index, appliance in enumerate(appliance_array):
            if appliance.attributes["label"].strip() == "":
                continue
            if appliance.attributes["label"].strip() == "__SPAN__":
                continue
            label_textbox = Rect(
                x=appliance.attributes["x"],
                y=appliance.attributes["y"],
                width=appliance.attributes["width"],
                height=40,
                label=appliance.attributes["label"],
                _type="text-box",
            )
            self.create_mxobject(label_textbox.attributes)

    def create_node_ptrs(self, appliance_array: list[Appliance], left: bool):
        """
        Create pointers for each node to manage connections on the graph
        Args:
            appliance_array: The array of either left/right side appliances
            left: if the array being passed in is on the left of the matrix

        Returns:
            None
        """
        max_rows = self.matrix.num_connections
        total_nodes = len(appliance_array)
        for i, appliance in enumerate(appliance_array):
            col, row = appliance.meta.__COLUMN_INDEX__, appliance.meta.__ROW_INDEX__
            next_col = col + 1
            previous_col = col - 1
            if col == 0:
                if left:
                    appliance.right_ptr = self.matrix
                    self.append_connection(appliance, appliance.right_ptr)
                else:
                    appliance.left_ptr = self.matrix
                    self.append_connection(appliance.left_ptr, appliance)
            else:
                previous_node_index = (previous_col * max_rows) + row
                if 0 <= previous_node_index < total_nodes:
                    if left:
                        appliance.right_ptr = appliance_array[previous_node_index]
                        self.append_connection(
                            appliance, appliance.right_ptr
                        )
                    else:
                        appliance.left_ptr = appliance_array[previous_node_index]
                        self.append_connection(
                            appliance.left_ptr, appliance
                        )

                next_node_index = (next_col * max_rows) + row
                if 0 <= next_node_index < total_nodes:
                    if left:
                        appliance.left_ptr = appliance_array[next_node_index]
                    else:
                        appliance.right_ptr = appliance_array[next_node_index]

    def append_connection(
        self,
        src_node: Appliance | Matrix,
        tgt_node: Appliance | Matrix,
    ):
        connection = Connection(
            src_node=src_node,
            tgt_node=tgt_node,
        )
        self.connections_array.append(connection)

    def create_connections(self) -> None:
        """
        Iterates through self.connections_array and creates arrows/connections
        between each object on the graph.
        Returns:

        """

        for index, conn in enumerate(self.connections_array):

            if isinstance(conn.src_node, Matrix):
                if conn .tgt_node.meta.__SPANNING_NODE__ or conn.tgt_node.attributes.get('label').strip() == "":
                    continue
                if conn.tgt_node.meta.__MULTI_CONNECTION_LEFT__:
                    for node in conn.tgt_node.meta.__CONNECTION_INDEXES_LEFT__:
                        arrow = conn.create_connection_mc(self.matrix.y, node)
                        self.create_mxobject(arrow.attributes, is_arrow=True)
                else:
                    arrow = conn.create_connection_sc()
                    self.create_mxobject(arrow.attributes, is_arrow=True)

            elif isinstance(conn.src_node, Appliance):

                if conn.src_node.meta.__SPANNING_NODE__ or conn.src_node.attributes.get('label').strip() == "":
                    continue
                if conn.src_node.meta.__SIDE__ == "left":
                    if conn.src_node.meta.__MULTI_CONNECTION_RIGHT__:
                        for node in conn.src_node.meta.__CONNECTION_INDEXES_RIGHT__:
                            arrow = conn.create_connection_mc(self.matrix.y, node)
                            self.create_mxobject(arrow.attributes, is_arrow=True)
                    else:
                        arrow = conn.create_connection_sc()
                        self.create_mxobject(arrow.attributes, is_arrow=True)
                else:
                    if conn.src_node.meta.__MULTI_CONNECTION_RIGHT__:
                        for node in conn.src_node.meta.__CONNECTION_INDEXES_RIGHT__:
                            arrow = conn.create_connection_mc(self.matrix.y, node)
                            self.create_mxobject(arrow.attributes, is_arrow=True)
                    else:
                        arrow = conn.create_connection_sc()
                        self.create_mxobject(arrow.attributes, is_arrow=True)

    @staticmethod
    def check_matrix_dimensions(matrix_dims: MatrixDimensions):
        """
        Verifies the matrix dimensions being passed in are the proper size.
        It also verifies the starting X and Y coordinates are in a proper location,
        relative to the size of the graph.
        Args:
            matrix_dims (MatrixDimensions) : The dimensions returned by the config file

        Returns:
            bool: True if the dimensions are within bounds
        """
        # Starts +70 on the y-axis (which puts it below the matrix y) and increments that spacing by +120
        total_height = (
            matrix_dims.num_connections * (APPLIANCE_ATTRIBUTES_SC["height"] + 20)
        ) + 70
        if matrix_dims.height < total_height:
            # print(f"Matrix not large enough. Height = {matrix_dims.height}px")
            # print(f"Total height of appliances w/spacing = {total_height}px")
            # print("Adjusting height to compensate for the difference.")
            difference = total_height - matrix_dims.height
            matrix_dims.height = matrix_dims.height + difference + 50
            # print("New height of matrix: " + f"{matrix_dims.height}px")
        # else:
        #     print("Matrix is large enough, no adjustments needed.")

    @staticmethod
    def generate_connection_number(column_index: int, counter: int, left: bool) -> str:
        """
        Create a numbering system for the connections between each appliance
        Args:
            column_index: The current column index of the node
            counter: The counter to track number position of the appliance
            left: If the appliance is on the left or right of the matrix

        Returns:
        Formatted string with the correct number
        """
        if left:
            if counter < 10 and column_index == 0:
                return "000" + str(counter)
            if counter >= 10 and column_index == 0:
                return "00" + str(counter)
            if counter >= 10:
                return "0" + str(column_index) + str(counter)
            else:
                return "0" + str(column_index) + "0" + str(counter)
        else:
            if counter < 10 and column_index == 0:
                return "100" + str(counter)
            if counter >= 10 and column_index == 0:
                return "10" + str(counter)
            if counter >= 10:
                return "1" + str(column_index) + str(counter)
            else:
                return "1" + str(column_index) + "0" + str(counter)

    @staticmethod
    def get_corresponding_index(node_index: int, max_per_column: int) -> int:
        """
        Given a node index and the max nodes per column,
        return the (column index, row index) for the node.
        Args:
            node_index: index of current node
            max_per_column: total number of nodes per column

        Returns:
            column_index: int, row_index: int
        """
        row_index = node_index % max_per_column
        return row_index

    @staticmethod
    def debug_print(appliance_node: Appliance):
        print("\n")
        print(f"\tLabel         : {appliance_node.attributes.get('label')}\n"
              f"\tSide          : {appliance_node.meta.__SIDE__}\n"
              f"\tSpanning Node : {appliance_node.meta.__SPANNING_NODE__}\n"
              f"\tMulti-Left    : {appliance_node.meta.__MULTI_CONNECTION_LEFT__}\n"
              f"\tMulti-Right   : {appliance_node.meta.__MULTI_CONNECTION_RIGHT__}\n"
              f"\tColumn Index  : {appliance_node.meta.__COLUMN_INDEX__}\n"
              f"\tRow Index     : {appliance_node.meta.__ROW_INDEX__}\n"
              f"\tInput Labels  : {appliance_node.meta.__INPUT_LABELS__}\n"
              f"\tOutput Labels : {appliance_node.meta.__OUTPUT_LABELS__}\n")
