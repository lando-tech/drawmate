from .drawmate_link import DrawmateLink
class DrawmatePort:
    def __init__(
            self,
            label: str,

    ) -> None:
        self.label = label
        self.width: float = 0
        self.height: float = 0
        self.link: DrawmateLink
        self.x: float = 0
        self.y: float = 0
