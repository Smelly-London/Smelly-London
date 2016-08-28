#!/usr/bin/env python3

import smell_hits
import pprint
import csv
import sys
import os

class LocationFinder:
    def __init__(self):
        self._locations = {}
        self._read_locations()

    def _read_locations(self):
        cwd = os.path.dirname(__file__)
        borough_data_path = os.path.join(cwd, "..", "generate_boroughs", "all_borough_data.csv")
        print("Reading {} locations file".format(borough_data_path))
        locationsfile = open(borough_data_path, "r", newline="")

        locationsreader = csv.reader(locationsfile)

        for line in locationsreader:
            self._locations[line[3]] = (line[0], line[1])

        print("Read {} different locations".format(len(self._locations)))

    def lookup(self, name):
        return self._locations[name]

def create_carto_file():
    """ Creates a .csv file to be uploaded into http://carto.com with the smells. """

    locationFinder = LocationFinder()

    filename = "carto.csv"
    csvfile=open(filename, "w", newline="")
    print("Output file: {}".format(filename))

    mapwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_ALL)

    mapwriter.writerow(["longitude", "latitude", "year", "location_name", "number_of_smells"])

    for borough_name, borough_information in smell_hits.res.items():
        for year, number_of_smells in borough_information.items():
            (latitude, longitude) = locationFinder.lookup(borough_name)
            mapwriter.writerow([latitude, longitude, year, borough_name, number_of_smells])

if __name__ == "__main__":
    create_carto_file()
