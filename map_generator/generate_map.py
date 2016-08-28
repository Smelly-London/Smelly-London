#!/usr/bin/env python3

import smell_hits
import pprint
import csv
import sys

def latitude_longitude_from_location_name(location_name):
    locationsfile = open("borough_feature_data.csv", "r", newline="")

    locationsreader = csv.reader(locationsfile)

    for line in locationsreader:
        if location_name == line[3]:
            return(line[0], line[1])

    return (0, 0)

def main():
    csvfile=open("carto.csv", "w", newline="")

    mapwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_ALL)

    mapwriter.writerow(["longitude", "latitude", "year", "location_name", "number_of_smells"])

    for borough_name, borough_information in smell_hits.res.items():
        for year, number_of_smells in borough_information.items():
            (latitude, longitude) = latitude_longitude_from_location_name(borough_name)
            mapwriter.writerow([latitude, longitude, year, borough_name, number_of_smells])

    sys.exit(0)

if __name__ == "__main__":
    main()
