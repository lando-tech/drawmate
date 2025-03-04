import sys
import json
import time

from drawmate_engine.drawmate import draw
from utils.pathfinder import PathFinder
# from utils.log_manager import LogManager

pf = PathFinder()
# lg = LogManager()


def get_template_file(input_file):
    try:
        with open(input_file, "r") as new_template:
            content = new_template.read()
            json_content = json.loads(content)
            return json_content
    except FileNotFoundError as e:
        print("File not found or incorrect path")


def update_template(input_file) -> bool:
    """
    Update the contents of the template file with the user provided template.

    Returns: True if file was successfully saved. False otherwise.

    """
    template_data = get_template_file(input_file)
    json_data = json.dumps(template_data, indent=4)
    try:
        with open(
            f"{pf.template_dir}builder-template-master.json", "w", encoding="utf-8"
        ) as temp_file:
            temp_file.write(json_data)
            return True
    except IOError as e:
        print("Error updating template file. Check log files for error messages.")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <input-file-path> <output-file-path>")
    else:
        user_input_file = sys.argv[1]
        user_output_file = sys.argv[2]
        if user_input_file[0] == "~":
            print(
                "Wildcard character detected on input path, please provide absolute path:"
            )
            print("/home/user/<input-file-path>")

        if user_output_file[0] == "~":
            print(
                "Wildcard character detected on output path, please provide the absolute path:"
            )
            print("/home/user/<output-file-path>")

        draw(user_input_file, user_output_file)
        print(f"\nTemplate creation success\n\nTemplate path: {user_output_file}")
