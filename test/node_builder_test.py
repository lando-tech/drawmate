from builder.node_builder import NodeBuilder
from builder.doc_builder import generate_id
from graph_objects.appliance import ApplianceMetadata
from test.builder_test import BuilderTest

input_test_file = "/home/landotech/easyrok/drawmate/test/mc_test_1.json"
output_test_file = "/home/landotech/easyrok/drawmate/test/mc_test_1.drawio.xml"

b_test = BuilderTest(input_test_file)
draw_config = b_test.drawmate_config
doc_builder = b_test.doc_builder
mx_builder = b_test.mx_builder

node_id = str(generate_id())
node_side = "left"
node_meta = ApplianceMetadata(node_id, node_side)

node_attributes = {
    "x": 1000,
    "y": 1000,
    "width": 160,
    "height": 90,
    "label": "AV Appliance",
    "input_labels": "HDMI",
    "output_labels": "HDMI",
}

node_builder = NodeBuilder(node_meta)

node_obj = node_builder.init_node(node_attributes)
node_label_obj = node_builder.init_node_label(node_obj)

node_input_obj = node_builder.init_node_input(node_obj.x, node_obj.y, node_obj.input_label)
node_output_obj = node_builder.init_node_output(node_obj.x, node_obj.y, node_obj.output_label)

node_elem = mx_builder.create_mxcell(node_obj.attributes, __id__= node_obj.meta.__ID__, has_label=False)
node_label_elem = mx_builder.create_mxcell(node_label_obj.attributes, __id__=str(generate_id()))
node_input_elem = mx_builder.create_mxcell(node_input_obj.attributes, str(generate_id()))
node_output_elem = mx_builder.create_mxcell(node_output_obj.attributes, str(generate_id()))

doc_builder.root.appendChild(node_elem)
doc_builder.root.appendChild(node_label_elem)
doc_builder.root.appendChild(node_input_elem)
doc_builder.root.appendChild(node_output_elem)
doc_builder.create_xml(output_test_file)
