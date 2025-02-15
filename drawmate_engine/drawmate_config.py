import json
from dataclasses import dataclass
from typing import Optional

from drawmate_engine.doc_builder import create_document, MxObject
from drawmate_engine.matrix import Rect, Matrix, Dtp, Connections, TextBox
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

    def get_connections_count(self) -> Optional[int]:
        if not self.template_data:
            return None

        return len(self.template_data.get("connections-left"))

    def get_rect_labels(
        self, appliance_type: str, level: int = 0
    ) -> Optional[list[str]] or Optional[tuple[list[str], list[str]]]:
        """

        Args:
            appliance_type: matrix, dtp
            level: which level on the graph to retrieve labels for

        Returns:

        """
        if not self.template_data:
            return None

        if appliance_type == "matrix":
            return self.template_data.get("connections-left"), self.template_data.get(
                "connections-right"
            )
        elif appliance_type == "dtp" and level != 0:
            if level == 1:
                return (
                    self.template_data["first-level-left"]["labels"]
                    + self.template_data["first-level-right"]["labels"]
                )
            elif level == 2:
                return (
                    self.template_data["second-level-left"]["labels"]
                    + self.template_data["second-level-right"]["labels"]
                )
            elif level == 3:
                return (
                    self.template_data["third-level-left"]["labels"]
                    + self.template_data["third-level-right"]["labels"]
                )
        else:
            return None

    def get_rect_labels_as_tuple(self, level: int = 0):
        """ """
        if level == 0:
            return None
        elif level == 1:
            return (
                self.template_data["first-level-left"]["labels"],
                self.template_data["first-level-right"]["labels"],
            )
        elif level == 2:
            return (
                self.template_data["second-level-left"]["labels"],
                self.template_data["second-level-right"]["labels"],
            )
        elif level == 3:
            return (
                self.template_data["third-level-left"]["labels"],
                self.template_data["third-level-right"]["labels"],
            )
