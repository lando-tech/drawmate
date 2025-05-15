from constants.constants import MX_GRAPH_XML_STYLES
from graph_objects.matrix import Matrix
from graph_objects.node import Node
from graph_objects.text_box import TextBox


class Port(TextBox):
    DEFAULT_STYLE = MX_GRAPH_XML_STYLES["text-box"]
    def __init__(self, x: int, y: int, width: int, height: int, parent: Node | Matrix, label: str, style: str = DEFAULT_STYLE):
        super().__init__(x=x, y=y, width=width, height=height, label=label, _type="port", style=style)
        self.id: str = ""
        self.parent: Node | Matrix = parent
        self.x: int = int(self.attributes["x"])
        self.y: int = int(self.attributes["y"])
        self.width: int = int(self.attributes["width"])
        self.height: int = int(self.attributes["height"])
