import argparse


def init_drawmate_mc(input_file, output_file):
    from drawmate_engine.drawmate_template_two import Drawmate

    if input_file and output_file:
        draw = Drawmate(input_file, output_file)
        draw.build_graph()
        print(f"\nTemplate creation success\n\nTemplate path: {output_file}\n")


def init_drawmate_sc(input_file, output_file):
    from drawmate_engine.drawmate import Drawmate

    if input_file and output_file:
        draw = Drawmate(input_file, output_file)
        draw.build_graph()
        print(f"\nTemplate creation success\n\nTemplate path: {output_file}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("output_file", help="Path to output file")

    parser.add_argument(
        "-mc",
        "--multiple_connections",
        action="store_true",
        help="If the current config file contains objects/nodes with more than one connection",
    )

    args = parser.parse_args()
    if args.multiple_connections:
        print("Adding multiple connections")
        init_drawmate_mc(args.input_file, args.output_file)
    else:
        print("Default graph")
        init_drawmate_sc(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
