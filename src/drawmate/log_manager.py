# from pathfinder import PathFinder
# from datetime import datetime

# pf = PathFinder()


# def get_timestamp():
#     """_summary_

#     Returns:
#         _type_: _description_
#     """
#     timestamp = datetime.now().replace(microsecond=0)
#     formatted_timestamp = timestamp.strftime("%a %d %b %Y %I_%M_%S")

#     return formatted_timestamp


# class LogManager:

#     def __init__(self):
#         self.drawmate_logs_path = f"{pf.log_dir}drawmate_logs.txt"
#         self.doc_builder_logs_path = f"{pf.log_dir}doc_builder_logs.txt"
#         self.gui_logs_path = f"{pf.log_dir}gui_logs.txt"
#         self.web_logs_path = f"{pf.log_dir}web_logs.txt"
#         self.matrix_logs_path = f"{pf.log_dir}matrix_logs.txt"
#         self.async_main_path = f"{pf.log_dir}async_main_logs.txt"

#         self.separator = "\n======================================\n\n"
#         self.error_header = "ERROR"
#         self.warning_header = "WARNING"
#         self.success_header = "SUCCESS"
#         self.timestamp = get_timestamp()

#     def add_log(
#         self,
#         object_log: str,
#         message: str,
#         line_number: str,
#         is_error: bool,
#         is_warning: bool,
#     ):
#         """
#         Summary:

#         """
#         header = str()
#         if is_error:
#             header = self.error_header

#         if is_warning:
#             header = self.warning_header

#         if not is_warning and not is_error:
#             header = self.success_header

#         file_path = str()
#         py_file = str()
#         if object_log == "drawmate":
#             file_path = self.drawmate_logs_path
#             py_file = "drawmate.py"
#         elif object_log == "doc_builder":
#             file_path = self.doc_builder_logs_path
#             py_file = "doc_builder.py"
#         elif object_log == "gui":
#             file_path = self.gui_logs_path
#             py_file = "gui.py"
#         elif object_log == "matrix":
#             file_path = self.matrix_logs_path
#             py_file = "matrix.py"
#         elif object_log == "web":
#             file_path = self.web_logs_path
#             py_file = "app.py"
#         elif object_log == "async_main":
#             file_path = self.async_main_path
#             py_file = "template_hash.py"
#         else:
#             print("Key error, please specify object log")

#         formatted_message = self.format_log(
#             header=header, message=message, line_number=line_number, py_file=py_file
#         )

#         try:
#             with open(file_path, "a", encoding="utf-8") as log_file:
#                 log_file.write(formatted_message)
#         except IOError:
#             print("Failed to write contents to log file: Line 74 log_manager.py")

#     def format_log(
#         self, header: str, message: str, line_number: str, py_file: str
#     ) -> str:
#         log_data = (
#             "\n\n"
#             + header
#             + " ----- "
#             + self.timestamp
#             + self.separator
#             + f"{header} Message: '{message}'"
#             + "\n"
#             + f"{py_file} | Line Number: {line_number}"
#         )
#         return log_data
