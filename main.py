import sys
import json
import time

from drawmate_engine.drawmate import draw
from utils.pathfinder import PathFinder

pf = PathFinder()

def get_template_file() :
    if len(sys.argv) != 2:
        print("Usage: python script.py <file-path>")
    else:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as new_template:
                content = new_template.read()
                json_content = json.loads(content)
                return json_content
        except FileNotFoundError:
            print("File not found or incorrect path")


def update_template():
    template_data = get_template_file()
    json_data = json.dumps(template_data, indent=4)
    with open(f"{pf.TEMPLATE_DIR}builder-template-master.json", "w", encoding="utf-8") as temp_file:
        temp_file.write(json_data)
        return True


if update_template():
    time.sleep(3)
    draw()