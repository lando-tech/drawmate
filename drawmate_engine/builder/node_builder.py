from graph_objects.appliance import Appliance, ApplianceMetadata


class NodeBuilder:
    def __init__(self):
        self.node_dict: dict[str, Appliance] = dict()

    def init_node_meta(self, attrib_dict: dict) -> ApplianceMetadata:
        pass

    def init_node_dict(self) -> None:
        pass