import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("output_file", help="Path to output file")
    args = parser.parse_args()

    from drawmate_renderer import DrawmateRenderer
    drawmate = DrawmateRenderer(args.input_file) # type: ignore
    drawmate.init_matrix()
    drawmate.init_nodes("left")
    drawmate.init_nodes("right")
    drawmate.render_nodes()
    drawmate.link_nodes()
    drawmate.create_xml(args.output_file) # type: ignore

if __name__ == "__main__":
    main()
