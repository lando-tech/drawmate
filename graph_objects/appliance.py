from graph_objects.rect import Rect
from constants.constants import MX_GRAPH_XML_STYLES, APPLIANCE_ATTRIBUTES_SC
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ApplianceMetadata:
    __ID__: str
    __SIDE__: str
    __ROW_INDEX__: Optional[int] = None
    __COLUMN_INDEX__: Optional[int] = None
    __MULTI_CONNECTION_LEFT__: bool = False
    __MULTI_CONNECTION_RIGHT__: bool = False
    __SPANNING_NODE__: bool = False
    __CONNECTION_INDEXES_LEFT__: List[int] = field(default_factory=list)
    __CONNECTION_INDEXES_RIGHT__: List[int] = field(default_factory=list)
    __LABEL_INDEXES__: List[int] = field(default_factory=list)
    __INPUT_LABELS__: List[str] = field(default_factory=list)
    __OUTPUT_LABELS__: List[str] = field(default_factory=list)


@dataclass
class Bounds:
    x: int
    y: int
    width: int
    height: int


class ApplianceSc(Rect):
    """
    Summary: This is child class of the Rect class. It inherits the attributes dictionary.
    This class manages the attributes of the appliances that will be attached to the matrix.

    Args:
        x (int): The X coord for the rect.
        y (int): The Y coord for the rect.
        style (str, optional): xml style for the graph element. Defaults to DEFAULT_STYLE.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    def __init__(
        self,
        x: int,
        y: int,
        label,
        input_label,
        output_label,
        width: int = APPLIANCE_ATTRIBUTES_SC["width"],
        height: int = APPLIANCE_ATTRIBUTES_SC["height"],
        input_label_array: list = None,
        output_label_array: list = None,
        mc_left: bool = False,
        mc_right: bool = False,
        left_ptr_array: list = None,
        right_ptr_array: list = None,
        style=DEFAULT_STYLE,
    ):
        super().__init__(
            x=x,
            y=y,
            style=style,
            label=label,
            _type="DTP",
            width=width,
            height=height,
        )
        self.x = x
        self.y = y
        self.left_ptr = None
        self.right_ptr = None
        self.input_label_array = input_label_array
        self.output_label_array = output_label_array
        self.mc_left = mc_left
        self.mc_right = mc_right
        self.left_ptr_array = left_ptr_array
        self.right_ptr_array = right_ptr_array
        self.input_label = input_label
        self.output_label = output_label

    def clear_label(self):
        """
        Reset the label as a blank string
        Returns:
        None
        """
        self.attributes["label"] = ""


class ApplianceMc(Rect):
    """
    Summary: This is child class of the Rect class. It inherits the attributes dictionary.
    This class manages the attributes of the appliances that will be attached to the matrix.

    Args:
        x (int): The X coord for the rect.
        y (int): The Y coord for the rect.
        label (str): Appliance label.
        input_label (str): label of appliance input port
        output_label (str): label of appliance output port
        meta (ApplianceMetadata): An instance of the ApplianceMetadata class
        width (int, optional): Appliance width
        height (int, optional): Appliance height
        style (str, optional): xml style for the graph element. Defaults to DEFAULT_STYLE.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    def __init__(
        self,
        x: int,
        y: int,
        label,
        input_label,
        output_label,
        meta: ApplianceMetadata,
        width: int = APPLIANCE_ATTRIBUTES_SC["width"],
        height: int = APPLIANCE_ATTRIBUTES_SC["height"],
        style=DEFAULT_STYLE,
    ):
        super().__init__(
            x=x,
            y=y,
            style=style,
            label=label,
            _type="DTP",
            width=width,
            height=height,
        )
        self.x = x
        self.y = y
        self.left_ptr = None
        self.right_ptr = None
        self.input_label = input_label
        self.output_label = output_label
        self.meta = meta

    def clear_label(self):
        """
        Reset the label as a blank string
        Returns:
        None
        """
        self.attributes["label"] = ""
