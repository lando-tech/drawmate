import json



class TemplateBuilder:
    def __init__(self) -> None:
        self.template_dict: dict = {}
        self.page_width: int = 0
        self.page_height: int = 0
        self.matrix_label: str = ""
        self.matrix_width: int = 0
        self.num_connections: int = 0
        self.num_columns: int = 0
        self.levels = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth"
        ]

    def create_template(self, file_path: str):
        with open(file_path, "w") as new_template:
            json.dump(self.template_dict, new_template, indent=2)

    def init_graph_dimensions(self, page_width, page_height):
        self.page_width = page_width
        self.page_height = page_height
        self.template_dict["graph-dimensions"] = {
            "dx": self.page_width,
            "dy": self.page_height,
            "width": self.page_width,
            "height": self.page_height
        }
    
    def init_matrices(self, matrix_label, matrix_width, num_connections):
        self.num_connections = num_connections
        self.template_dict["matrices"] = {
            "labels": matrix_label,
            "width": matrix_width,
            "x": self.page_width // 2,
            "y": self.page_height // 2,
            "num_connections": num_connections,
        }
        for i in range(self.num_connections):
            self.template_dict["connections-left"] = []
            self.template_dict["connections-right"] = []
            self.template_dict["connections-left"].append("")
            self.template_dict["connections-right"].append("")
    
    def init_nodes(self, num_columns):
        self.num_columns = num_columns
        if len(self.levels) < self.num_columns:
            raise IndexError(f"Number of columns cannot exceed {len(self.levels)}")

        for i in range(self.num_columns):

            self.template_dict[f"{self.levels[i]}-level-left"] = []
            for i in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-left"].append(["", "", "", ["NONE"], ["NONE"]])

            self.template_dict[f"{self.levels[i]}-level-right"] = []
            for i in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-right"].append(["", "", "", ["NONE"], ["NONE"]])


if __name__ == "__main__":
    template_builder = TemplateBuilder()
    page_width: int = int(input("Enter page width: "))
    page_height: int = int(input("Enter page height: "))
    num_connections: int = int(input("Enter number of connections for the matrix (this will be the total amount of rows): "))
    num_columns: int = int(input("Enter the number of columns(levels to span from the matrix): "))
    matrix_label: str = input("Enter the name of the matrix/codec/switch: ")
    matrix_width: int = int(input("Enter the desired width of the matrix (height is automatically calculated): "))
    file_path: str = input("Enter file path for template: ")
    template_builder.init_graph_dimensions(page_width, page_height)
    template_builder.init_matrices(matrix_label, matrix_width, num_connections)
    template_builder.init_nodes(num_columns)
    template_builder.create_template(file_path)