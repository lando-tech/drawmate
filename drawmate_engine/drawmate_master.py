from constants.constants import APPLIANCE_ATTRIBUTES_SC
from doc_builder import DocBuilder
from drawmate_config import DrawmateConfig, MatrixDimensions
from graph_objects.arrow import Arrow
from graph_objects.matrix import Matrix, MatrixMeta
from mx_graph_api.mxcell import MxCell
from mx_graph_api.mxgeometry import MxGeometry
from mx_graph_api.mxpoint import MxPoint
from doc_builder import generate_id


class DrawmateMaster(DocBuilder):
    """
    This is the top-level class for the templating engine.
    It contains the core logic for building the XML document and
    orchestrating the creation of the graph/xml document.
    """

    def __init__(self, input_file: str, output_file: str):
        super().__init__()
        # JSON input file
        self.input_file = input_file
        # File to write the output
        self.output_file = output_file
        # An instance of the DrawmateConfig class
        self.dc = DrawmateConfig(template_path=self.input_file)
        # The multidimensional array returned from the drawmate_config module
        self.matrix_array = self.dc.build_matrix_array()

    def create_mxcell(
        self,
        data: dict = None,
        __id__: str = "",
        has_label: bool = True,
    ):
        """
        Summary:
            Creates the document structure for the XML object, appending each
            node to the appropriate parent.

        Args:
            __id__: ID of the graph object
            data (dict): The attributes out from an instance of the Rect class or one of its children.
            has_label (bool): If a label should be added, or a blank string placed instead
        """
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

    def create_mxcell_arrow(self, data: dict = None, __id__: str = ""):
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

    @staticmethod
    def create_mxpoint(mx_geo_elem, mxcell_obj, data: dict):
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

    def create_mxarray(self, mx_points: tuple[Arrow]):
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

    def create_node(self):
        pass

    def create_textbox(self):
        pass

    def create_connections(self):
        pass

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
        total_height = ( matrix_dims.num_connections * (APPLIANCE_ATTRIBUTES_SC["height"] + 20) ) + 70
        if matrix_dims.height < total_height:
            difference = total_height - matrix_dims.height
            matrix_dims.height = matrix_dims.height + difference + 50