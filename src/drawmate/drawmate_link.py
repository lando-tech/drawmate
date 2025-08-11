class DrawmateLink:
    def __init__(self, source_id: str, target_id: str) -> None:
        self.id: str
        self.source_id = source_id
        self.target_id = target_id
        self.source_x: float
        self.source_y: float
        self.target_x: float
        self.target_y: float
        self.waypoints: list[DrawmateLink] = []
