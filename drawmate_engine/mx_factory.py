from graph_objects.arrow import Arrow
from mx_graph_api.mxcell import MxCell
from mx_graph_api.mxgeometry import MxGeometry
from mx_graph_api.mxpoint import MxPoint
from doc_builder import generate_id
from xml.dom.minidom import Element


class MxFactory:
    """
    This is the top-level class for the templating engine.
    It contains the core logic for building the XML document.
    """

    def create_mxcell(
        self,
        data: dict = None,
        __id__: str = "",
        has_label: bool = True,
    ) -> Element | None:
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

        return cell_elem

    def create_mxcell_arrow(self, data: dict = None, __id__: str = "") -> Element | None:
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

    def create_mxpoint(self, mxcell_obj, data: dict) -> tuple[Element, Element] | None:
        """
        Summary:
            Creates the XML structure for and instantiates the mxPoint object.

        Args:
            mxcell_obj (mxObject): An instance of the mxObject class.
            data (dict): An attribute dictionary from the instance of the Arrow class.
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
        target_element = mxcell_obj.create_xml_element("mxPoint", target_point.attributes)
        return source_element, target_element

    def create_mxarray(self, mx_points: tuple[Arrow]) -> list[Element] | None:
        elements = []
        for index, waypoint in enumerate(mx_points):
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
            elements.append(cell_elem)

        return elements
