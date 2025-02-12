"""
Summary:
"""

import json
import os
import sys
import re
from datetime import datetime
from utils.pathfinder import PathFinder

try:
    from lxml.etree import Element, ElementTree
    from lxml import etree
except ModuleNotFoundError:
    print("lxml module not found")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
pf = PathFinder()


class Json2Xml:
    """_summary_"""

    def __init__(self) -> None:
        # self.patternOne = r"\{\{.*?\}\}"
        self.path_finder = pf
        self.timestamp = datetime.now().replace(microsecond=0)
        self.formatted_timestamp = self.timestamp.strftime("%a %d %b %Y, %H:%M:%S")
        self.parent_cells = {}

    def xml2json(self, node, index=0, include_root=True):
        """
        Converts a DOM node to a dictionary with unique keys, optionally excluding the root node's name.

        :param node: The DOM node to convert.
        :param index: Index for the current node for unique naming.
        :param include_root: Whether to include the root node's name in the dictionary.
        :return: A dictionary representing the node.
        """
        # Determine the key suffix based on the index
        key_suffix = f"-{index}" if index > 0 else ""
        node_key = node.nodeName + key_suffix if include_root else ""

        # Prepare the node dictionary
        node_dict = {} if not include_root else {node_key: {}}
        current_dict = node_dict if include_root else {}

        # Include attributes if they exist
        if node.attributes:
            attrs = {
                attr: node.attributes[attr].value for attr in node.attributes.keys()
            }
            if include_root:
                current_dict[node_key] = attrs
            else:
                current_dict.update(attrs)

        # Include child nodes
        children_counts = {}
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                # Track the count of each child node type
                children_counts[child.nodeName] = (
                    children_counts.get(child.nodeName, 0) + 1
                )
                # Recursively add child nodes as dictionaries with unique keys
                child_dict = self.xml2json(child, children_counts[child.nodeName] - 1)
                if include_root:
                    current_dict[node_key].update(child_dict)
                else:
                    current_dict.update(child_dict)

        return node_dict if include_root else current_dict

    def json_to_dict(self, json_data):
        """Convert JSON data to Python dictionary."""
        return json.loads(json_data)

    def dict_to_xml(self, tag, d):
        """Convert a dictionary to XML, handling CDATA and preserving structure."""
        elem = Element(tag)
        for key, val in d.items():
            # remove number id from mxCell and mxPoint
            if re.match(r"mxCell-\d+", key):
                key = "mxCell"
            elif re.match(r"mxPoint-\d+", key):
                key = "mxPoint"
            elif re.match(r"object-\d+", key):
                key = "object"

            if isinstance(val, dict):
                child = self.dict_to_xml(key, val)
                elem.append(child)
            elif isinstance(val, list):
                for sub_d in val:
                    child = self.dict_to_xml(key, sub_d)
                    elem.append(child)
            elif key == "text":  # Handle text content separately
                elem.text = etree.CDATA(val)  # Wrap text in CDATA if needed
            else:
                elem.set(key, val)
        return elem

    def json2xml(self, json_file_path, xml_file_path):
        """Convert JSON file to XML file."""
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            json_data = json_file.read()

        data = self.json_to_dict(json_data)

        root_tag = "mxfile"  # Adjust as needed based on data
        xml_root = self.dict_to_xml(root_tag, data)

        tree = ElementTree(xml_root)
        tree.write(
            xml_file_path, encoding="utf-8", xml_declaration=True, pretty_print=True
        )
        print("json to xml conversion success")

    @staticmethod
    def open_json(file_path):
        """_summary_

        Args:
            file_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
            return data_dict
