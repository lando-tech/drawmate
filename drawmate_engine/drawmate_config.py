import json
from dataclasses import dataclass
from typing import Optional

from utils.pathfinder import PathFinder
from utils.log_manager import LogManager


pf = PathFinder()


@dataclass
class GraphDimensions:
    dx: int
    dy: int
    width: int
    height: int


@dataclass
class MatrixDimensions:
    labels: str
    width: int
    height: int
    x: int
    y: int
    num_connections: int


class DrawmateConfig:

    def __init__(self, template_path: str):
        self.template_path = template_path
        self.pf = PathFinder()
        self.log_mgr = LogManager()
        self.template_data = self.load_template()

    def load_template(self) -> Optional[dict]:
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

    def get_graph_dimensions(self) -> Optional[GraphDimensions]:
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

    def get_matrix_dimensions(self) -> Optional[MatrixDimensions]:

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

    def build_matrix_array(self) -> tuple[list, list]:
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

    def get_matrix_connection_labels(self) -> tuple[list, list]:
        return self.template_data.get("connections-left"), self.template_data.get(
            "connections-right"
        )

    def get_matrix_label(self):
        return self.template_data.get("matrices")["labels"]
