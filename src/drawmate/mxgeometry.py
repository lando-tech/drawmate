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

        def set_waypoint_source(self, x: int, y: int):
            self.attributes["x"] = str(x)
            self.attributes["y"] = str(y)

        def set_waypoint_target(self, x: int, y: int):
            self.attributes["x"] = str(x)
            self.attributes["y"] = str(y)
