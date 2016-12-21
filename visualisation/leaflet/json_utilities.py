#!/usr/bin/python3

import json
import pprint
import sys
import os

# Set the python path.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "python_utils"))

json_file = os.path.join("..", "data", "london_districts_latlong_with_centroids.json")

def read_json_file(json_file):
    '''Read a json file.'''

    j_open = open(json_file)
    j = json.load(j_open)
#    pprint.pprint(j)

    return j

def dict_keys_of_json_file(json_data):
    ''' Get the dictionary keys within a json file.'''
    dict_keys = json_data.keys()
    print(dict_keys)

    return dict_keys

if __name__ == "__main__":
    json_data =  read_json_file(json_file)
    dict_keys = dict_keys_of_json_file(json_data)
    list_of_features = json_data["features"]
    for feature in list_of_features:
        print(feature["properties"]["name"], feature["properties"]["lat_centre"], feature["properties"]["long_centr"], feature["geometry"]["coordinates"])
#        print(feature["properties"]["name"], feature["properties"]["lat_centre"], feature["properties"]["long_centr"])    
