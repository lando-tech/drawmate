
class DrawmateLink:
    def __init__(self, source_id: str, target_id: str) -> None:
        self.id: str
        self.source_id = source_id
        self.target_id = target_id
        self.waypoints: list[DrawmateLink] = []
