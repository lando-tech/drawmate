# import argparse
# import os
# import threading
# from .doc_builder import get_timestamp
# from .pathfinder import print_system_info
# from .drawmate_renderer import DrawmateRenderer
# from .template_builder import TemplateBuilder


# USER_HOME = os.path.expanduser("~")
# CONFIG_HOME = USER_HOME + "/.config"
# DRAWMATE_HOME = CONFIG_HOME + "/drawmate"
# TEST_HOME = DRAWMATE_HOME + "/tests"


# def generate_config_dir():
#     if get_drawmate_home()[1]:
#         return
#     else:
#         try:
#             os.chdir(CONFIG_HOME)
#             os.mkdir("drawmate")
#             os.chdir("drawmate")
#             os.mkdir("tests")
#             print(f"Created drawmate config directory @ {DRAWMATE_HOME}")
#         except FileNotFoundError as e:
#             print("Failed to create drawmate config directory, ensure that the '.config' directory exists")
#             print(f"Original error {e}")
#             return
#         except PermissionError as p_e:
#             print("Failed to create drawmate config directory, permission error")
#             print(f"Original error {p_e}")
#             return


# def get_drawmate_home() -> tuple[str, bool]:
#     if os.path.isdir(DRAWMATE_HOME):
#         return DRAWMATE_HOME, True
#     else:
#         return "Failed to find drawmate config directory", False


# def input_file_help():
#     msg = (
#         "The path to the JSON template file. See API documentation for how to format the input file.\n" \
#         "Alternatively, pass in the '-b' or '--build-template' flag to get a blank starter template in the correct format"
#     )
#     return msg


# def output_file_help():
#     msg = (
#         "The path to the drawio.xml output file.\n" \
#         "Acceptable file extensions are ['.drawio', '.xml', '.drawio.xml']. Drawio will accept any of those three.\n" \
#         "You can also pass in the '-t' or '--timestamp' flag to append a timestamp to the file."
#     )
#     return msg


# def build_template_help():
#     msg = (
#         "Interactive guide to build a starter JSON template with valid structure and empty node data."
#     )
#     return msg


# def link_label_help():
#     msg = (
#         "Add labels to links based on node positions (e.g., '0101'). See docs for label format."
#     )
#     return msg


# def generate_test_help():
#     msg = (
#         "Generate a test JSON template and output Draw.io XML. Test files are saved to ~/.config/drawmate/tests."
#     )
#     return msg


# def drawmate_render(input_file: str, output_file: str, has_label: bool = False, add_timestamp: bool = False):
#     drawmate = DrawmateRenderer(input_file) # type: ignore
#     drawmate.init_matrix()
#     drawmate.init_nodes("left")
#     drawmate.init_nodes("right")
#     drawmate.render_nodes()
#     drawmate.link_nodes(has_label)
#     drawmate.create_xml(output_file, add_timestamp) # type: ignore


# def generate_test():
#     if os.path.isdir(CONFIG_HOME):
#         write_done = threading.Event()
#         temp_builder = TemplateBuilder()
#         input_path = f"test_template_{get_timestamp()}"
#         output_path = input_path
#         temp_builder.build_test_template()

#         def create_template_and_signal(file_path):
#             try:
#                 temp_builder.create_template(file_path)
#             finally:
#                 print(f"JSON template saved: @ {TEST_HOME}/{input_path}.json")
#                 write_done.set()

#         try:
#             t = threading.Thread(target=create_template_and_signal, args=(f"{TEST_HOME}/{input_path}.json",))
#             t.start()
#             if write_done.wait(timeout=3):
#                 drawmate_render(f"{TEST_HOME}/{input_path}.json", f"{TEST_HOME}/{output_path}.drawio", has_label=True, add_timestamp=False)
#             else:
#                 print(f"Timeout: could not find file: {TEST_HOME}/{input_path}.json")
#             t.join()
#         except IOError as e:
#             print("Failed to create test file")
#             print(f"Original error {e}")

#         return True
#     else:
#         print(f"Failed to generate test file: config directory not found! {CONFIG_HOME}")
#         return False

# def build():
#     from .template_builder import init_template_builder
#     init_template_builder()


# def main():
#     generate_config_dir()
#     parser = argparse.ArgumentParser()
#     parser.add_argument("input_file", help=input_file_help(), nargs="?")
#     parser.add_argument("output_file", help=output_file_help(), nargs="?")
#     parser.add_argument("-v", "--version", help="Print drawmate version, as well as system information", action="store_true")
#     parser.add_argument("-b", "--build-template", action="store_true", help=build_template_help())
#     parser.add_argument("-t", "--timestamp", action="store_true", help="Add a timestamp to the output file")
#     parser.add_argument("-l", "--link-label", action="store_true", help=link_label_help())
#     parser.add_argument("-gt", "--generate-test", action="store_true", help=generate_test_help())
#     args = parser.parse_args()

#     if args.version:
#         print_system_info()
#         exit(code=0)
#     if args.generate_test:
#         generate_test()
#         exit(code=0)
#     if args.build_template:
#         build()
#         exit(code=0)
#     if args.link_label:
#         if args.input_file and args.output_file:
#             if args.timestamp:
#                 drawmate_render(args.input_file, args.output_file, True, True)
#             else:
#                 drawmate_render(args.input_file, args.output_file, True, False)
#             exit(code=0)
#         else:
#             print("[error] --link-label flag used without path to input/output files!")
#             exit(code=-1)
#     elif args.input_file and args.output_file:
#         if args.timestamp:
#             drawmate_render(args.input_file, args.output_file, add_timestamp=True)
#         else:
#             drawmate_render(args.input_file, args.output_file)
#         exit(code=0)

def main():
    from .drawmate_renderer import DrawmateRenderer
    render = DrawmateRenderer("/home/landotech/Projects/drawmate/test/mc_test_1.json")
    for i in render.left_nodes:
        print(i)


if __name__ == "__main__":
    main()
