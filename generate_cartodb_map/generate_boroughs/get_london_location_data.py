#!/usr/bin/env python3

# This script reads a csv file of locations in London (generally referred to as boroughs, but historically can be parish councils, district councils and other authoritative bodies depending on the historical period). Thereafter it finds the positions of each of these locations using an API (printing them to a csv file) and if no data are found, prints a list of the locations that are not found. 

# This is a first attempt to prove the methods, so the data extracted from the API is not necessarily consistent and for the missing locations, positions were added manually afterwards, from various sources. 

# DATA SOURCES
# The list of locations are from the list of Ministry of Health Reports from present day back to 1850.
# API - https://web.archive.org/web/20160402224319/http://edina.ac.uk/unlock/places/deep.html
# The API is still running but is unsupported. It was compiled by the project, "Digital Exposure of English Place-Names" (DEEP). 

# TODO
# Improve selection of data from API (prioritise)
# Try a different API / data source
# When removing duplicates, ensure that similar names remain (there are some locations that have the same name but are from different parts of London, e.g. St. Mary's)

# Jen Thomas & Carles Pina
# August 2016
#############################################################################

# import modules required
import json # to deal with the output format
import pprint # makes the output of json more easily readable
import csv
import requests # module to use APIs
import os


def read_csv(csv_file):
    """read csv file into a list, skipping the header line"""

    data = []
    first_line = True

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if first_line == True:
                first_line = False
                continue

            data.append(row)

    return data


def get_location_names(csv_data):
    """get a list of location names from the csv data and output as a list"""

    location_names = []

    for item in csv_data:
        location_names.append(item[2])

    return location_names


def remove_duplicates(duplist):
    """remove all duplicates from a list, so that only one of each item remains and output a list"""

    nondup_list = list(set(duplist))

    return nondup_list


def remove_white_space(list):
    """remove leading or trailing white space from the outer sides of a list and output the list"""

    nospace_list = []

    for item in list:
        stripped = item.strip()

        nospace_list.append(stripped)

    return nospace_list


def get_location_data(location_list):
    """iterate through the list of locations and extract data from the API for each one. output the data in json format."""

    location_data_json = {}
    address = 'http://unlock.edina.ac.uk/ws/search?name=' # address of API
    country_code = 'GB'
    dups = set([x for x in location_list if location_list.count(x) > 1])
    print(dups)

    for location in location_list:
        url = address+location+"&countrycode="+country_code+"&format=json"
        print("Trying URL ",location_list.index(location)," of ",len(location_list),":", url)

        data = requests.get(url)
        data_json = data.json()
        print("DATA JSON FOR:", location)
        pprint.pprint(data_json)
        print('============')
        location_data_json[location] = data_json

    return location_data_json


def get_list_of_values_from_dict(location_data_dictionary, key):
    """get a list of values for a certain key from a dictionary and output into a list."""
    list_of_key_values = []

    for location_name, location_data in location_data_dictionary.items():
        for feature in location_data['features']:
            pprint.pprint(feature)
            value = feature['properties'][key]
            if value not in list_of_key_values:
                list_of_key_values.append(value)

    return list_of_key_values


def get_london_location_data(location_data_dictionary):
    """get position data from dictionary according to conditions. Output a list of dictionaries."""

    location_feature_data = [] # create a list of dictionaries containing position data for each location

    for location_name, location_data in location_data_dictionary.items():

        for feature in location_data['features']:
            if ('properties' in feature and 'adminlevel2' in feature['properties'] and 'featuretype' in feature['properties'] \
                 and feature['properties']['adminlevel2'] == 'Greater London' and (feature['properties']['featuretype'] == 'Populated Place' or \
                 feature['properties']['featuretype'] == 'Section of Populated Place')) or \
               ('properties' in feature and 'featuretype' in feature['properties'] and feature['properties']['featuretype'] == 'London Borough') or \
               ('properties' in feature and 'featuretype' in feature['properties'] and feature['properties']['featuretype'] == 'London Borough (Royal)'): # select various critieria that are used to get data

                location_feature_data_dict = {} # create a dictionary for each location
                location_feature_data_dict["name"] = location_name
                centroid = feature['properties']['centroid'] # this is one variable within the dictionary: split into lat / lon
                location_feature_data_dict["centroid_lon"] = centroid.split(", ")[0]
                location_feature_data_dict["centroid_lat"] = centroid.split(", ")[1]
                location_feature_data_dict["feature_type"] = feature['properties']['featuretype']
                location_feature_data_dict["source"] = 'http://unlock.edina.ac.uk'
                location_feature_data.append(location_feature_data_dict)
                break # once one position has been found and added to the list, find data for the next location. See TODO.

    return location_feature_data


def write_dict_to_csv(list_of_dictionaries, output_file):
    """write a list of dictionaries to a csv file."""

    fieldnames = ['centroid_lon', 'centroid_lat', 'feature_type', 'name', 'source']

    with open(output_file, 'w', newline = '') as f:
        w = csv.DictWriter(f, fieldnames, quoting = csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(list_of_dictionaries)


def output_dict_elements_with_value(dictionary, value):
    """output elements from a dictionary that have a certain value. Output in a list"""
    locations_with_no_data= []
    for location_name in dictionary:
        count = dictionary[location_name]

        if count == value:
            locations_with_no_data.append(location_name)

    return locations_with_no_data


def get_missing_locations(found_locations, all_locations):
    missing_locations = []

    for wanted_location in all_locations:
        found = False
        for found_location in found_locations:
            if found_location['name'] == wanted_location:
                found = True
                break

        if not found:
            missing_locations.append(wanted_location)

    return missing_locations


def main():
    # read the data from the csv into a variable.
    cwd = os.path.dirname(__file__)
    print("CWD ", cwd)
    london_location_path = os.path.join(cwd, "london_borough_year_list_moh.csv")
    print(london_location_path)
    csv_data = read_csv(london_location_path)

    # create a list of the locations
    location_names = get_location_names(csv_data)

    # read list without leading or trailing white space into a variable.
    location_names = remove_white_space(location_names)

    # read list of non duplicate location names into a list.
    location_list = remove_duplicates(location_names)

    print("location list: ", location_list)
    print("Number of locations: ", len(location_list))

    location_data = get_location_data(location_list)

    key = 'featuretype' # used here to find relevant data (includes things such as London Borough, Towns etc)

    key_values = get_list_of_values_from_dict(location_data, key)
    print('KEY VALUES: ', key_values)

    location_feature_data = get_london_location_data(location_data)

    cwd = os.path.dirname(__file__)
    output_location_data_path = os.path.join(cwd, "location_data_generated.csv")
    write_dict_to_csv(location_feature_data, output_location_data_path)

    list_of_locations_with_no_data = get_missing_locations(location_feature_data, location_list)

    print("LOCATIONS WITH NO DATA FROM API")
    pprint.pprint(list_of_locations_with_no_data)


if __name__ == "__main__":
    main()