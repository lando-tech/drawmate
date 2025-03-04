# # TODO Add module summary
# """_summary_
# doc: instance of the DocBuilder class
# """
#
# from drawmate_engine.doc_builder import create_document, MxObject
# from drawmate_engine.matrix import Matrix, Dtp, Connections, TextBox
# from drawmate_engine.drawmate_config import (
#     DrawmateConfig,
#     MatrixDimensions,
# )
# from utils.pathfinder import PathFinder
# from utils.log_manager import LogManager
#
# global doc
# pf = PathFinder()
# log_mgr = LogManager()
#
# class Drawmate:
#     # TODO Add class summary
#     """_summary_"""
#
#     def __init__(self, matrix_rect: Matrix, draw_config: DrawmateConfig):
#         self.conn_mgr = None
#         self.draw_config = draw_config
#         self.first_level_conn_array = []
#         self.second_level_conn_array = []
#         self.third_level_conn_array = []
#         self.matrix_rect = matrix_rect
#         self.first_level_labels = self.draw_config.get_rect_labels("dtp", level=1)
#         self.second_level_labels = self.draw_config.get_rect_labels("dtp", level=2)
#         self.third_level_labels = self.draw_config.get_rect_labels("dtp", level=3)
#         self.matrix_labels = self.draw_config.get_rect_labels("matrix")
#         self.create_matrix_rect()
#
#     def create_mxobject(self, data: dict, is_arrow: bool):
#         """
#         Summary:
#             Creates the document structure for the xml object, appending each
#             node to the appropriate parent.
#
#         Args:
#             data (dict): The attributes of an instance of the Rect class or one of its children.
#             is_arrow (bool): Check if the Rect is an ArrowRect.
#         """
#         # Create object node
#         mx_obj = MxObject()
#         mx_obj.set_object_values(data["label"], data["type"])
#
#         # If the rect being passed in is an arrow, adjust methods accordingly
#         if is_arrow:
#             # Create mxCell object
#             cell = mx_obj.MxCell()
#             cell.set_mxcell_values_point(data["style"], data["label"])
#
#             # Append mxCell to mxObject
#             cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
#             mx_obj.mx_object.appendChild(cell_elem)
#
#             # Create mxGeometry object
#             geo = cell.MxGeometry()
#             geo.set_geometry_values_point()
#             geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)
#
#             # Append mxGeometry to mxCell
#             cell_elem.appendChild(geo_elem)
#
#             # Call to the create_mxpoint function
#             self.create_mxpoint(
#                 mx_geo=geo, mx_geo_elem=geo_elem, mx_obj=mx_obj, data=data
#             )
#
#         else:
#             # Create mxCell object
#             cell = mx_obj.MxCell()
#             cell.set_mxcell_values(value=data["label"], style=data["style"])
#
#             # Append mxCell to mxObject
#             cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
#             mx_obj.mx_object.appendChild(cell_elem)
#
#             # Create mxGeometry object
#             geo = cell.MxGeometry()
#             geo.set_geometry_values(data["x"], data["y"], data["width"], data["height"])
#
#             # Append mxGeometry to mxCell
#             geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)
#             cell_elem.appendChild(geo_elem)
#
#         # Get root element of xml
#         root = doc.root
#         # Append mxObject to root
#         root.appendChild(mx_obj.mx_object)
#
#     def create_mxpoint(self, mx_geo, mx_geo_elem, mx_obj, data: dict):
#         """
#         Summary:
#             Creates the xml structure for, and instantiates the mxPoint object.
#
#         Args:
#             mx_geo (mxGeometry): An instance of the mxGeometry class.
#             mx_geo_elem (mxGeometryElement): An instance of the mxGeometry xml element.
#             mx_obj (mxObject): An instance of the mxObject class.
#             data (dict): An attribute dictionary from the instance of the Arrow class.
#         """
#         # Set source mxPoint element
#         source_point = mx_geo.MxPoint()
#         source_point.set_mxpoint_source(data["source_x"], data["source_y"])
#         source_element = mx_obj.create_xml_element("mxPoint", source_point.attributes)
#         mx_geo_elem.appendChild(source_element)
#
#         # Set target mxPoint element
#         target_point = mx_geo.MxPoint()
#         target_point.set_mxpoint_target(data["target_x"], data["target_y"])
#         target_elem = mx_obj.create_xml_element("mxPoint", target_point.attributes)
#         mx_geo_elem.appendChild(target_elem)
#
#     def create_matrix_rect(self):
#         """
#         Summary:
#             This is a dispatcher function that manages all the
#             logic to create each object on the graph,
#             and calls the appropriate function.
#             This is the main entry point for the program.
#         """
#         # Get matrix attributes
#         matrix_attrib = self.matrix_rect.attributes
#
#         # Create textboxes for the matrix
#         self.matrix_rect.create_matrix_textboxes(self.matrix_labels)
#
#         # Store an instance of the textbox array from the matrix class
#         text_box_array = self.matrix_rect.matrix_text_boxes
#
#         # Create xml element for matrix rect
#         self.create_mxobject(matrix_attrib, is_arrow=False)
#
#         # Create label for matrix
#         matrix_label = self.matrix_rect.add_matrix_label(
#             self.matrix_rect.attributes["x"],
#             self.matrix_rect.attributes["y"],
#             self.matrix_rect.attributes["label"],
#         )
#         self.create_mxobject(matrix_label.attributes, is_arrow=False)
#
#         # Create xml elements for text boxes
#         self.iter_create_object(appliance_array=text_box_array)
#
#         # TODO Pass in the tuple, with the appliance text box in/out labels
#
#         # Create first level appliances to be connected to the matrix
#         self.matrix_rect.create_first_level_appliance(
#             self.draw_config.get_rect_labels_as_tuple(level=1)
#         )
#         # Store an instance of the appliance array
#         dtp_array = self.matrix_rect.dtp_rects
#         # Place dtp appliances on graph
#         self.place_appliance(appliance_array=dtp_array, second_level=True)
#
#         # Store an instance of the second level dtp rects
#         second_level_array = self.matrix_rect.second_level_dtp_rects
#
#         # Create the second level appliances
#         self.create_object_with_label(
#             appliance_array=second_level_array,
#             label_array=self.second_level_labels,
#         )
#         self.place_appliance(appliance_array=second_level_array, second_level=False)
#
#         # Store an instance of the third level appliances
#         third_level_array = self.matrix_rect.third_level_dtp_rects
#
#         # Create third level appliances
#         self.create_object_with_label(
#             appliance_array=third_level_array,
#             label_array=self.third_level_labels,
#         )
#
#         # Create input/output text box for each appliance
#         appliance_textboxes = self.matrix_rect.dtp_text_boxes
#         self.iter_create_object(appliance_array=appliance_textboxes)
#
#         # Connect all appliances
#         self.connect_first_level_appliances(
#             appliance_array=dtp_array,
#             text_box_array=text_box_array,
#         )
#         self.connect_sublevel_appliances(
#             first_level_array=dtp_array,
#             sublevel_array=second_level_array,
#             third_level=False,
#         )
#         self.connect_sublevel_appliances(
#             first_level_array=second_level_array,
#             sublevel_array=third_level_array,
#             third_level=True,
#         )
#
#     def place_appliance(self, appliance_array: list[Dtp], second_level: bool):
#         """
#         Iterate through the array of appliance nodes and place them on the graph
#         according to their X coordinate and which level (1st, 2nd, 3rd) on the
#         graph.
#
#         Args:
#             appliance_array (list[Dtp]): List of Appliance nodes
#             second_level (bool): If the appliance is on the second level on the graph
#         """
#
#         # Create first level appliances, and instantiate the second level appliances
#         for index, item in enumerate(appliance_array):
#
#             # indexed first level labels
#             indexed_label_first = self.first_level_labels[index][0]
#             # indexed second level labels
#             indexed_label_second = self.second_level_labels[index][0]
#             # indexed third level labels
#             indexed_label_third = self.third_level_labels[index][0]
#
#             # indexed second level in/out labels
#             second_level_in = self.second_level_labels[index][1]
#             second_level_out = self.second_level_labels[index][2]
#
#             # indexed third level in/out labels
#             third_level_in = self.third_level_labels[index][1]
#             third_level_out = self.third_level_labels[index][2]
#
#             # Debug print statements
#             # if index == 0:
#             #     print("==============================")
#
#             # if second_level:
#             #     print(f"\nFirst level label: {indexed_label_first}")
#             # else:
#             #     print(f"\nSecond level label: {indexed_label_second}")
#
#             # print(f"First level x: {item.attributes["x"]}")
#             # print(f"First level y: {item.attributes["y"]}")
#             # print(f"Index: {index}\n")
#             # print("==============================")
#
#             if item.attributes["x"] > self.matrix_rect.attributes["x"]:
#                 # Debug print statements
#                 # print(f"\nFirst level left x coordinate: {item.attributes['x']}")
#                 # print(f"Matrix x: {self.matrix_rect.attributes["x"]}\n")
#                 # print("\n==============================\n")
#                 if second_level:
#                     # if indexed_label_second.strip() == "":
#                     #     print("\nSecond level No appliance\n")
#                     #     print("==============================\n")
#                     # else:
#                     #     print(f"\n{indexed_label_second}\n")
#                     #     print("==============================\n")
#
#                     self.matrix_rect.add_second_level_appliance(
#                         is_left=True,
#                         first_level_x=item.attributes["x"],
#                         first_level_y=item.attributes["y"],
#                         current_label=indexed_label_second,
#                         in_label=second_level_in,
#                         out_label=second_level_out,
#                     )
#                 else:
#                     # if indexed_label_third.strip() == "":
#                     # Debug print statements
#                     # print("\nThird level No appliance\n")
#                     # print("==============================\n")
#                     # else:
#                     #     print(f"\n{indexed_label_third}\n")
#                     #     print("==============================\n")
#                     self.matrix_rect.add_third_level_appliance(
#                         is_left=True,
#                         first_level_x=item.attributes["x"],
#                         first_level_y=item.attributes["y"],
#                         current_label=indexed_label_third,
#                         in_label=third_level_in,
#                         out_label=third_level_out,
#                     )
#             if item.attributes["x"] < self.matrix_rect.attributes["x"]:
#                 if second_level:
#                     # if indexed_label_second.strip() == "":
#                     # Debug print statements
#                     # print("\nSecond level No appliance\n")
#                     # print("==============================\n")
#                     # else:
#                     # print(f"\n{indexed_label_second}\n")
#                     # print("==============================\n")
#
#                     self.matrix_rect.add_second_level_appliance(
#                         is_left=False,
#                         first_level_x=item.attributes["x"],
#                         first_level_y=item.attributes["y"],
#                         current_label=indexed_label_second,
#                         in_label=second_level_in,
#                         out_label=second_level_out,
#                     )
#                 else:
#                     # if indexed_label_third.strip() == "":
#                     # Debug print statements
#                     # print("\nThird level No appliance\n")
#                     # print("==============================\n")
#                     # else:
#                     #     print(f"\n{indexed_label_third}\n")
#                     #     print("==============================\n")
#                     self.matrix_rect.add_third_level_appliance(
#                         is_left=False,
#                         first_level_x=item.attributes["x"],
#                         first_level_y=item.attributes["y"],
#                         current_label=indexed_label_third,
#                         in_label=third_level_in,
#                         out_label=third_level_out,
#                     )
#             if second_level:
#                 # If the label is empty, don't create the object on the graph
#                 if indexed_label_first.strip() == "":
#                     pass
#                 else:
#                     self.create_mxobject(item.attributes, is_arrow=False)
#                     appliance_label = self.matrix_rect.add_appliance_label(
#                         dtp_x=item.attributes["x"],
#                         dtp_y=item.attributes["y"],
#                         label=indexed_label_first,
#                     )
#                     self.create_mxobject(appliance_label.attributes, is_arrow=False)
#
#     def iter_create_object(self, appliance_array: list):
#         """_summary_
#
#         Args:
#             appliance_array (list): _description_
#         """
#         for i in appliance_array:
#             self.create_mxobject(i.attributes, is_arrow=False)
#
#     def create_object_with_label(
#         self, appliance_array: list[Dtp], label_array: list[list]
#     ):
#         """_summary_
#
#         Args:
#             appliance_array (list[Dtp]): _description_
#             label_array (list[list]): _description_
#         """
#         for index, item in enumerate(appliance_array):
#             current_label = label_array[index][0]
#             if current_label.strip() == "":
#                 pass
#             else:
#                 self.create_mxobject(item.attributes, is_arrow=False)
#                 label = self.matrix_rect.add_appliance_label(
#                     dtp_x=item.attributes["x"],
#                     dtp_y=item.attributes["y"],
#                     label=current_label,
#                 )
#                 self.create_mxobject(label.attributes, is_arrow=False)
#
#     def connect_first_level_appliances(
#         self,
#         appliance_array: list[Dtp],
#         text_box_array: list[TextBox],
#     ):
#         """_summary_
#
#         Args:
#             appliance_array (list[Dtp]): _description_
#             text_box_array (list[TextBox]): _description_
#         """
#         counter_left = 0
#         counter_right = 0
#         for dtp, text in zip(appliance_array, text_box_array):
#
#             self.conn_mgr = Connections(dtp, text, first_level=True)
#
#             counter_left += 1
#
#             if counter_left == self.matrix_rect.num_connections + 1:
#                 counter_left = 1
#             elif counter_left > self.matrix_rect.num_connections + 1:
#                 counter_right += 1
#                 counter_left = counter_right
#
#             label = self.get_connection_label(
#                 appliance_x=dtp.attributes["x"],
#                 level=1,
#                 counter=counter_left,
#             )
#             new_connection = self.conn_mgr.create_connection(label, "arrow")
#             self.first_level_conn_array.append(new_connection)
#
#         for index, item in enumerate(self.first_level_conn_array):
#             if self.first_level_labels[index][0].strip() == "":
#                 pass
#             else:
#                 self.create_mxobject(item.attributes, is_arrow=True)
#
#     def connect_sublevel_appliances(
#         self,
#         first_level_array: list,
#         sublevel_array: list,
#         third_level: bool,
#     ):
#         """_summary_
#
#         Args:
#             first_level_array (list): _description_
#             sublevel_array (list): _description_
#             third_level (bool): _description_
#         """
#
#         counter_left = 0
#         counter_right = 0
#
#         for item in sublevel_array:
#             # Start value for the closest first level appliance
#             closest_dtp = None
#             # The threshold for how close the appliance should be to make a connection
#             threshold = 500
#             # The minimum x coordinate
#             min_distance_x = float(500.0)
#             # The minimum y coordinate
#             min_distance_y = float(20.0)
#             # The x and y cords for the current second level appliance
#             item_x = int(item.attributes["x"])
#             item_y = int(item.attributes["y"])
#
#             # Connections counter
#
#             for dtp in first_level_array:
#                 dtp_x = int(dtp.attributes["x"])
#                 dtp_y = int(dtp.attributes["y"])
#                 # The absolute distance between x and y of current second and first level appliance
#                 distance_x = abs(dtp_x - item_x)
#                 distance_y = abs(dtp_y - item_y)
#                 # If the absolute distance is less than the min distance, set values accordingly
#                 if distance_x < min_distance_x and distance_y < min_distance_y:
#                     min_distance_x = distance_x
#                     min_distance_y = distance_y
#                     closest_dtp = dtp
#             # Compare the above calculated distances to the threshold,
#             # then add those instances to the Connections class
#             if (
#                 closest_dtp
#                 and min_distance_x <= threshold
#                 and min_distance_y <= threshold
#             ):
#                 self.conn_mgr = Connections(closest_dtp, item, first_level=False)
#                 # add labels here
#                 if third_level:
#                     counter_left += 1
#
#                     if counter_left == self.matrix_rect.num_connections + 1:
#                         counter_left = 1
#                     elif counter_left > self.matrix_rect.num_connections + 1:
#                         counter_right += 1
#                         counter_left = counter_right
#
#                     label = self.get_connection_label(
#                         appliance_x=item_x,
#                         level=3,
#                         counter=counter_left,
#                     )
#                     new_connection = self.conn_mgr.create_connection(label, "arrow")
#                     self.third_level_conn_array.append(new_connection)
#                 else:
#                     counter_left += 1
#
#                     if counter_left == self.matrix_rect.num_connections + 1:
#                         counter_left = 1
#                     elif counter_left > self.matrix_rect.num_connections + 1:
#                         counter_right += 1
#                         counter_left = counter_right
#
#                     label = self.get_connection_label(
#                         appliance_x=item_x,
#                         level=2,
#                         counter=counter_left,
#                     )
#                     new_connection = self.conn_mgr.create_connection(label, "arrow")
#                     self.second_level_conn_array.append(new_connection)
#
#         if third_level:
#             sorted_dtp_rects = sorted(
#                 self.third_level_conn_array, key=lambda x: x.attributes["source_x"]
#             )
#         else:
#             # Sort the list of connections based on source x coordinate
#             sorted_dtp_rects = sorted(
#                 self.second_level_conn_array, key=lambda x: x.attributes["source_x"]
#             )
#         # Iteratively create a new connection/arrow object on the graph
#         for index, item in enumerate(sorted_dtp_rects):
#             if third_level:
#                 if self.third_level_labels[index][0] != "":
#                     self.create_mxobject(item.attributes, is_arrow=True)
#             else:
#                 if self.second_level_labels[index][0] != "":
#                     self.create_mxobject(item.attributes, is_arrow=True)
#
#     def get_connection_label(self, appliance_x, level: int, counter: int) -> str:
#         """
#
#         Args:
#             appliance_x:
#             level:
#             counter:
#
#         Returns:
#
#         """
#
#         if level == 1:
#             if int(appliance_x) < int(self.matrix_rect.attributes["x"]):
#                 if counter >= 10:
#                     return "00" + str(counter)
#                 else:
#                     return "000" + str(counter)
#             else:
#                 if counter >= 10:
#                     return "10" + str(counter)
#                 else:
#                     return "100" + str(counter)
#
#         if level == 2:
#             if int(appliance_x) < int(self.matrix_rect.attributes["x"]):
#                 if counter >= 10:
#                     return "01" + str(counter)
#                 return "010" + str(counter)
#             else:
#                 if counter >= 10:
#                     return "11" + str(counter)
#                 else:
#                     return "110" + str(counter)
#
#         if level == 3:
#             if int(appliance_x) < int(self.matrix_rect.attributes["x"]):
#                 if counter >= 10:
#                     return "02" + str(counter)
#                 else:
#                     return "020" + str(counter)
#             else:
#                 if counter >= 10:
#                     return "12" + str(counter)
#                 else:
#                     return "120" + str(counter)
#
#
# def draw(output_file_path: str, input_file_path: str) -> bool:
#     """_summary_"""
#
#     draw_config = DrawmateConfig(input_file_path)
#     try:
#         # Graph dimensions fetched from json template
#         graph_dimensions = draw_config.get_graph_dimensions()
#         dx = graph_dimensions.dx
#         dy = graph_dimensions.dy
#         page_width = graph_dimensions.width
#         page_height = graph_dimensions.height
#
#         global doc
#         # Create root document
#         doc = create_document(x=dx, y=dy, width=page_width, height=page_height)
#         matrix_dims = draw_config.get_matrix_dimensions()
#         draw_matrix_one(matrix_dims)
#         doc.create_xml(output_file_path)
#         log_data = "No key errors were detected during template creation."
#         log_mgr.add_log(
#             object_log="drawmate",
#             message=log_data,
#             line_number="495",
#             is_error=False,
#             is_warning=False,
#         )
#         return True
#     except KeyError as e:
#         error = f"Missing required field in template: {e}"
#         print(error)
#         log_mgr.add_log(
#             object_log="drawmate",
#             message=error,
#             line_number="504",
#             is_error=True,
#             is_warning=False,
#         )
#         return False
#
#
# def draw_matrix_one(matrix_dimensions: MatrixDimensions):
#     """
#     summary:
#     """
#     # Matrix attributes fetched from json template
#     # Matrix inputs and outputs
#     num_connections = matrix_dimensions.num_connections
#
#     # Matrix dimensions
#     matrix_width = matrix_dimensions.width
#     matrix_height = matrix_dimensions.height
#     matrix_x = matrix_dimensions.x
#     matrix_y = matrix_dimensions.y
#
#     # Matrix Label
#     matrix_label = matrix_dimensions.labels
#
#     # Create matrix 1
#     matrix_rect_1 = Matrix(
#         connections_count=num_connections,
#         matrix_label=matrix_label,
#         width=matrix_width,
#         height=matrix_height,
#         x=matrix_x,
#         y=-matrix_y,
#     )
#
#     Drawmate(matrix_rect=matrix_rect_1, draw_config)
from multiprocessing.resource_tracker import ensure_running

