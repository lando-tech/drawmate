from graph_objects.text_box import TextBox


class Port(TextBox):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x=x, y=y, width=width, height=height, label="", _type="port")
        self.input_label: str = ""
        self.output_label: str = ""
        self.id: str = ""
