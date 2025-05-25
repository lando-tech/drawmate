class MxPoint:
    """_summary_"""

    def __init__(self) -> None:
        self.attributes = {
            "x": "",
            "y": "",
            "as": "",
        }
        self.waypoint_attributes = {
            "x": "",
            "y": "",
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

    def set_waypoint_x_y(self, x: int, y: int):
        self.waypoint_attributes["x"] = str(x)
        self.waypoint_attributes["y"] = str(y)
