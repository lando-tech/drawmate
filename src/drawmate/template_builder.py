import json
import os


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
            "tenth",
        ]

    def build_test_template(self):
        self.init_graph_dimensions(4000, 4000)
        self.init_matrices("Central Appliance", 200, 12)
        self.init_nodes_test(6)

    def create_template(self, file_path: str) -> bool:
        with open(file_path, "w") as new_template:
            json.dump(self.template_dict, new_template, indent=2)
            if os.path.isfile(file_path):
                return True
            else:
                return False

    def init_graph_dimensions(self, page_width, page_height):
        self.page_width = page_width
        self.page_height = page_height
        self.template_dict["graph-dimensions"] = {
            "dx": self.page_width,
            "dy": self.page_height,
            "width": self.page_width,
            "height": self.page_height,
        }

    def init_matrices(self, matrix_label, matrix_width, num_connections):
        self.num_connections = num_connections
        self.template_dict["matrices"] = {
            "labels": matrix_label,
            "width": matrix_width,
            "height": num_connections * 100,
            "x": self.page_width // 2,
            "y": self.page_height // 2,
            "num_connections": num_connections,
        }

        self.template_dict["connections-left"] = []
        self.template_dict["connections-right"] = []
        for i in range(self.num_connections):
            self.template_dict["connections-left"].append("NONE")
            self.template_dict["connections-right"].append("NONE")

    def init_nodes(self, num_columns):
        self.num_columns = num_columns
        if len(self.levels) < self.num_columns:
            raise IndexError(f"Number of columns cannot exceed {len(self.levels)}")

        for i in range(self.num_columns):

            self.template_dict[f"{self.levels[i]}-level-left"] = {"labels": []}
            for j in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-left"]["labels"].append(
                    ["", "", "", ["NONE"], ["NONE"]]
                )

            self.template_dict[f"{self.levels[i]}-level-right"] = {"labels": []}
            for k in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-right"]["labels"].append(
                    ["", "", "", ["NONE"], ["NONE"]]
                )

    def init_nodes_test(self, num_columns):
        self.num_columns = num_columns
        for i in range(self.num_columns):
            self.template_dict[f"{self.levels[i]}-level-left"] = {"labels": []}
            for j in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-left"]["labels"].append(
                    ["Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]]
                )

            self.template_dict[f"{self.levels[i]}-level-right"] = {"labels": []}
            for k in range(self.num_connections):
                self.template_dict[f"{self.levels[i]}-level-right"]["labels"].append(
                    ["Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]]
                )


def print_welcome_message():
    msg = (
        "\n\nWelcome to the drawmate template builder!\n"
        "This tool will guide you through building a basic JSON template for drawmate.\n"
        "Please follow the prompts below:\n"
    )
    print(msg)


def get_page_width_height() -> tuple[int, int]:
    width_verified: bool = False
    height_verified: bool = False
    page_width: int = 0
    page_height: int = 0
    while not width_verified:
        page_width = get_width()
        if page_width <= 0:
            page_width = get_width()
        else:
            width_verified = True

    while not height_verified:
        page_height = get_height()
        if page_height <= 0:
            page_height = get_height()
        else:
            height_verified = True

    return page_width, page_height


def get_width() -> int:
    page_width: int = 0
    try:
        page_width = int(input("Enter page width: "))
    except ValueError as e:
        print(f"Please enter a valid number! {e}")
        return 0

    return page_width


def get_height() -> int:
    page_height: int = 0
    try:
        page_height = int(input("Enter page height: "))
    except ValueError as e:
        print(f"Please enter a valid number! {e}")
        return 0

    return page_height


def get_columns_row() -> tuple[int, int]:
    columns_verified: bool = False
    rows_verified: bool = False
    columns: int = 0
    rows: int = 0
    while not columns_verified:
        columns = get_columns()
        if columns <= 0:
            columns = get_columns()
        else:
            columns_verified = True

    while not rows_verified:
        rows = get_rows()
        if rows <= 0:
            rows = get_rows()
        else:
            rows_verified = True

    return columns, rows


def get_columns() -> int:
    columns: int = 0
    try:
        columns = int(
            input(
                "Enter the number of columns (levels to span from the matrix, left/right): "
            )
        )
    except ValueError as e:
        print(f"Please enter a valid number: {e}")
        return 0

    return columns


def get_rows() -> int:
    rows: int = 0
    try:
        rows = int(
            input(
                "Enter number of connections for the matrix (this will be the total amount of rows): "
            )
        )
    except ValueError as e:
        print(f"Please enter a valid number: {e}")
        return 0

    return rows


def get_matrix_width() -> int:
    try:
        matrix_width: int = int(
            input(
                "Enter the desired width of the matrix (height is automatically calculated): "
            )
        )
    except ValueError as e:
        print(f"Please enter a valid number: {e}")
        return 0
    return matrix_width


def init_template_builder():
    template_builder = TemplateBuilder()
    print_welcome_message()

    try:
        page_width, page_height = get_page_width_height()
        num_columns, num_connections = get_columns_row()

        matrix_width = get_matrix_width()
        while matrix_width <= 0:
            matrix_width = get_matrix_width()

        matrix_label: str = input("Enter the name of the matrix/codec/switch: ")
        file_path: str = input("Enter file path for template: ")
        template_builder.init_graph_dimensions(page_width, page_height)
        template_builder.init_matrices(matrix_label, matrix_width, num_connections)
        template_builder.init_nodes(num_columns)

        if template_builder.create_template(file_path):
            print(f"File saved @ {file_path}")
            exit()
        else:
            print(
                "Oops! Something went wrong! Please check drawmate logs (~/.config/drawmate/logs)"
            )
            exit()
    except KeyboardInterrupt:
        print("\nExiting template builder! Goodbye!")
        exit()
