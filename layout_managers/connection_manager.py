from graph_objects.arrow import Arrow, ArrowWaypoint, ArrowMeta


class ConnectionManager:
    def __init__(self):
        pass

    def add_connection(self, connection_data: dict) -> Arrow:
        return Arrow(
            target_x=connection_data["target-x"],
            target_y=connection_data["target-y"],
            source_x=connection_data["source-x"],
            source_y=connection_data["source-y"],
            label=connection_data["label"],
            _type=connection_data["connection-type"],
            style=connection_data["style"]
        )

    def add_connection_waypoint(self, x: int, y: int, waypoint_meta: ArrowMeta = None) -> ArrowWaypoint:
        return ArrowWaypoint(
            x=x,
            y=y,
            meta=waypoint_meta
        )

    def calculate_connection_x(self):
        pass

    def calculate_connection_y(self):
        pass

    def calculate_waypoints(self):
        pass