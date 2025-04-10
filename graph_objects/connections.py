from graph_objects.appliance import ApplianceSc, ApplianceMc
from graph_objects.matrix import Matrix
from graph_objects.arrow import Arrow, ArrowMeta, ArrowWaypoint
from constants.constants import MATRIX_CONNECTIONS


class ConnectionsSc:
    """
    Summary: Accepts an instance of a target and source rect, and manages the connections between the two objects.
    It also servers as a dispatcher for the Arrow class
    and adds an instance of the Arrow class between the source and target.

    Args:
        target_rect (Rect): An instance of a target Rect.
        source_rect (Rect): An instance of a source Rect.
        col_index   (int) : The current column index of the source/target rect
        left        (bool): If the object is on the left or right side
        mc          (bool): If the object has multiple connections
    """

    def __init__(
        self,
        source_rect: ApplianceSc | Matrix,
        target_rect: ApplianceSc | Matrix,
        col_index: int,
        left: bool,
        mc: bool = False,
    ):
        # y offset, default is set to center connection on object
        # this offset will place the connection on the IN/OUT label instead of the center of
        # the appliance
        self.src_center = source_rect.y + (
            int(source_rect.attributes.get("height")) // 2
        )
        self.tgt_center = target_rect.y + (
            int(target_rect.attributes.get("height")) // 2
        )
        if mc:
            self.offset = -40
        else:
            self.offset = 20

        self.source_x = int(source_rect.attributes["x"])
        self.target_x = int(target_rect.attributes["x"])

        if (col_index == 0 and left) or left:
            self.target_y = self.src_center + self.offset
            self.source_y = self.target_y
        elif col_index == 0:
            self.source_y = self.tgt_center + self.offset
            self.target_y = self.source_y
        else:
            self.source_y = self.src_center + self.offset
            self.target_y = self.source_y

    def create_connection(self, label: str, _type: str):
        """
        Returns an instance of the Arrow class
        Args:
            label (str): The label for the arrow
            _type (str): The type descriptor
        """
        arrow = Arrow(
            target_x=self.target_x,
            target_y=self.target_y,
            source_x=self.source_x,
            source_y=self.source_y,
            _type=_type,
            label=label,
        )
        return arrow


