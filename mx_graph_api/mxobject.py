from drawmate_engine.doc_builder import DocBuilder
from drawmate_engine.doc_builder import generate_id
from constants.constants import MX_OBJECT_ATTRIBUTES


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
