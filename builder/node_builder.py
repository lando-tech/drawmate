from graph_objects.appliance import Appliance, ApplianceMetadata
from graph_objects.rect import Rect
from constants.constants import APPLIANCE_ATTRIBUTES, APPLIANCE_INPUT_OUTPUT_DIMS, APPLIANCE_INPUT, APPLIANCE_OUTPUT
from graph_objects.text_box import TextBox


class NodeBuilder:
    def __init__(self, appliance_meta: ApplianceMetadata):
        self.meta = appliance_meta

    def init_node(self, node_attributes: dict) -> Appliance:
        x = node_attributes["x"]
        y = node_attributes["y"]
        label = node_attributes["label"]
        input_label = node_attributes["input_labels"]
        output_label = node_attributes["output_labels"]
        width = node_attributes["width"]
        height = node_attributes["height"]
        return Appliance(
            x=x,
            y=y,
            label=label,
            input_label=input_label,
            output_label=output_label,
            width=width,
            height=height,
            meta=self.meta,
        )

    def init_node_label(self, node: Appliance):
        return Rect(
            x=node.x,
            y=node.y,
            width=node.attributes["width"],
            height=APPLIANCE_ATTRIBUTES["label_height"],
            label=node.attributes["label"],
            _type="text-box"
        )

    def init_node_input(self, x: int, y: int, label: str):
        input_x, input_y = self.calculate_input_offset(x, y)
        return TextBox(
            x=input_x,
            y=input_y,
            width=APPLIANCE_INPUT_OUTPUT_DIMS["width"],
            height=APPLIANCE_INPUT_OUTPUT_DIMS["height"],
            label=label,
            _type="text-box"
        )

    def init_node_output(self, x: int, y: int, label: str):
        output_x, output_y = self.calculate_output_offset(x, y)
        return TextBox(
            x=output_x,
            y=output_y,
            width=APPLIANCE_INPUT_OUTPUT_DIMS["width"],
            height=APPLIANCE_INPUT_OUTPUT_DIMS["height"],
            label=label,
            _type="text-box"
        )

    @staticmethod
    def calculate_input_offset(x: int, y: int) -> tuple[int, int]:
        x = x + APPLIANCE_INPUT["x_offset"]
        y = y + APPLIANCE_INPUT["y_offset"]
        return x, y

    @staticmethod
    def calculate_output_offset(x: int, y: int) -> tuple[int, int]:
        x = x + 100
        y = y + APPLIANCE_OUTPUT["y_offset"]
        return x, y