class ConnectionMc:
    """
    Summary: Accepts an instance of a target and source rect, and manages the connections between the two objects.
    It also servers as a dispatcher for the Arrow class
    and adds an instance of the Arrow class between the source and target.

    Args:
        tgt_node (ApplianceMc | Matrix): An instance of a target Rect.
        src_node (Appliance | Matrix): An instance of a source Rect.
    """

    def __init__(
        self,
        src_node: ApplianceMc | Matrix,
        tgt_node: ApplianceMc | Matrix,
    ):
        self.src_node = src_node
        self.tgt_node = tgt_node
        self.source_center = int(self.src_node.y) + (
            int(self.src_node.attributes["height"]) // 2
        )
        self.target_center = int(self.tgt_node.y) + (
            int(self.tgt_node.attributes["height"]) // 2
        )
        self.mx_points: list = []
        self.source_x = 0
        self.source_y = 0
        self.target_x = 0
        self.target_y = 0
        self.offset = 0

    def create_connection_sc(self) -> Arrow:
        """
        Adds the appropriate spacing for each arrow/connections based on the source
        and target attributes. If mc is passed to this function as True, it will then
        dispatch the add_x_y_spacing_mc function which handles the spacing of a
        multi-connection node.
        Args:

        Returns:

        """
        # y offset, default is set to center connection on object
        # this offset will place the connection on the IN/OUT label instead of the center of
        # the appliance

        self.offset = 20

        self.source_x = int(self.src_node.x)
        self.target_x = int(self.tgt_node.x)

        if isinstance(self.src_node, Matrix):
            self.target_y = self.target_center + self.offset
            self.source_y = self.target_y
        elif self.src_node.meta.__SIDE__ == "left":
            self.target_y = self.source_center + self.offset
            self.source_y = self.target_y
        elif self.src_node.meta.__COLUMN_INDEX__ == 0:
            self.target_y = self.target_center + self.offset
            self.source_y = self.target_y
        else:
            self.source_y = self.target_center + self.offset
            self.target_y = self.source_y

        return self.create_arrow_instance(label="", _type="arrow")

    def create_connection_mc(
        self, matrix_y: int, connection_index: int, pos_index: int
    ) -> Arrow | tuple[ArrowWaypoint, ArrowWaypoint, ArrowWaypoint]:
        """

        Args:
            pos_index:
            connection_index:
            matrix_y (int): The Y coordinate of an instance of the Matrix class

        Returns:

        """
        self.source_x = int(self.src_node.x)
        self.target_x = int(self.tgt_node.x)
        mc_offset = 50

        if isinstance(self.src_node, Matrix):
            connection_y = (
                (int(matrix_y) + MATRIX_CONNECTIONS["height"])
                + (MATRIX_CONNECTIONS["label_spacing"] * connection_index)
                + mc_offset
            )
            self.source_y = connection_y
            self.target_y = self.source_y
        elif isinstance(self.src_node, ApplianceMc):
            connection_y = (
                (int(matrix_y) + MATRIX_CONNECTIONS["height"])
                + (MATRIX_CONNECTIONS["label_spacing"] * connection_index)
                + mc_offset
            )
            if connection_index != self.src_node.meta.__LABEL_INDEXES__[pos_index]:
                mc_offset = 65
                return self.create_arrow_waypoints(
                    connection_index, pos_index, connection_y, mc_offset
                )

            elif self.src_node.meta.__SIDE__ == "left":
                self.target_y = connection_y
                self.source_y = self.target_y
            else:
                self.source_y = connection_y
                self.target_y = self.source_y

        return self.create_arrow_instance("", _type="arrow")

    def create_arrow_instance(self, label: str, _type: str):
        """
        Returns an instance of the Arrow class
        Args:
            label (str): The label for the arrow
            _type (str): The type descriptor
        """
        arrow = Arrow(
            target_x=self.target_x,
            target_y=self.target_y,
            source_x=self.source_x,
            source_y=self.source_y,
            _type=_type,
            label=label,
        )
        return arrow

    def create_arrow_waypoints(
        self, connection_index, pos_index, connection_y, mc_offset
    ) -> tuple[ArrowWaypoint, ArrowWaypoint, ArrowWaypoint] | None:
        """
        Generates and returns waypoints for drawing arrows between source and target nodes.

        The function calculates the midpoint and vertical points between
        the source and target nodes and constructs corresponding waypoints
        for arrows. Three different arrow paths are created: midpoint, vertical,
        and final connection. Each is defined using source and target coordinates
        and is generated via an internal arrow creation method. Debugging
        functionality is included to print relevant connection data.

        Args:
            connection_index (int): The index of the current connection for debug purposes.
            pos_index (int): The position index to identify where the arrow connects.
            connection_y (float): The vertical coordinate for the connection point on the target node.
            mc_offset (float): The offset added or applied to the y-coordinates of source node to
                define the connection path.

        Returns:
            tuple: A tuple containing three waypoint arrows, representing
                the midpoint, vertical, and final part of the connection.
        """
        meta = ArrowMeta(self.src_node.meta.__ID__, self.tgt_node.meta.__ID__)
        print(f"Source ID: {self.src_node.meta.__ID__} | Target ID: {self.tgt_node.meta.__ID__}")
        midpoint = self.get_x_coord_midpoint(self.tgt_node.x, self.src_node.x)
        midpoint_waypoints = {
            "x": self.src_node.x,
            "y": self.src_node.y + mc_offset
        }
        vertical_waypoints = {
            "x": self.src_node.x + midpoint,
            "y": connection_y,
        }
        final_point_waypoints = {
            "x": self.tgt_node.x,
            "y": connection_y,
        }
        midpoint_arrow = self.create_arrow_break(
            midpoint_waypoints["x"],
            midpoint_waypoints["y"],
            meta=meta,
        )
        vertical_arrow = self.create_arrow_break(
            vertical_waypoints["x"],
            vertical_waypoints["y"],
        )
        final_arrow = self.create_arrow_break(
            final_point_waypoints["x"],
            final_point_waypoints["y"],
        )
        self.debug_print(connection_index, pos_index, connection_y)
        return midpoint_arrow, vertical_arrow, final_arrow

    def debug_print(self, connection_index, pos_index, connection_y):
        print("\n")
        print("\t=======================================")
        print(f"\tSource Node      : {self.src_node.attributes.get('label')}")
        print(f"\tSource Column    : {self.src_node.meta.__COLUMN_INDEX__}")
        print(f"\tSource Row       : {self.src_node.meta.__ROW_INDEX__}")
        print(f"\tSource X         : {self.src_node.x}")
        print(f"\tSource Y         : {self.src_node.y}")
        print(f"\tLabel Index      : {self.src_node.meta.__LABEL_INDEXES__[pos_index]}")
        print("\t=======================================")
        print(f"\tConnection Index : {connection_index}")
        print(f"\tConnection Y     : {connection_y}")
        print("\t=======================================")
        print(f"\tTarget Node      : {self.tgt_node.attributes.get('label')}")
        print(f"\tTarget Y         : {self.tgt_node.y}")
        print(f"\tTarget X         : {self.tgt_node.x}")
        print(f"\tMidpoint         : {self.target_x}")
        print("\t=======================================")

    @staticmethod
    def create_arrow_break(x, y, meta=None) -> ArrowWaypoint:
        waypoint = ArrowWaypoint(
            x=x,
            y=y,
            meta=meta,
        )
        return waypoint

    @staticmethod
    def get_x_coord_midpoint(src_x, tgt_x):
        x_offset = 80
        return (src_x - tgt_x) // 2 + x_offset
