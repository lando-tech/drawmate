from graph_objects.appliance import Appliance, ApplianceMetadata
from constants.constants import APPLIANCE_ATTRIBUTES_SC


class NodeBuilder:
    def __init__(self, appliance_meta: ApplianceMetadata):
        self.meta = appliance_meta

    def init_node(self, node_attributes: dict) -> Appliance:
        x = node_attributes["x"]
        y = node_attributes["y"]
        label = node_attributes["label"]
        input_label = node_attributes["left_labels"]
        output_label = node_attributes["right_labels"]
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

    def init_node_label(self):
        pass
