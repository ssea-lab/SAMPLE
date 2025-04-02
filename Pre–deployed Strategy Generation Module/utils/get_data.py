import math
import numpy as np
import json
import pickle

class GetData():
    def __init__(self) -> None:
        with open('D:\\EoH-main\\examples\\shanghai2\\file\\shanggai_0(3000).json', 'r') as file:
            self.datasets = json.load(file)

    def calculate_distance(self, lon1, lat1, lon2, lat2):
        R = 6371000

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(dLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c

        return distance

    def check_base_coverage(self, user_location, base_location, base_radius):
        distance = self.calculate_distance(user_location[0], user_location[1], base_location[0], base_location[1])
        return distance <= base_radius

    def check_resource_availability(self, base_stations, user_request, valid_indices):
        k = 0
        lst = []
        for i in valid_indices:
            k = 0
            f = 1
            for j in base_stations[i]['resources']:
                if j < user_request[k]:
                    f = 0
                    break
                else:
                    k += 1
            if f==1:
                lst.append(i)
        return lst

    def check_service_availability(self, base_stations, user_request, valid_indices):
        if len(valid_indices) > 1 :
            for i in valid_indices:
                for j in base_stations[i]["allocated_services"]:
                    if j == user_request["service"]:
                        return []
            return valid_indices
        elif len(valid_indices) == 0:
            return []
        elif len(valid_indices) == 1:
            for i in base_stations[valid_indices[0]]["allocated_services"]:
                if i == user_request["service"]:
                    return []
            return [valid_indices[0]]

    def get_resource_instances(self):
        resource_instances=self.datasets
        return resource_instances