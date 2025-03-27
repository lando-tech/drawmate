"""Add summary"""

from xml.dom.minidom import getDOMImplementation
from datetime import datetime
import random

# Imports the pathfinder class from the utils directory.
# See the pathfinder.py for specific uses.
from utils.pathfinder import PathFinder
from utils.log_manager import LogManager
from constants.constants import MX_OBJECT_ATTRIBUTES,TOP_LEVEL_MX_CELL, MX_ARRAY_ATTRIBUTES, MX_GRAPH_MODEL_ATTRIBUTES

# Instance of the pathfinder class for directory navigation
pf = PathFinder()
log_mgr = LogManager()


def get_timestamp() -> str:
    """
    Create a timestamp for the template file

    Returns:
        str: A formatted timestamp
    """
    timestamp = datetime.now().replace(microsecond=0)
    formatted_timestamp = timestamp.strftime("%Y-%m-%dT%I%M%S")

    return formatted_timestamp


TEMPLATE_STORAGE_PATH = (
    f"{pf.xml_template_dir}builder_template__{get_timestamp()}.drawio"
)


class DocBuilder:
    """
    The top level class for building the boilerplate xml structure for the template.
    self.newXML is the instance that controls document creation for the entire
    xml file. There should only be one instance of the doc builder at a time, and
    all other objects should be implemented using the relative instance.
    """

    def __init__(self) -> None:

        # Instantiates the DOMImplementation from xml.minidom
        self.builder = getDOMImplementation()
        # Instantiates the root level document
        self.new_xml = self.builder.createDocument(None, "mxfile", None)
        # Instantiates the top level document element, which will be passed to self.root
        self.top_level = self.new_xml.documentElement
        # Instantiates the diagram tag for the xml file
        self.diagram = self.new_xml.createElement("diagram")
        # Instantiates the mxGraphModel tag for the xml file
        self.mx_graph_model = self.new_xml.createElement("mxGraphModel")
        # Root tag where all mxCell and Object tags will be placed
        self.root = self.new_xml.createElement("root")

        self.set_top_level_cells()
        self.create_xml_structure()

    def create_xml_structure(self):
        """
        Instantiates the appropriate parent/child elements to the file
        """
        # Append mxGraphModel to diagram
        self.diagram.appendChild(self.mx_graph_model)
        # Append root to mxGraphModel
        self.mx_graph_model.appendChild(self.root)
        # Append diagram to top_level of document
        self.top_level.appendChild(self.diagram)

    def set_graph_values(self, dx: int, dy: int, page_width: int, page_height: int):
        """
        Summary: This function sets the dimensions for the graph. All calculations and placement
        of graph objects will be directly affected by the parameters passed to this function.

        Args:
            dx (int): Represents the offset of the top left corner to the origin point on the graph, on the x-axis
            dy (int): Represents the offset of the top left corner to the origin point on the graph, on the y-axis
            page_width (int): The desired width of the page
            page_height (int): The desired height of the page
        """

        # set initial graph values
        MX_GRAPH_MODEL_ATTRIBUTES["dx"] = str(dx)
        MX_GRAPH_MODEL_ATTRIBUTES["dy"] = str(dy)
        MX_GRAPH_MODEL_ATTRIBUTES["pageWidth"] = str(page_width)
        MX_GRAPH_MODEL_ATTRIBUTES["pageHeight"] = str(page_height)

        for k, v in MX_GRAPH_MODEL_ATTRIBUTES.items():
            self.mx_graph_model.setAttribute(attname=k, value=v)

    def set_top_level_cells(self):
        """Summary
        Each draw.io diagram needs two top level mxCells, this function ensures those items are added appropriately,
        with the proper default values.
        """
        cell_one = self.new_xml.createElement("mxCell")
        cell_two = self.new_xml.createElement("mxCell")
        for k, v in TOP_LEVEL_MX_CELL.items():
            if k == "id":
                cell_one.setAttribute(k, v)
                cell_two.setAttribute(k, "1")
            if k == "parent":
                cell_two.setAttribute(k, v)
        self.root.appendChild(cell_one)
        self.root.appendChild(cell_two)

    def create_xml(self, output_file_path: str):
        """
        Summary:
        Writes the xml template to disk, omitting the xml declaration.
        """
        xml_data = self.new_xml.childNodes[0].toprettyxml(indent="  ")
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(xml_data)
                if file:
                    log_data = f"Export-Template file saved: {output_file_path}"
                    log_mgr.add_log(
                        object_log="doc_builder",
                        message=log_data,
                        line_number="216",
                        is_error=False,
                        is_warning=False,
                    )
                else:
                    print("File not saved")
                    # Print statement used for debugging. This will print the raw xml string
                    # print(self.newXML.childNodes[0].toprettyxml(indent="  "))
        except IOError as e:
            error_message = f"Error saving template file" + f"\nError message: {e}"
            log_mgr.add_log(
                object_log="doc_builder",
                message=error_message,
                line_number="225",
                is_error=True,
                is_warning=False,
            )

        try:
            with open(TEMPLATE_STORAGE_PATH, "w", encoding="utf-8") as temp_file:
                temp_file.write(xml_data)
                success_msg = f"Storage-Template file saved: {TEMPLATE_STORAGE_PATH}"
                log_mgr.add_log(
                    object_log="doc_builder",
                    message=success_msg,
                    line_number="230",
                    is_error=False,
                    is_warning=False,
                )
        except IOError as e:
            error_message = f"Error saving template file" + f"\nError message: {e}"
            log_mgr.add_log(
                object_log="doc_builder",
                message=error_message,
                line_number="239",
                is_error=True,
                is_warning=False,
            )


