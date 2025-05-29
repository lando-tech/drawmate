"""Add summary"""

from xml.dom.minidom import getDOMImplementation
from datetime import datetime
import random

# Imports the pathfinder class from the utils directory.
# See the pathfinder.py for specific uses.
# from pathfinder import PathFinder
# from log_manager import LogManager
from constants import (
    TOP_LEVEL_MX_CELL,
    MX_GRAPH_MODEL_ATTRIBUTES,
)

# Instance of the pathfinder class for directory navigation
# pf = PathFinder()
# log_mgr = LogManager()


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

def get_timestamp() -> str:
    """
    Create a timestamp for the template file

    Returns:
        str: A formatted timestamp
    """
    timestamp = datetime.now().replace(microsecond=0)
    formatted_timestamp = timestamp.strftime("%Y-%m-%dT%I%M%S")

    return formatted_timestamp


# TEMPLATE_STORAGE_PATH = (
#     f"{pf.xml_template_dir}builder_template__{get_timestamp()}.drawio"
# )


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
        self.diagram.setAttribute(attname="name", value="Page-1")
        self.diagram.setAttribute(attname="id", value=str(generate_id()))
        # Append mxGraphModel to diagram
        self.diagram.appendChild(self.mx_graph_model)
        # Append root to mxGraphModel
        self.mx_graph_model.appendChild(self.root)
        # Append diagram to top_level of document
        self.top_level.appendChild(self.diagram) # type: ignore

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
                # if file:
                #     log_data = f"Export-Template file saved: {output_file_path}"
                #     log_mgr.add_log(
                #         object_log="doc_builder",
                #         message=log_data,
                #         line_number="216",
                #         is_error=False,
                #         is_warning=False,
                #     )
                # else:
                #     print("File not saved")
                #     # Print statement used for debugging. This will print the raw xml string
                #     # print(self.newXML.childNodes[0].toprettyxml(indent="  "))
        except IOError as e:
            error_message = f"Error saving template file" + f"\nError message: {e}"
            print(error_message)
            exit()
            # log_mgr.add_log(
            #     object_log="doc_builder",
            #     message=error_message,
            #     line_number="225",
            #     is_error=True,
            #     is_warning=False,
            # )

        # try:
        #     with open(TEMPLATE_STORAGE_PATH, "w", encoding="utf-8") as temp_file:
        #         temp_file.write(xml_data)
        #         # success_msg = f"Storage-Template file saved: {TEMPLATE_STORAGE_PATH}"
        #         # log_mgr.add_log(
        #         #     object_log="doc_builder",
        #         #     message=success_msg,
        #         #     line_number="230",
        #         #     is_error=False,
        #         #     is_warning=False,
        #         # )
        # except IOError as e:
        #     error_message = f"Error saving template file" + f"\nError message: {e}"
        #     log_mgr.add_log(
        #         object_log="doc_builder",
        #         message=error_message,
        #         line_number="239",
        #         is_error=True,
        #         is_warning=False,
        #     )