from drawmate_config import DrawmateConfig
from matrix import Matrix, Dtp
from doc_builder import DocBuilder, MxObject

# from drawmate_engine.node import Node


class Drawmate(DocBuilder):

    def __init__(
        self,
        draw_config: DrawmateConfig,
    ):
        super().__init__()
        self.dc = draw_config
        self.matrix_array = self.dc.build_matrix_array()

    def create_matrix(self) -> Matrix:
        matrix_attrib = self.dc.get_matrix_dimensions()
        return Matrix(
            x=matrix_attrib.x,
            y=matrix_attrib.y,
            width=matrix_attrib.width,
            height=matrix_attrib.height,
            connections_count=matrix_attrib.num_connections,
            matrix_label=matrix_attrib.labels,
        )

    def create_dtp(self, x, y, label):
        return Dtp(x=x, y=y, label=label)

    def create_mxobject(self, data: dict, is_arrow: bool):
        """
        Summary:
            Creates the document structure for the xml object, appending each
            node to the appropriate parent.

        Args:
            data (dict): The attributes of an instance of the Rect class or one of its children.
            is_arrow (bool): Check if the Rect is an ArrowRect.
        """
        # Create object node
        mx_obj = MxObject()
        mx_obj.set_object_values(data["label"], data["type"])

        # If the rect being passed in is an arrow, adjust methods accordingly
        if is_arrow:
            # Create mxCell object
            cell = mx_obj.MxCell()
            cell.set_mxcell_values_point(data["style"], data["label"])

            # Append mxCell to mxObject
            cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
            mx_obj.mx_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = cell.MxGeometry()
            geo.set_geometry_values_point()
            geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)

            # Append mxGeometry to mxCell
            cell_elem.appendChild(geo_elem)

            # Call to the create_mxpoint function
            self.create_mxpoint(
                mx_geo=geo, mx_geo_elem=geo_elem, mx_obj=mx_obj, data=data
            )

        else:
            # Create mxCell object
            cell = mx_obj.MxCell()
            cell.set_mxcell_values(value=data["label"], style=data["style"])

            # Append mxCell to mxObject
            cell_elem = mx_obj.create_xml_element("mxCell", cell.attributes)
            mx_obj.mx_object.appendChild(cell_elem)

            # Create mxGeometry object
            geo = cell.MxGeometry()
            geo.set_geometry_values(data["x"], data["y"], data["width"], data["height"])

            # Append mxGeometry to mxCell
            geo_elem = mx_obj.create_xml_element("mxGeometry", geo.attributes)
            cell_elem.appendChild(geo_elem)

        # Get root element of xml
        # Append mxObject to root
        self.root.appendChild(mx_obj.mx_object)

    def create_mxpoint(self, mx_geo, mx_geo_elem, mx_obj, data: dict):
        """
        Summary:
            Creates the xml structure for, and instantiates the mxPoint object.

        Args:
            mx_geo (mxGeometry): An instance of the mxGeometry class.
            mx_geo_elem (mxGeometryElement): An instance of the mxGeometry xml element.
            mx_obj (mxObject): An instance of the mxObject class.
            data (dict): An attribute dictionary from the instance of the Arrow class.
        """
        # Set source mxPoint element
        source_point = mx_geo.MxPoint()
        source_point.set_mxpoint_source(data["source_x"], data["source_y"])
        source_element = mx_obj.create_xml_element("mxPoint", source_point.attributes)
        mx_geo_elem.appendChild(source_element)

        # Set target mxPoint element
        target_point = mx_geo.MxPoint()
        target_point.set_mxpoint_target(data["target_x"], data["target_y"])
        target_elem = mx_obj.create_xml_element("mxPoint", target_point.attributes)
        mx_geo_elem.appendChild(target_elem)


