from xml.dom.minidom import Element

from drawmate_engine.drawmate_config import DrawmateConfig, MatrixDimensions
from graph_objects.matrix import Matrix
from builder.matrix_builder import MatrixBuilder
from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder
from graph_objects.text_box import TextBox

dc: DrawmateConfig = DrawmateConfig("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
mx_builder: MxBuilder = MxBuilder()
doc_builder: DocBuilder = DocBuilder()

matrix_dims: MatrixDimensions = dc.get_matrix_dimensions()
matrix_builder: MatrixBuilder = MatrixBuilder(matrix_dimensions=matrix_dims)
matrix: Matrix = matrix_builder.init_matrix()
matrix_label: TextBox = matrix_builder.init_matrix_label()

matrix_cell_elem: Element = mx_builder.create_mxcell(data=matrix.attributes, __id__=matrix.meta.__ID__, has_label=False)
matrix_label_elem: Element = mx_builder.create_mxcell(data=matrix_label.attributes)

doc_builder.root.appendChild(matrix_cell_elem)
doc_builder.root.appendChild(matrix_label_elem)
doc_builder.create_xml("/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml")
