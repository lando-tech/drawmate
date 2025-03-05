import os
import json
import platform


def get_os_name():
    return platform.system()


OS_NAME = get_os_name()
print(f"\nOperating System: {OS_NAME}")


class PathFinder:

    def __init__(self):
        # Path to the data directories to export to other modules
        self.xml_export_dir = f"{self.get_project_dir()}/data/xml_files/xml_exports/"
        self.xml_template_dir = f"{self.get_project_dir()}/data/xml_files/xml_templates/"
        self.json_templates = f"{self.get_project_dir()}/data/templates/"
        self.log_dir = f"{self.get_project_dir()}/logs/"
        self.FILETYPES = [
            (("xml files", "*.xml"), ("all files", "*.*")),
            (("json files", "*.json"), ("all files", "*.*")),
            (("pdf files", "*.pdf"), ("all files", "*.*")),
            (("toml files", "*.toml"), ("all files", "*.*")),
        ]

    @staticmethod
    def get_project_dir():
        """Return the root directory of the project"""
        path_finder_dir = os.path.dirname(os.path.abspath(__file__))

        while (
            not os.path.isfile(os.path.join(path_finder_dir, "anchor.toml"))
            and path_finder_dir != "/"
        ):
            path_finder_dir = os.path.dirname(path_finder_dir)

        if path_finder_dir == "/":
            raise RuntimeError("Project root directory not found")

        return path_finder_dir

    def get_xml_exports(self):
        """Return the contents of the xml exports dir, sorted by timestamp"""

        with os.scandir(self.xml_export_dir) as entries:
            file_paths = [entry.path for entry in entries if entry.is_file()]

        return sorted(file_paths, key=lambda x: os.path.getmtime(x))

    def get_xml_templates(self):
        """Return the contents of the xml uploads dir, sorted by timestamp"""
        with os.scandir(self.xml_template_dir) as entries:
            file_paths = [entry.path for entry in entries if entry.is_file()]

        return sorted(file_paths, key=lambda x: os.path.getmtime(x))

    def export_template(self):
        """Return the latest entry in the template_list"""
        with open(
            f"{self.templates}builder-template-master.json", "r", encoding="utf-8"
        ) as export:
            exported_data = json.load(export)

        return exported_data

    def view_templates(self):
        """Return a list of current templates"""
        template_list = None
        with open(
            f"{self.templates}builder-template-master.json", "r", encoding="utf-8"
        ) as view:
            template_view = json.load(view)

            for key, value in template_view.items():
                template_list = value

            return template_list
