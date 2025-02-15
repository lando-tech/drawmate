connections_counter = 0
connections_label = ""
connections_array = []

left_side = False
right_side = False

first_level = False
second_level = False
third_level = False

for i in range(0, 30):
    if i < 10:
        first_level = True
    else:
        break

    if first_level:
        connections_counter += 1
        connections_label = "000" + str(connections_counter)
        connections_array.append(connections_label)


print(connections_array)