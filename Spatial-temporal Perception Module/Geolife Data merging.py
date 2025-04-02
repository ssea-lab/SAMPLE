import json
from pathlib import Path
import csv
import re
import pandas as pd

num = 3000

base_path = Path("Spatial-temporal Perception Module/output/geolife/num_10")
file_list = []
for csv_file in base_path.rglob("*.csv"):
    line_count = 0
    with open(csv_file, 'r', encoding='utf-8') as file:  # Adjust the encoding according to the actual situation
        reader = csv.reader(file)
    file_list.append(csv_file)
file_list.sort()

print("------------Retrieve corresponding longitude and latitude according to user links------------")
# Open the file
with open("data/users(geolife).json", "r") as file:
    # Read the file content and parse it into a Python object
    users = json.load(file)

loc = []
loc_all = []
st = []

for user_i in range(0, 45):
    with open(file_list[user_i], 'r', encoding='utf-8') as file:  # Adjust the encoding according to the actual situation
        print(file_list[user_i])
        match = re.search(r"(\d+)\.csv", str(file_list[user_i]))  # Find the part in the file name starting with a number followed by .csv
        if match:
            user_number = match.group(1)
        # print(user_number)
        user_csv = csv.reader(file)
        cnt = 0
        for row in user_csv:
            cnt += 1
            if cnt > 1:
                a = eval(row[2].strip())
                loc.append(a[0])

            if cnt - 1 == len(users["users"][user_i]):
                break
    loc_all.append({
        "user": int(user_number),
        "locs": loc
    })
    loc = []

loc_table = []
loc_temp = []
bases = []

df = pd.read_csv("Spatial-temporal Perception Module/data/locations_geolife.csv")

for loc_i in range(len(loc_all)):
    user_number = loc_all[loc_i]["user"]
    user_locs = loc_all[loc_i]["locs"]

    for loc in user_locs:
        loc_df = df[df["id"] == loc]
        # print(loc_df)
        str_p = loc_df.iloc[0, 2]
        # Remove the leading "POINT (" and trailing ")"
        content = str_p[len("POINT ("):-1]
        # Split the string by space
        parts = content.split(' ')
        long = float(parts[0])
        lat = float(parts[1])
        loc_temp.append([long, lat])
        bases.append([long, lat])
    loc_table.append({
        "user": user_number,
        "locs": loc_temp
    })
    loc_temp = []
bases = [list(x) for x in set(tuple(x) for x in bases)]

print("----------Construct the structure of user_requests----------")
user_requests = []
for i in range(len(loc_table)):
    locations = loc_table[i]["locs"]
    lianlus = users["users"][i]
    flags = [False for i in range(len(users["users"][i]))]
    user_requests.append({
        "locations": locations,
        "lianlus": lianlus,
        "flags": flags
    })

print("----------Construct the structure of base_stations----------")
base_stations = []
g = 39
for i in range(len(bases)):
    location = bases[i]
    radius = 0.0
    resource = [
        3000,
        3000,
        3000
    ]
    allocated_services = []

    base_stations.append({
        "location": location,
        "radius": radius,
        "resource": resource,
        "allocated_services": allocated_services,
    })

base_station = {
    "base_stations": base_stations
}
# file_path = "F:/pycharm/codepython/LLM-Mob-main/output/bases_660.json"
# with open(file_path, 'w') as file:
#     json.dump(base_station, file, indent=4, ensure_ascii=False)
# print(base_stations)

print("----------Constructed structure----------")
with open('methods.json', 'r') as file:
    # Read the file content and parse it into a Python object
    methods = json.load(file)
    methods = methods['methods']

a = {
    "user_requests": user_requests,
    "base_stations": base_stations,
    "methods": methods
}

file_path = f"Spatial-temporal Perception Module/output/geolife_{num}.json"
with open(file_path, 'w') as file:
    json.dump(a, file, indent=4, ensure_ascii=False)