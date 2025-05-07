import json
from dataclasses import dataclass

from constants.matrix_constants import MatrixDimensions
from utils.pathfinder import PathFinder
from utils.log_manager import LogManager


pf = PathFinder()


@dataclass
class GraphDimensions:
    dx: int
    dy: int
    width: int
    height: int


class DrawmateConfig:

    def __init__(self, template_path: str):
        self.template_path = template_path
        self.pf = PathFinder()
        self.log_mgr = LogManager()
        self.template_data = self.load_template()

    def load_template(self) -> dict | None:
        try:
            with open(self.template_path, "r", encoding="utf-8") as template_file:
                return json.load(template_file)
        except FileNotFoundError:
            log_data = f"Template file not found: {self.template_path}\n"
            self.log_mgr.add_log(
                object_log="drawmate",
                message=log_data,
                line_number="460",
                is_error=True,
                is_warning=False,
            )
            return None
        except json.JSONDecodeError as json_error:
            log_data = (
                f"Invalid JSON in template file: {self.template_path}\n"
                + f"Json error: {json_error}"
            )
            self.log_mgr.add_log(
                object_log="drawmate",
                message=log_data,
                line_number="468",
                is_error=True,
                is_warning=False,
            )
            return None

    def get_graph_dimensions(self) -> GraphDimensions | None:
        if not self.template_data:
            return None
        dimensions = self.template_data.get("graph-dimensions")

        if not dimensions:
            return None

        return GraphDimensions(
            dimensions["dx"],
            dimensions["dy"],
            dimensions["width"],
            dimensions["height"],
        )

    def get_matrix_dimensions(self) -> MatrixDimensions | None:

        if not self.template_data:
            return None

        dimensions = self.template_data.get("matrices")

        if not dimensions:
            return None

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

    def build_node_dict(self, num_connections: int):
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
                    for label in value["labels"]:
                        if row_index_left >= num_connections:
                            row_index_left = 0
                        object_key = f"{col_index_left}-{row_index_left}"
                        left_side[object_key] = label
                        row_index_left += 1
                    col_index_left += 1
                elif (
                    current_level == levels[col_index_right] and current_side == "right"
                ):
                    for label in value["labels"]:
                        if row_index_right >= num_connections:
                            row_index_right = 0
                        object_key = f"{col_index_right}-{row_index_right}"
                        right_side[object_key] = label
                        row_index_right += 1
                    col_index_right += 1

            return left_side, right_side
        else:
            return None

    def get_matrix_connection_labels(self) -> tuple[list, list]:
        return self.template_data.get("connections-left"), self.template_data.get(
            "connections-right"
        )

    def get_matrix_label(self):
        return self.template_data.get("matrices")["labels"]