class MxObject(DocBuilder):
    """
    Summary: The MxObject class is a child of the DocBuilder class. Its main function is to
    facilitate the proper structure for each xml element and ensure that the proper nesting
    of each xml element is managed accordingly. For instance: The object is the top level tag,
    followed by mxCell, mxGeometry, mxPoint, and mxArray (if any). The MxObject class can be
    instantiated as much as needed to create a new object on the graph, ensuring the structure
    is accurate and consistent throughout template/diagram creation. It is crucial that only
    one instance of the doc builder class exists since MxObject inherits the top level structure of the file.
    Otherwise, the object might be added to the wrong instance of a DocBuilder object, resulting
    in inaccurate xml structure.
    """

    def __init__(self) -> None:
        # Top level mxObject
        super().__init__()
        # Inherits the attributes from the MX_OBJECT_ATTRIBUTES
        self.attributes = MX_OBJECT_ATTRIBUTES
        # Creates a new xml element
        self.mx_object = self.new_xml.createElement("object")

        self.create_object_node()
        # Generates a unique id for the object
        self.__id__ = generate_id()
        # Array to store a list of all id's on the graph
        self.id_array = []

    def create_object_node(self):
        """_summary_"""
        # Append the object to the root element of the xml file
        self.root.appendChild(self.mx_object)

    def set_object_values(self, label: str, _type: str, __id__: str = None):
        """
        Summary: Sets the attributes for the object element.
        Each element contains a minimum of three values by default,
        however, the label can be passed as an empty string if no
        label is required.

        Args:
            __id__ (str): Optional ID to track various metadata about objects on the graph
            label (str): The label for the object that will appear on the graph
            _type (str): The type descriptor, see more in the README for specific naming conventions
        """
        # Set attributes for mxObject
        self.attributes["label"] = label
        self.attributes["type"] = _type
        if __id__:
            self.attributes["id"] = __id__
        else:
            self.attributes["id"] = str(self.__id__)
        self.id_array.append(self.attributes["id"])

        # Iteratively set the attributes for the xml element
        for k, v in self.attributes.items():
            self.mx_object.setAttribute(k, v)

    def add_child_nodes(self, child):
        """Add child nodes to each instance of mxObject"""
        self.mx_object.appendChild(child)

    def create_xml_element(self, tag: str, attrib: dict):
        """
        Summary: Creates each child element of the xml
        object element, and sets all the attributes of the child
        iteratively.

        Args:
            tag (str): The name of the xml tag, mxCell, mxGeometry, mxPoint, mxArray
            attrib (dict): The dictionary of attributes for each element.
            See documentation for the Rect class for more details.

        Returns:
            XML Element: An xml element with all attributes.
        """
        # Add error checking for incorrect tag names.
        # Must be within draw.io standard naming convention for xml tags.
        # Add error checking for incorrect data type for the attrib argument.
        # Print a more useful message.

        # Create the new element with the appropriate tag
        element = self.new_xml.createElement(tag)
        # Iteratively set the attributes for the element
        for k, v in attrib.items():
            if v is None:
                pass
            else:
                element.setAttribute(k, v)

        return element

    class MxCell:
        """_summary_"""

        def __init__(self) -> None:
            self.attributes = {
                "id": "",
                "value": "",
                "style": "",
                "parent": "1",
                "connectable": "",
                "edge": "",
                "vertex": "",
                "source": "",
                "target": "",
            }

        def set_mxcell_values(self, value: str, style: str, __id__: str = None):
            """_summary_

            Args:
                __id__: Optional ID, one is generated automatically unless explicitly passed
                value (str): _description_
                style (str): _description_
            """
            self.attributes["value"] = value
            self.attributes["style"] = style
            self.attributes["vertex"] = "1"
            if __id__:
                self.attributes["id"] = __id__
            else:
                self.attributes["id"] = str(generate_id())

        def set_mxcell_values_point(self, style: str, value: str, __id__: str = None, src_id: str = None, tgt_id: str = None):
            """_summary_

            Args:
                __id__:
                src_id:
                tgt_id:
                style (str): The xml style for the object
                value (str): The value will be the label on the object once drawn.
            """
            self.attributes["vertex"] = ""
            self.attributes["value"] = value
            self.attributes["style"] = style
            self.attributes["edge"] = "1"

            if __id__:
                self.attributes["id"] = __id__
            else:
                self.attributes["id"] = str(generate_id())

            if src_id:
                self.attributes["source"] = str(src_id)
            else:
                self.attributes["source"] = ""

            if tgt_id:
                self.attributes["target"] = ""
            else:
                self.attributes["target"] = ""

        class MxGeometry:
            """_summary_"""

            def __init__(self) -> None:
                self.attributes = {
                    "x": "",
                    "y": "",
                    "width": "",
                    "height": "",
                    "relative": "",
                    "as": "geometry",
                }

            def set_geometry_values(self, x: int, y: int, width: int, height: int):
                """_summary_

                Args:
                    x (int): X coordinate
                    y (int): Y coordinate
                    width (int): object width
                    height (int): object height
                """
                self.attributes["x"] = str(x)
                self.attributes["y"] = str(y)
                self.attributes["width"] = str(width)
                self.attributes["height"] = str(height)

            def set_geometry_values_point(self):
                """
                Set mxGeometry point values
                Returns: None

                """
                self.attributes["relative"] = "1"
                self.attributes["x"] = ""
                self.attributes["y"] = ""
                self.attributes["width"] = ""
                self.attributes["height"] = ""

            class MxPoint:
                """_summary_"""

                def __init__(self) -> None:
                    self.attributes = {
                        "x": "",
                        "y": "",
                        "as": "",
                    }

                def set_mxpoint_source(self, x: int, y: int):
                    """_summary_

                    Args:
                        x (int): _description_
                        y (int): _description_
                    """
                    self.attributes["x"] = str(x)
                    self.attributes["y"] = str(y)
                    self.attributes["as"] = "sourcePoint"

                def set_mxpoint_target(self, x: int, y: int):
                    """_summary_

                    Args:
                        x (int): _description_
                        y (int): _description_
                    """
                    self.attributes["x"] = str(x)
                    self.attributes["y"] = str(y)
                    self.attributes["as"] = "targetPoint"

                class MxArray:
                    """_summary_"""

                    def __init__(self) -> None:
                        self.attributes = MX_ARRAY_ATTRIBUTES

                    def set_array_values(self, as_relative: str):
                        """_summary_

                        Args:
                            as_relative (str): _description_
                        """
                        self.attributes["as"] = as_relative


def create_document(x: int, y: int, width: int, height: int) -> DocBuilder:
    """
    Summary:
    Creates an instance of the DocBuilder class and sets the starting values for
    the graph.

    Args:
        x (int): dx for the mxGraphModel xml tag.
        y (int): dy for the mxGraphModel xml tag.
        width (int): pageWidth for the mxGraphModel xml tag.
        height (int): pageHeight for the mxGraphModel xml tag.

    Returns:
        DocBuilder: Instance of the DocBuilder
    """

    # Create document and set graph values
    _doc = DocBuilder()
    _doc.set_graph_values(x, y, width, height)
    return _doc


def generate_id() -> int:
    """
    Summary:
    Generates a unique id for each object.
    Returns:
        int: A unique id.
    """
    start = 100000000000000000
    stop = 9999999999999999999
    _id = random.randrange(start=start, stop=stop)
    return _id
