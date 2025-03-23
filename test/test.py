# def create_connections(self, appliance_array: list[Appliance], left: bool):
#     """
#     Create connection/arrow objects for each appliance based on the left and right
#     pointers
#     Args:
#         appliance_array: The array of either left/right side appliances
#         left: if the array being passed in is on the left of the matrix
#
#     Returns:
#         None
#     """
#     counter = 0
#     for app_index, appliance in enumerate(appliance_array):
#         counter += 1
#         if counter > int(self.matrix.num_connections):
#             counter = 1
#
#         col, row = self.get_corresponding_index(
#             app_index, self.matrix.num_connections
#         )
#         if appliance.attributes["label"] == "":
#             pass
#         else:
#             if left:
#                 ptr = appliance.right_ptr
#                 if ptr.attributes:
#                     # if col == 0:
#                     if appliance.output_label:
#                         arrow_label = (
#                             appliance.output_label
#                             + " "
#                             + self.generate_connection_number(
#                                 col, counter, left
#                             )
#                         )
#                         self.dispatch_connections(
#                             appliance, ptr, col, left, arrow_label
#                         )
#                     elif appliance.output_label_array:
#                         num_connections = len(appliance.right_ptr_array)
#                         num_offset = 0
#                         for i in range(num_connections):
#                             arrow_label = (
#                                 appliance.output_label_array[i]
#                                 + " "
#                                 + self.generate_connection_number(
#                                     col, counter + num_offset, left
#                                 )
#                             )
#                             self.dispatch_connections(appliance, ptr, col, left, arrow_label, True)
#                             num_offset += 1
#
#             else:
#                 ptr = appliance.left_ptr
#                 if ptr.attributes:
#                     # if col == 0:
#                     if appliance.output_label:
#                         arrow_label = (
#                             appliance.output_label
#                             + " "
#                             + self.generate_connection_number(
#                                 col, counter, False
#                             )
#                         )
#                         self.dispatch_connections(
#                             ptr, appliance, col, False, arrow_label
#                         )
#                     elif appliance.output_label_array:
#                         num_connections = len(appliance.left_ptr_array)
#                         num_offset = 0
#                         for i in range(num_connections):
#                             arrow_label = (
#                                 appliance.output_label_array[i]
#                                 + " "
#                                 + self.generate_connection_number(
#                                     col, counter + num_offset, left
#                                 )
#                             )
#                             self.dispatch_connections(ptr, appliance, col, False, arrow_label, True)
#                             num_offset += 1
#
# def dispatch_connections(
#     self,
#     ptr: Rect,
#     appliance: Appliance,
#     col: int,
#     left: bool,
#     conn_label: str,
#     mc: bool = False
# ):
#     connection_mgr = Connections(ptr, appliance, col, left, mc)
#     arrow = connection_mgr.create_connection("", "arrow")
#     arrow_textbox = TextBox(
#         x=int(arrow.attributes["target_x"]) - ARROW_CONNECTIONS["x_offset"],
#         y=int(arrow.attributes["target_y"]) - ARROW_CONNECTIONS["y_offset"],
#         width=ARROW_CONNECTIONS["width"],
#         height=ARROW_CONNECTIONS["height"],
#         label=conn_label,
#         _type="text-box",
#     )
#     self.create_mxobject(arrow.attributes, is_arrow=True)
#     self.create_mxobject(arrow_textbox.attributes)
