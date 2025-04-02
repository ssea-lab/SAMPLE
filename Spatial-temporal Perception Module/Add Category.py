import json
import math
from collections import Counter

# Define parameters
num = 3000

# Load data from JSON file
with open(f'Spatial-temporal Perception Module/output/geolife_{num}.json', 'r') as file:
    aall = json.load(file)
    base_stations = aall['base_stations']
    user_requests = aall['user_requests']

# Initialize a list to store base station location information
l = []
for i in range(len(base_stations)):
    lat = base_stations[i]["location"][1]  # Latitude
    long = base_stations[i]["location"][0]  # Longitude
    l.append({(long, lat): []})

def calculate_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the distance between two points using the Haversine formula (in kilometers).

    :param lat1: Latitude of the first point.
    :param lon1: Longitude of the first point.
    :param lat2: Latitude of the second point.
    :param lon2: Longitude of the second point.
    :return: Distance between the two points (in kilometers).
    """
    R = 6371000  # Earth's average radius in meters
    # print(type(lon1))
    # print(type(lat1))
    # print(type(lon2))
    # print(type(lat2))

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

# Initialize a list to store user-related information
u = []
ans = 0
for user in user_requests:
    st = set()
    for i in range(len(user["locations"])):
        lat = user["locations"][i][1]
        long = user["locations"][i][0]
        for j in range(len(l)):
            for key in l[j].keys():
                # print(type(long), type(key[0]), long, lat, key[0], key[1])
                # d = calculate_distance(long, lat, key[1], key[0])
                # print(d, type(d))
                # print((float(key[0]) - float(long)) * (float(key[0]) - float(long))) + ((float(key[1]) - float(lat)) * (float(key[1]) - float(lat)))
                if calculate_distance(long, lat, key[0], key[1]) <= 100.0:
                    l[j][key].append(user["lianlus"][i])
                    st.add(((long, lat)))
    ans += 1

# Initialize a list to store category counts
all = []

for i in l:
    for key, value in i.items():
        all.append(Counter(value))

# Convert Counter objects in 'all' to regular dictionaries
new_all = []
for counter_obj in all:
    new_all.append(dict(counter_obj))

# Initialize a list to store category information
lis = []
categorys = new_all

# Pad the 'categorys' list to a length of 600 if necessary
if len(categorys) < 600:
    for k in range(600 - len(categorys)):
        ll = {}
        for l in range(1, 39):
            ll[l] = 0
        categorys.append(ll)

# Define a parameter
g = 39
bbi = 0
for bi in base_stations:
    t = []
    for key, value in categorys[bbi].items():
        t.append([int(key), value])
    for j in range(1, g):
        f = 0
        for k in range(len(t)):
            if j == t[k][0]:
                f = 1
                break
        if f:
            continue
        else:
            t.append([j, 0])
    sorted_lst = sorted(t, key=lambda x: x[0])
    tt = []
    for w in sorted_lst:
        tt.append(w[1])
    bi["category"] = tt
    bbi += 1

# Save the updated data back to the JSON file
file_path = f"Pre–deployed Strategy Generation Module/data/geolife.json"

with open(file_path, 'w') as file:
    json.dump(aall, file, indent=4, ensure_ascii=False)