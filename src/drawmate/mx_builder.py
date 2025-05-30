from .mxcell import MxCell
from .mxgeometry import MxGeometry
from xml.dom.minidom import Element

from .mxpoint import MxPoint


class MxBuilder:
    """
    This is the top-level class for the templating engine.
    It contains the core logic for building the XML document.
    The caller is responsible for appending each cell to the
    document root.
    """

    def create_mxcell(
        self,
        data: dict,
        __id__: str = "",
        has_label: bool = True,
    ) -> Element:
        """
        Creates an Mxcell element with geometry.

        Args:
            data (dict): Dictionary containing cell attributes.
            __id__ (str): Unique identifier for the cell. Must be unique across all elements.
            has_label (bool, optional): Whether to include the label. Defaults to True.

        Returns:
            Element | None: The created MX cell element, or None if creation fails

        Note:
            The caller must manually append the created element to the document root.
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

        return cell_elem
    
    def create_mxcell_with_target(self, attributes: dict, __id__:str, source_id: str, target_id: str, has_label: bool = False):
        cell = MxCell()
        if not has_label:
            cell.set_mxcell_values_point(value="", style=attributes["style"], __id__=__id__, src_id=source_id, tgt_id=target_id)
        else:
            cell.set_mxcell_values_point(
               style=attributes["style"], value=attributes["label"], __id__= __id__, src_id=source_id, tgt_id=target_id
            )
        # Append mxCell to mxObject
        cell_elem = cell.create_xml_element("mxCell", cell.attributes)
        cell.mxcell_object.appendChild(cell_elem)

        # Create mxGeometry object
        # geo = MxGeometry()
        # geo.set_geometry_values(attributes["x"], attributes["y"], attributes["width"], attributes["height"])

        # # Append mxGeometry to mxCell
        # geo_elem = cell.create_xml_element("mxGeometry", geo.attributes)
        # cell_elem.appendChild(geo_elem)

        return cell_elem       

    def create_mxcell_arrow(
        self, data: dict, __id__: str = ""
    ) -> Element:
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

        # Create mxPoint objects and append to mxGeometry
        mx_points = self.create_mxpoint(mxcell_obj=cell, data=data)
        geo_elem.appendChild(mx_points[0])
        geo_elem.appendChild(mx_points[1])

        return cell_elem

    def create_mxpoint(self, mxcell_obj, data: dict) -> tuple[Element, Element]:
        """
        Creates source and target point elements for an MX cell.

        Args:
            mxcell_obj (MxCell): The Mxcell object to create points for
            data (dict): Dictionary containing point coordinates
        Returns:
            tuple[Element, Element] | None: A tuple containing (source_point, target_point) elements,
                or None if creation fails
        """
        # Set source mxPoint element
        source_point = MxPoint()
        source_point.set_mxpoint_source(data["source_x"], data["source_y"])
        source_element = mxcell_obj.create_xml_element(
            "mxPoint", source_point.attributes
        )

        # Set target for mxPoint element
        target_point = MxPoint()
        target_point.set_mxpoint_target(data["target_x"], data["target_y"])
        target_element = mxcell_obj.create_xml_element(
            "mxPoint", target_point.attributes
        )
        return source_element, target_element

