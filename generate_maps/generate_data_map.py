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
        borough_data_path = os.path.join(cwd, "..", "generate_boroughs", "location_data_all.csv")
        print("Reading {} locations file".format(borough_data_path))
        locations_file = open(borough_data_path, "r", newline="")

        locations_reader = csv.reader(locations_file)

        for line in locations_reader:
            self._locations[line[3]] = (line[0], line[1])

        print("Read {} different locations".format(len(self._locations)))

    def lookup(self, name):
        return self._locations.get(name, (None, None))


def create_carto_file():
    """ Creates a .csv file to be uploaded into http://carto.com with the smells. """

    location_finder = LocationFinder()

    filename = "carto.csv"
    csv_file = open(filename, "w", newline="")
    print("Output file: {}".format(filename))

    map_writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_ALL)

    map_writer.writerow(["longitude", "latitude", "date", "location_name", "number_of_smells"])

    missing_locations = []
    for borough_name, borough_information in smell_hits.res.items():
        for year, number_of_smells in borough_information.items():
            (latitude, longitude) = location_finder.lookup(borough_name)
            if latitude is not None and longitude is not None:
                date = "{}/01/01".format(year)
                map_writer.writerow([latitude, longitude, date, borough_name, number_of_smells])
            else:
                if borough_name not in missing_locations:
                    missing_locations.append(borough_name)

    print("Missing locations:", missing_locations)

if __name__ == "__main__":
    create_carto_file()
