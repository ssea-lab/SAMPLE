import numpy as np
import importlib
from .utils.get_data import GetData
from prompts import GetPrompts
import types
import warnings
import sys


class pre_deployment():
    def __init__(self):
        getdata = GetData()
        self.get = getdata
        self.instances = getdata.get_resource_instances()
        self.prompts = GetPrompts()

    def get_valid_bin_indices(self, base: dict, services: list, methods: list) -> list:
        """Returns indices of bins in which item can fit."""
        valid_bin_indices = []
        for i in range(len(services)):
            for j in range(len(services[i]['locations'])):
             f = self.get.check_base_coverage(services[i]['locations'][j], base['location'], base['radius'])
             if(f):
                valid_bin_indices.append([i,j])

        lis = []

        for i in valid_bin_indices:
            if services[i[0]]['flags'][i[1]] == True:
                continue
            else:
                if services[i[0]]['lianlus'][i[1]] in base['allocated_services']:
                    services[i[0]]['flags'][i[1]] = True
                    continue
                else:
                    lis.append(i)
        bins = []

        for i in lis:
            name = services[i[0]]['lianlus'][i[1]]
            a = methods[name - 1]
            for j in range(len(a)):
                f = 1
                for k in range(3):
                    if a[j][k] > base['resource'][k]:
                        f = 0
                        break
                if f == 1:
                    bins.append({"name":name,
                                 "index_1":i,  #对应services中的第i[0]个用户第i[1]个微服务
                                 "location":services[i[0]]["locations"][i[1]],  #微服务的地理位置
                                 "index_3":j,
                                 "resource":a[j]
                                       })
        return bins

    def online_binpack(self, bases: list, services: list, methods: list, alg):
        for i, base in enumerate(bases):
            while 1:
                valid_bin_indices = self.get_valid_bin_indices(base, services, methods)

                if len(valid_bin_indices) == 0:
                    break

                priorities = alg.score(base, valid_bin_indices)
                priorities_index = priorities[0]
                best_service = valid_bin_indices[priorities_index]

                services[best_service['index_1'][0]]['flags'][best_service['index_1'][1]] = True
                base['allocated_services'].append(best_service['name'])
                for j in range(3):
                    base['resource'][j] -= best_service['resource'][j]
        return

    def evaluateGreedy(self, alg) -> float:
        methods = self.instances['methods']
        services = self.instances['user_requests']
        bases = self.instances['base_stations']
        self.online_binpack(bases, services, methods, alg)
        success_count = 0
        all = 0

        for i in services:
            all += len(i['flags'])
            for j in range(len(i['flags'])):
               if i["flags"][j] == True:
                success_count += 1
        fitness = success_count / all

        return fitness

    def evaluate(self, code_string):
        try:
            # Suppress warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                # Create a new module object
                heuristic_module = types.ModuleType("heuristic_module")

                # Execute the code string in the new module's namespace
                exec(code_string, heuristic_module.__dict__)

                # Add the module to sys.modules so it can be imported
                sys.modules[heuristic_module.__name__] = heuristic_module

                fitness = self.evaluateGreedy(heuristic_module)

                return fitness
        except Exception as e:
            return None