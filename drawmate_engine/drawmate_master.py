from xml.dom.minidom import Element

from drawmate_engine.drawmate_config import DrawmateConfig
from graph_objects.matrix import Matrix
from builder.matrix_builder import MatrixBuilder
from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder
from graph_objects.text_box import TextBox


class DrawmateMaster(DocBuilder, MxBuilder):
    def __init__(self, matrix_builder: MatrixBuilder):
        super().__init__()
        self.matrix_builder: MatrixBuilder = matrix_builder

    def draw_matrix(self):
        matrix_obj: Matrix = self.matrix_builder.init_matrix()
        matrix_elem: Element = self.create_mxcell(
            data=matrix_obj.attributes, __id__=matrix_obj.meta.__ID__, has_label=False
        )
        self.root.appendChild(matrix_elem)

    def draw_matrix_label(self):
        matrix_label: TextBox = self.matrix_builder.init_matrix_label()
        matrix_label_elem: Element = self.create_mxcell(data=matrix_label.attributes)
        self.root.appendChild(matrix_label_elem)

    def draw_matrix_ports(self, spacing: int, connection_labels: tuple[list, list]):
        matrix_ports: list[TextBox] = self.matrix_builder.init_matrix_ports(
            spacing=spacing,
            connection_labels=connection_labels
        )
        for port in matrix_ports:
            self.root.appendChild(self.create_mxcell(data=port.attributes))

if __name__ == "__main__":
    dc = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
    matrix_builder: MatrixBuilder = MatrixBuilder(dc.get_matrix_dimensions())
    dm = DrawmateMaster(matrix_builder)
    dm.draw_matrix()
    dm.draw_matrix_label()
    dm.draw_matrix_ports(120, dc.get_matrix_connection_labels())
    dm.create_xml("/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml")