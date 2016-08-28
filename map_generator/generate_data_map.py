#!/usr/bin/env python3

import smell_hits
import csv
import os


class LocationFinder:
    def __init__(self):
        self._locations = {}
        self._read_locations()

    def _read_locations(self):
        cwd = os.path.dirname(__file__)
        borough_data_path = os.path.join(cwd, "..", "generate_boroughs", "all_borough_data.csv")
        print("Reading {} locations file".format(borough_data_path))
        locations_file = open(borough_data_path, "r", newline="")

        locations_reader = csv.reader(locations_file)

        for line in locations_reader:
            self._locations[line[3]] = (line[0], line[1])
            print("test locations_reader")

        print("Read {} different locations".format(len(self._locations)))

    def lookup(self, name):
        return self._locations[name]


def create_carto_file():
    """ Creates a .csv file to be uploaded into http://carto.com with the smells. """

    location_finder = LocationFinder()

    filename = "carto.csv"
    csv_file = open(filename, "w", newline="")
    print("Output file: {}".format(filename))

    map_writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_ALL)

    map_writer.writerow(["longitude", "latitude", "year", "location_name", "number_of_smells"])

    for borough_name, borough_information in smell_hits.res.items():
        for year, number_of_smells in borough_information.items():
            (latitude, longitude) = location_finder.lookup(borough_name)
            map_writer.writerow([latitude, longitude, year, borough_name, number_of_smells])


if __name__ == "__main__":
    create_carto_file()