from drawmate.doc_builder import DocBuilder, generate_id


class MxCell(DocBuilder):
    """_summary_"""

    def __init__(self) -> None:
        super().__init__()
        self.attributes = {
            "id": "",
            "value": "",
            "style": "",
            "parent": "1",
            "connectable": "1",
            "edge": "",
            "vertex": "",
            "source": "",
            "target": "",
        }
        self.mxcell_object = self.new_xml.createElement("mxCell")

    def set_mxcell_values(self, value: str, style: str, __id__: str = ""):
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
            # print("Using Node ID")
        else:
            self.attributes["id"] = generate_id()
            # print("Generating Node ID")

    def set_mxcell_values_point(
        self,
        style: str,
        value: str,
        __id__: str = None,  # type: ignore
        src_id: str = None,  # type: ignore
        tgt_id: str = None,  # type: ignore
    ):
        """_summary_

        Args:
            __id__:
            src_id:
            tgt_id:
            style (str): The xml style for the object
            value (str): The value will be the label on the object once drawn.
        """
        # self.attributes["vertex"] = "1"
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
            self.attributes["target"] = str(tgt_id)
        else:
            self.attributes["target"] = ""

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
