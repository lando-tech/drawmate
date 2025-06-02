import argparse
from .pathfinder import print_system_info
    

def drawmate_render(input_file: str, output_file: str, has_label: bool = False):
    from .drawmate_renderer import DrawmateRenderer
    drawmate = DrawmateRenderer(input_file) # type: ignore
    drawmate.init_matrix()
    drawmate.init_nodes("left")
    drawmate.init_nodes("right")
    drawmate.render_nodes()
    drawmate.link_nodes(has_label)
    drawmate.create_xml(output_file) # type: ignore
    print(f"Template file saved: @ {output_file}")


def build():
    from .template_builder import init_template_builder
    init_template_builder()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file", nargs="?")
    parser.add_argument("output_file", help="Path to output file", nargs="?")
    parser.add_argument("-v", "--version", help="Print drawmate version, as well as system information", action="store_true")
    parser.add_argument("-b", "--build-template", action="store_true", help="Interactive guide to build a JSON starter template")
    parser.add_argument("-l", "--link-label", action="store_true", help="Boolean flag to add labels to each Link using the column/row of the connecting node")
    args = parser.parse_args()

    if args.version:
        print_system_info()
        exit(code=0)
    if args.build_template:
        build()
        exit(code=0)
    if args.link_label:
        if args.input_file and args.output_file:
            drawmate_render(args.input_file, args.output_file, True)
            exit(code=0)
        else: 
            print("[error] --link-label flag used without path to input/output files!")
            exit(code=-1)
    elif args.input_file and args.output_file:
        drawmate_render(args.input_file, args.output_file)
        exit(code=0)


if __name__ == "__main__":
    main()
