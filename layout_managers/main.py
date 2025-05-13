import json


with open("../test_templates/xtp_crosspoint_6400.json", "r") as temp:
    data = json.load(temp)
    for k, v in data.items():
        new_entry = ['', '', '', ['NONE'], ["NONE"]]
        try:
            level = v.get("labels")
            for i in range(24):
                level.append(new_entry)
            with open('../test_templates/xtp_crosspoint_6400.json', 'w') as new_temp:
                json.dump(data, new_temp, indent=2)
        except AttributeError:
            print("Not a level entry")