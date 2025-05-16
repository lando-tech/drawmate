from graph_objects.rect import Rect
from constants.constants import MX_GRAPH_XML_STYLES
from constants.node_constants import NodeAttributes
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(slots=True)
class NodeMetaData:
    __ID__: str
    __SIDE__: str
    __LABEL__: str = None
    __ROW_INDEX__: Optional[int] = None
    __COLUMN_INDEX__: Optional[int] = None
    __MULTI_CONNECTION_LEFT__: bool = False
    __MULTI_CONNECTION_RIGHT__: bool = False
    __SPANNING_NODE__: bool = False
    __INPUT_LABEL__: str = None
    __OUTPUT_LABEL__: str = None
    __INPUT_LABEL_ARRAY__: List[str] = field(default_factory=list)
    __OUTPUT_LABEL_ARRAY__: List[str] = field(default_factory=list)
    __CONNECTION_INDEXES_LEFT__: List[int] = field(default_factory=list)
    __CONNECTION_INDEXES_RIGHT__: List[int] = field(default_factory=list)
    __LABEL_INDEXES__: List[int] = field(default_factory=list)


class Node(Rect):
    """
    Summary: This is the child class of the Rect class. This class inherits the attributes dictionary.
    This class manages the attributes of the appliances that will be attached to the matrix.

    Args:
        x (int): The X coord for the rect.
        y (int): The Y coord for the rect.
        label (str): Appliance label.
        input_label (str): label of appliance input port
        output_label (str): label of appliance output port
        meta (NodeMetaData): An instance of the ApplianceMetadata class
        width (int, optional): Appliance width
        height (int, optional): Appliance height
        style (str, optional): XML style for the graph element. Defaults to DEFAULT_STYLE.
    """

    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["rect"]

    def __init__(
        self,
        x: int,
        y: int,
        label,
        input_label,
        output_label,
        meta: NodeMetaData = None,
        width: int = NodeAttributes.width,
        height: int = NodeAttributes.height,
        style=DEFAULT_STYLE,
    ):
        super().__init__(
            x=x,
            y=y,
            style=style,
            label=label,
            _type="node",
            width=width,
            height=height,
        )
        # self.x, self.y are reference only, mutate only the attributes["x"], attributes["y"]
        self.x = int(self.attributes["x"])
        self.y = int(self.attributes["y"])
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
