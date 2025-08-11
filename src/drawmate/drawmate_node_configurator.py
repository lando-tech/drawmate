from drawmate.drawmate_node import DrawmateNode
from drawmate.drawmate_spacing_manager import DrawmateSpacingManager


class DrawmateNodeConfigurator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def configure_node_left(
        __id__,
        base_y,
        column_count,
        node: DrawmateNode,
        spacing_mgr: DrawmateSpacingManager,
    ):
        node.id = __id__
        node.height = spacing_mgr.get_node_height(len(node.ports_input))
        node.width = spacing_mgr.node_width
        node.x = spacing_mgr.get_node_x_left(column_count)
        node.y = base_y

    @staticmethod
    def configure_node_right(
        __id__,
        base_y,
        column_count,
        node: DrawmateNode,
        spacing_mgr: DrawmateSpacingManager,
    ):
        node.id = __id__
        node.height = spacing_mgr.get_node_height(len(node.ports_input))
        node.width = spacing_mgr.node_width
        node.x = spacing_mgr.get_node_x_right(column_count)
        node.y = base_y
