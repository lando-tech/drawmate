import json
from dataclasses import dataclass

from .matrix_constants import MatrixDimensions
# from pathfinder import PathFinder
# from log_manager import LogManager


# pf = PathFinder()


@dataclass
class GraphDimensions:
    dx: int
    dy: int
    width: int
    height: int


class DrawmateConfig:

    def __init__(self, template_path: str):
        self.template_path = template_path
        # self.pf = PathFinder()
        # self.log_mgr = LogManager()
        self.template_data = self.load_template()
        self.num_levels = 0

    def load_template(self) -> dict:
        try:
            with open(self.template_path, "r", encoding="utf-8") as template_file:
                return json.load(template_file)
        except FileNotFoundError:
            # log_data = f"Template file not found: {self.template_path}\n"
            # self.log_mgr.add_log(
            #     object_log="drawmate",
            #     message=log_data,
            #     line_number="460",
            #     is_error=True,
            #     is_warning=False,
            # )
            exit("Failed to find template file")
        except json.JSONDecodeError:
            # log_data = (
            #     f"Invalid JSON in template file: {self.template_path}\n"
            #     + f"Json error: {json_error}"
            # )
            # self.log_mgr.add_log(
            #     object_log="drawmate",
            #     message=log_data,
            #     line_number="468",
            #     is_error=True,
            #     is_warning=False,
            # )
            exit("Failed to parse JSON template!")

    def get_graph_dimensions(self) -> GraphDimensions:

        if not self.template_data:
            exit("Failed to load template file: get_graph_dimensions()")
        dimensions = self.template_data.get("graph-dimensions")

        if not dimensions:
            exit("Failed to fetch graph dimensions: get_graph_dimensions()")

        return GraphDimensions(
            dimensions["dx"],
            dimensions["dy"],
            dimensions["width"],
            dimensions["height"],
        )

    def get_matrix_dimensions(self) -> MatrixDimensions:

        if not self.template_data:
            exit("Failed to load template file: get_matrix_dimensions()")

        dimensions = self.template_data.get("matrices")

        if not dimensions:
            exit("Failed to fetch matrix dimensions: get_matrix_dimensions()")

        return MatrixDimensions(
            dimensions["labels"],
            dimensions["width"],
            dimensions["height"],
            dimensions["x"],
            dimensions["y"],
            dimensions["num_connections"],
        )

    def build_matrix_array(self) -> tuple[list[list], list[list]] | None:
        left_side = []
        right_side = []
        levels = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
        ]
        if self.template_data:
            for level in levels:
                for key, value in self.template_data.items():
                    current_key = key.split("-")
                    current_level = current_key[0]
                    current_side = current_key[-1]

                    if current_level == level and current_side == "left":
                        left_side.append(list(value["labels"]))
                    elif current_level == level and current_side == "right":
                        right_side.append(list(value["labels"]))

            return left_side, right_side
        else:
            return None

    def build_node_dict(self, num_connections: int) -> tuple[dict[str, list[str] | str], dict[str, list[str] | str]]:
        left_side = {}
        right_side = {}
        levels = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
        ]
        col_index_left = 0
        row_index_left = 0
        col_index_right = 0
        row_index_right = 0
        if self.template_data:
            for key, value in self.template_data.items():
                current_key = key.split("-")
                current_level = current_key[0]
                current_side = current_key[-1]

                if current_level == levels[col_index_left] and current_side == "left":
                    self.num_levels += 1
                    for label in value["labels"]:
                        if row_index_left >= num_connections:
                            row_index_left = 0
                        object_key = f"L-{col_index_left}-{row_index_left}"
                        left_side[object_key] = label
                        row_index_left += 1
                    col_index_left += 1
                elif (
                    current_level == levels[col_index_right] and current_side == "right"
                ):
                    for label in value["labels"]:
                        if row_index_right >= num_connections:
                            row_index_right = 0
                        object_key = f"R-{col_index_right}-{row_index_right}"
                        right_side[object_key] = label
                        row_index_right += 1
                    col_index_right += 1

            return left_side, right_side
        else:
            exit("Failed to load template file: build_node_dict()")

    def get_matrix_connection_labels(self) -> tuple[list, list]:
        return self.template_data.get("connections-left"), self.template_data.get(
            "connections-right"
        ) # type: ignore

    def get_matrix_label(self):
        return self.template_data.get("matrices")["labels"] # type: ignore