def process_nodes(matrix_arr):
    x_spacing = 400
    y_spacing = 140
    left_x = int(matrix.attributes["x"]) - x_spacing
    right_x = int(matrix.attributes["x"]) + x_spacing
    start_y = int(matrix.attributes["y"]) - y_spacing
    left_nodes = matrix_arr[0]
    right_nodes = matrix_arr[1]
    create_nodes(left_nodes, left_x, start_y, x_spacing, y_spacing, True)
    create_nodes(right_nodes, right_x, start_y, x_spacing, y_spacing, False)


def create_nodes(node_arr: list, x, start_y, x_spacing, y_spacing, left: bool):

    print(f"Starting y coord = {start_y}")

    for index, item in enumerate(node_arr):
        y = start_y
        level_counter = 0
        for r_index, row in enumerate(item):
            label, l_input, r_output = row
            next_label = item[(r_index + 1) % len(item)][0]
            # print("Current label: " + label)
            # print("Next label: " + next_label)

            if label.strip() == "" and next_label.strip() == "":
                y = y + (y_spacing * 2)
                if r_index == 0:
                    x = x - x_spacing if left else x + x_spacing
            elif label.strip() == "":
                y = y + y_spacing

            if next_label.strip() == "":
                y = y + y_spacing

            if index > 0 and r_index == 0:
                y = int(matrix.attributes["y"]) - y_spacing
                if left:
                    x = x - x_spacing
                else:
                    x = x + x_spacing
            y += y_spacing

            dtp = Dtp(x, y, label)
            if index == 0:
                dtp.right_ptr = matrix
                dtp.left_ptr = next_label

            drawmate.create_mxobject(dtp.attributes, is_arrow=False)
            level_counter += 1


dc = DrawmateConfig(
    "C:/Users/aaron/GitHub/drawmate/data/templates/builder-template-master.json"
)
drawmate = Drawmate(draw_config=dc)
drawmate.set_graph_values(dx=4000, dy=4000, page_width=4000, page_height=4000)
matrix = drawmate.create_matrix()
drawmate.create_mxobject(matrix.attributes, is_arrow=False)
matrix_array = dc.build_matrix_array()
process_nodes(matrix_array)
drawmate.create_xml("C:/Users/aaron/GitHub/drawmate/data/output.drawio")

