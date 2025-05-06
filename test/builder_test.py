from drawmate_engine.drawmate_config import DrawmateConfig
from builder.mx_builder import MxBuilder
from builder.doc_builder import DocBuilder


class BuilderTest:
    def __init__(self, test_file: str):
        self.drawmate_config: DrawmateConfig = DrawmateConfig(test_file)
        self.mx_builder: MxBuilder = MxBuilder()
        self.doc_builder: DocBuilder = DocBuilder()


b_test = BuilderTest("/home/landotech/easyrok/drawmate/test/mc_test_1.json")
left_side, right_side = b_test.drawmate_config.build_node_dict(8)
for k, v in left_side.items():
    col, row = k.split("-")
    print(f"Left Side: {col} - {row} -- {v}")

for k, v in right_side.items():
    col, row = k.split("-")
    print(f"Right Side: {col} - {row} -- {v}")