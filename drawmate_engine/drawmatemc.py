"""
This is the main entry point for the templating engine.
It contains the core logic for making a basic diagram.
Use this module as a template to implement various network topologies and connection logic.
"""

from drawmate_engine.archive.matrix import Arrow
from drawmate_engine.drawmate_config import DrawmateConfig

from graph_objects.rect import Rect
from graph_objects.matrix import Matrix, MatrixMeta
from graph_objects.appliance import ApplianceMc, ApplianceMetadata
from graph_objects.connections import ConnectionMc
from graph_objects.text_box import TextBox
from drawmate_engine.doc_builder import DocBuilder, generate_id
from mx_graph_api.mxcell import MxCell
from mx_graph_api.mxgeometry import MxGeometry
from mx_graph_api.mxpoint import MxPoint
from drawmate_engine.drawmate_config import MatrixDimensions
from constants.constants import (
    MATRIX_CONNECTIONS,
    MATRIX_LABEL,
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
        self.connections_array: list[ConnectionMc] = []
        self.arrow_array = []

    def create_mxobject(
        self,
        data: dict = None,
        __id__: str = "",
        is_arrow: bool = False,
        has_label: bool = True,
        is_mxarray: bool = False,
        mx_points: tuple = None,
    ):
        """
        Summary:
            Creates the document structure for the XML object, appending each
            node to the appropriate parent.

        Args:
            mx_points:
            is_mxarray (bool): if the object has more than one mxpoint/arrow
            __id__: ID of the graph object
            data (dict): The attributes out from an instance of the Rect class or one of its children.
            is_arrow (bool): Check if the Rect is an ArrowRect.
            has_label (bool): If a label should be added, or a blank string placed instead
        """

        # If the rect being passed in is an arrow, adjust methods accordingly
        if is_arrow:
            # Create mxCell object
            cell = MxCell()
            cell.set_mxcell_values_point(data["style"], data["label"], __id__)

            # Append mxCell to mxObject
            cell_elem = cell.create_xml_element("mxCell", cell.attributes)
            cell.mxcell_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = MxGeometry()
            geo.set_geometry_values_point()
            geo_elem = cell.create_xml_element("mxGeometry", geo.attributes)

            # Append mxGeometry to mxCell
            cell_elem.appendChild(geo_elem)

            # Call the 'create_mxpoint' function
            self.create_mxpoint(mx_geo_elem=geo_elem, mxcell_obj=cell, data=data)
            self.root.appendChild(cell_elem)
        elif is_mxarray:
            # Create mxarray
            self.create_mxarray(mx_points=mx_points)

        else:
            # Create mxCell object
            cell = MxCell()
            if not has_label:
                cell.set_mxcell_values(value="", style=data["style"], __id__=__id__)
            else:
                cell.set_mxcell_values(
                    value=data["label"], style=data["style"], __id__=__id__
                )
            # Append mxCell to mxObject
            cell_elem = cell.create_xml_element("mxCell", cell.attributes)
            cell.mxcell_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = MxGeometry()
            geo.set_geometry_values(data["x"], data["y"], data["width"], data["height"])

            # Append mxGeometry to mxCell
            geo_elem = cell.create_xml_element("mxGeometry", geo.attributes)
            cell_elem.appendChild(geo_elem)
            self.root.appendChild(cell_elem)

    def create_mxpoint(self, mx_geo_elem, mxcell_obj, data: dict):
        """
        Summary:
            Creates the XML structure for and instantiates the mxPoint object.

        Args:
            mx_geo_elem (mxGeometryElement): An instance of the mxGeometry XML element.
            mxcell_obj (mxObject): An instance of the mxObject class.
            data (dict): An attribute dictionary from the instance of the Arrow class.
        """
        # Set source mxPoint element
        source_point = MxPoint()
        source_point.set_mxpoint_source(data["source_x"], data["source_y"])
        source_element = mxcell_obj.create_xml_element(
            "mxPoint", source_point.attributes
        )
        mx_geo_elem.appendChild(source_element)

        # Set target for mxPoint element
        target_point = MxPoint()
        target_point.set_mxpoint_target(data["target_x"], data["target_y"])
        target_elem = mxcell_obj.create_xml_element("mxPoint", target_point.attributes)
        mx_geo_elem.appendChild(target_elem)

    def create_mxarray(self, mx_points):

        for waypoint in mx_points:
            cell = MxCell()
            # src_id = mx_points[0].meta.source_id
            # tgt_id = mx_points[0].meta.target_id
            cell.set_mxcell_values_point(
                waypoint.attributes["style"],
                "",
                str(generate_id()),
                src_id="",
                tgt_id="",
            )

            # Append mxCell to mxObject
            cell_elem = cell.create_xml_element("mxCell", cell.attributes)
            cell.mxcell_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = MxGeometry()
            geo.set_geometry_values_point()
            geo_elem = cell.create_xml_element("mxGeometry", geo.attributes)

            # Append mxGeometry to mxCell
            cell_elem.appendChild(geo_elem)

            source_point = MxPoint()
            target_point = MxPoint()
            source_point.set_mxpoint_source(waypoint.source_x, waypoint.source_y)
            target_point.set_mxpoint_target(waypoint.target_x, waypoint.target_y)
            source_point_elem = cell.create_xml_element(
                "mxPoint", source_point.attributes
            )
            target_point_elem = cell.create_xml_element(
                "mxPoint", target_point.attributes
            )
            geo_elem.appendChild(source_point_elem)
            geo_elem.appendChild(target_point_elem)

            self.root.appendChild(cell_elem)

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
        self.create_arrows()
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
        self.create_mxobject(
            self.matrix.attributes, has_label=False, __id__=self.matrix.meta.__ID__
        )
        self.create_matrix_label()
        self.create_matrix_connections()
        # Create the final XML Document
        self.create_xml(output_file_path=self.output_file)

    def create_matrix(self) -> Matrix:
        """
        Create the matrix object
        Returns:
            Matrix: An instance of the Matrix class
        """
        meta = MatrixMeta(__ID__=str(generate_id()))
        matrix_attrib = self.dc.get_matrix_dimensions()
        self.check_matrix_dimensions(matrix_attrib)
        return Matrix(
            x=matrix_attrib.x,
            y=matrix_attrib.y,
            width=matrix_attrib.width,
            height=matrix_attrib.height,
            connections_count=matrix_attrib.num_connections,
            matrix_label=matrix_attrib.labels,
            meta=meta,
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
            self.create_mxobject(left_text_box.attributes, str(generate_id()))
            self.create_mxobject(right_text_box.attributes, str(generate_id()))
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
        self.create_mxobject(matrix_text_box.attributes, str(generate_id()))

    def process_nodes(
        self, matrix_arr: tuple[list, list]
    ) -> dict[str, list[ApplianceMc]]:
        """
        Process the nodes and configure the x and y spacing. This method will then
        dispatch the nodes to the create_node_array method.
        Args:
            matrix_arr: Matrix Array of left and right nodes.

        Returns:
            dict[str, list[ApplianceMc]]: A dictionary with a list of right and left side Appliance object arrays.
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
            left_nodes,
            left_x,
            start_y,
            x_spacing,
            y_spacing,
            True,
        )
        node_dict["right_side"] = self.create_node_array(
            right_nodes,
            right_x,
            start_y,
            x_spacing,
            y_spacing,
            False,
        )
        return node_dict

    def create_node_array(
        self,
        node_arr: list,
        x,
        start_y,
        x_spacing,
        y_spacing,
        left: bool,
        debug: bool = False,
    ) -> list[ApplianceMc]:
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
                list[ApplianceMc]: A list of Appliance objects
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

            # Iterate through the sublist of Node data
            for r_index, row in enumerate(item):

                __ID__ = generate_id()
                meta = ApplianceMetadata(__SIDE__=side, __ID__=str(__ID__))
                meta.__ROW_INDEX__ = self.get_corresponding_index(
                    r_index, max_per_column
                )
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
                    if len(meta.__INPUT_LABELS__) > 0:
                        for i in range(len(meta.__INPUT_LABELS__)):
                            meta.__LABEL_INDEXES__.append(meta.__ROW_INDEX__ + i)
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

                appliance_node = ApplianceMc(
                    x=x,
                    y=y,
                    label=label,
                    input_label=l_input,
                    output_label=r_output,
                    width=width,
                    height=height,
                    meta=meta,
                )

                if debug:
                    self.debug_print(appliance_node)

                appliance_array.append(appliance_node)

        return appliance_array

    def create_nodes(self, appliance_array: list[ApplianceMc]):
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
                self.create_mxobject(
                    node.attributes, has_label=False, __id__=str(node.meta.__ID__)
                )

    def create_node_in_out_textbox(self, appliance_array: list[ApplianceMc]) -> None:
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

            elif (
                len(node.meta.__INPUT_LABELS__) > 1
                and len(node.meta.__OUTPUT_LABELS__) > 1
            ):

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
        self.create_mxobject(text_box.attributes, str(generate_id()))

    def create_node_label(self, appliance_array: list[ApplianceMc]):
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
            self.create_mxobject(label_textbox.attributes, str(generate_id()))

    def create_node_ptrs(self, appliance_array: list[ApplianceMc], left: bool):
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
                        self.append_connection(appliance, appliance.right_ptr)
                    else:
                        appliance.left_ptr = appliance_array[previous_node_index]
                        self.append_connection(appliance.left_ptr, appliance)

                next_node_index = (next_col * max_rows) + row
                if 0 <= next_node_index < total_nodes:
                    if left:
                        appliance.left_ptr = appliance_array[next_node_index]
                    else:
                        appliance.right_ptr = appliance_array[next_node_index]

    def append_connection(
        self,
        src_node: ApplianceMc | Matrix,
        tgt_node: ApplianceMc | Matrix,
    ):
        """
        Appends a connection between two nodes to the connection array.

        This method creates a new `ConnectionMc` object using the provided source and
        target nodes and adds it to the `connections_array`.

        Args:
            src_node: The source node for the connection. Can be an instance of
                `ApplianceMc` or `Matrix`.
            tgt_node: The target node for the connection. Can be an instance of
                `ApplianceMc` or `Matrix`.
        """
        connection = ConnectionMc(
            src_node=src_node,
            tgt_node=tgt_node,
        )
        self.connections_array.append(connection)

    def create_arrows(self) -> None:
        """
        Generates an array of Arrow objects based on the connections defined in the
        instance's `connections_array`. The method processes each connection, checks
        certain conditions, and creates the corresponding arrow(s). The output array
        may consist of individual Arrow objects or tuples containing multiple Arrows.

        Returns:
            list[Arrow] | list[Arrow, tuple[Arrow, Arrow, Arrow]]: An array of Arrow
            objects or a list containing Arrows and tuples of Arrows. The content of
            the array depends on the connection configurations and processed logic.

        Raises:
            None
        """
        for index, conn in enumerate(self.connections_array):
            if isinstance(conn.src_node, Matrix):
                if (
                    conn.tgt_node.meta.__SPANNING_NODE__
                    or conn.tgt_node.attributes.get("label").strip() == ""
                ):
                    continue
                if conn.tgt_node.meta.__MULTI_CONNECTION_LEFT__:
                    for i, node in enumerate(
                        conn.tgt_node.meta.__CONNECTION_INDEXES_LEFT__
                    ):
                        arrow = conn.create_connection_mc(self.matrix.y, node, i)
                        if isinstance(arrow, tuple):
                            self.create_mxobject(
                                has_label=False,
                                is_mxarray=True,
                                mx_points=arrow,
                                __id__=str(generate_id()),
                            )
                        else:
                            self.create_mxobject(
                                arrow.attributes,
                                has_label=False,
                                is_arrow=True,
                                __id__=str(generate_id()),
                            )
                else:
                    arrow = conn.create_connection_sc()
                    self.create_mxobject(
                        arrow.attributes,
                        has_label=False,
                        is_arrow=True,
                        __id__=str(generate_id()),
                    )
            elif isinstance(conn.src_node, ApplianceMc):
                if conn.src_node.attributes.get("label").strip() == "":
                    continue
                elif isinstance(conn.tgt_node, ApplianceMc):
                    if conn.tgt_node.attributes.get("label").strip() == "":
                        continue
                if conn.src_node.meta.__SIDE__ == "left":
                    if conn.src_node.meta.__SPANNING_NODE__:
                        continue
                    if conn.src_node.meta.__MULTI_CONNECTION_RIGHT__:
                        for i, node in enumerate(
                            conn.src_node.meta.__CONNECTION_INDEXES_RIGHT__
                        ):
                            arrow = conn.create_connection_mc(self.matrix.y, node, i)
                            if isinstance(arrow, tuple):
                                self.create_mxobject(
                                    has_label=False,
                                    is_mxarray=True,
                                    mx_points=arrow,
                                    __id__=str(generate_id()),
                                )
                            else:
                                self.create_mxobject(
                                    arrow.attributes,
                                    has_label=False,
                                    is_arrow=True,
                                    __id__=str(generate_id()),
                                )
                    else:
                        arrow = conn.create_connection_sc()
                        if isinstance(arrow, tuple):
                            self.create_mxobject(
                                has_label=False,
                                is_mxarray=True,
                                mx_points=arrow,
                                __id__=str(generate_id()),
                            )
                        else:
                            self.create_mxobject(
                                arrow.attributes,
                                has_label=False,
                                is_arrow=True,
                                __id__=str(generate_id()),
                            )
                else:
                    if conn.src_node.meta.__MULTI_CONNECTION_RIGHT__:
                        for i, node in enumerate(
                            conn.src_node.meta.__CONNECTION_INDEXES_RIGHT__
                        ):
                            arrow = conn.create_connection_mc(self.matrix.y, node, i)
                            if isinstance(arrow, tuple):
                                self.create_mxobject(
                                    has_label=False,
                                    is_mxarray=True,
                                    mx_points=arrow,
                                    __id__=str(generate_id()),
                                )
                            else:
                                self.create_mxobject(
                                    arrow.attributes,
                                    has_label=False,
                                    is_arrow=True,
                                    __id__=str(generate_id()),
                                )
                    else:
                        arrow = conn.create_connection_sc()
                        if isinstance(arrow, tuple):
                            self.create_mxobject(
                                has_label=False,
                                is_mxarray=True,
                                mx_points=arrow,
                                __id__=str(generate_id()),
                            )
                        else:
                            self.create_mxobject(
                                arrow.attributes,
                                has_label=False,
                                is_arrow=True,
                                __id__=str(generate_id()),
                            )

    def draw_arrows(self):
        for arrow in self.arrow_array:
            if isinstance(arrow, Arrow):
                self.create_mxobject(
                    arrow.attributes,
                    has_label=False,
                    is_arrow=True,
                    __id__=str(generate_id()),
                )
            elif isinstance(arrow, tuple) and len(arrow) == 3:
                self.create_mxobject(
                    has_label=False,
                    is_mxarray=True,
                    mx_points=arrow,
                    __id__=str(generate_id()),
                )

    @staticmethod
    def check_matrix_dimensions(matrix_dims: MatrixDimensions):
        """
        Verifies the matrix dimensions being passed in are the proper size.
        It also verifies the starting X and Y coordinates are in a proper location,
        relative to the size of the graph.
        Args:
            matrix_dims (MatrixDimensions): The dimensions returned by the config file

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
    def debug_print(appliance_node: ApplianceMc):
        print("\n")
        print(
            f"\tLabel         : {appliance_node.attributes.get('label')}\n"
            f"\tSide          : {appliance_node.meta.__SIDE__}\n"
            f"\tSpanning Node : {appliance_node.meta.__SPANNING_NODE__}\n"
            f"\tMulti-Left    : {appliance_node.meta.__MULTI_CONNECTION_LEFT__}\n"
            f"\tMulti-Right   : {appliance_node.meta.__MULTI_CONNECTION_RIGHT__}\n"
            f"\tColumn Index  : {appliance_node.meta.__COLUMN_INDEX__}\n"
            f"\tRow Index     : {appliance_node.meta.__ROW_INDEX__}\n"
            f"\tInput Labels  : {appliance_node.meta.__INPUT_LABELS__}\n"
            f"\tOutput Labels : {appliance_node.meta.__OUTPUT_LABELS__}\n"
        )
