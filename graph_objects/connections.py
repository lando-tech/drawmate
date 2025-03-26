from graph_objects.appliance import Appliance
from graph_objects.matrix import Matrix
from graph_objects.arrow import Arrow
from constants.constants import MATRIX_CONNECTIONS


class Connection:
    """
    Summary: Accepts an instance of a target and source rect, and manages the connections between the two objects.
    It also servers as a dispatcher for the Arrow class
    and adds an instance of the Arrow class between the source and target.

    Args:
        tgt_node (Appliance | Matrix): An instance of a target Rect.
        src_node (Appliance | Matrix): An instance of a source Rect.
    """

    def __init__(
        self,
        src_node: Appliance | Matrix,
        tgt_node: Appliance | Matrix,
    ):
        self.src_node = src_node
        self.tgt_node = tgt_node
        self.source_center = int(self.src_node.y) + (
                int(self.src_node.attributes["height"]) // 2
        )
        self.target_center = int(self.tgt_node.y) + (
                int(self.tgt_node.attributes["height"]) // 2
        )
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
        elif self.src_node.meta.__SIDE__ == 'left':
            self.target_y = self.source_center + self.offset
            self.source_y = self.target_y
        elif self.src_node.meta.__COLUMN_INDEX__ == 0:
            self.target_y = self.target_center + self.offset
            self.source_y = self.target_y
        else:
            self.source_y = self.target_center + self.offset
            self.target_y = self.source_y

        return self.create_arrow_instance(label="", _type="arrow")

    def create_connection_mc(self, matrix_y: int, connection_index: int) -> Arrow:
        """

        Args:
            connection_index:
            matrix_y (int): The Y coordinate of an instance of the Matrix class

        Returns:

        """
        self.source_x = int(self.src_node.x)
        self.target_x = int(self.tgt_node.x)
        threshold = 220
        mc_offset = 50

        if isinstance(self.src_node, Matrix):
            connection_y = (
                    (int(matrix_y) + MATRIX_CONNECTIONS["height"])
                    + (MATRIX_CONNECTIONS["label_spacing"] * connection_index)
                    + mc_offset
            )
            self.source_y = connection_y
            self.target_y = self.source_y
        else:
            connection_y = (
                    (int(matrix_y) + MATRIX_CONNECTIONS["height"])
                    + (MATRIX_CONNECTIONS["label_spacing"] * connection_index)
                    + mc_offset
            )

            if connection_y - self.src_node.y > threshold:
                # print("\n")
                # print(f"\tConnection Y: {connection_y}\n"
                #       f"\tSource Y    : {self.src_node.y}\n"
                #       f"\tSource Node : {self.src_node.attributes.get('label')}\n"
                #       f"\tSource Column: {self.src_node.meta.__COLUMN_INDEX__}\n"
                #       f"\tSource Row   : {self.src_node.meta.__ROW_INDEX__}\n"
                #       f"\tTarget Y    : {self.tgt_node.y}\n"
                #       f"\tTarget Node : {self.tgt_node.attributes.get('label')}\n")
                self.source_y = self.src_node.y + mc_offset
                self.target_y = connection_y

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
