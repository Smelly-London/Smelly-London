#!/usr/bin/python3

#This script generates the data file required to be used with the leaflet software which is used to display the data on a map.

import sys
import os
import dataset

# Set the python path.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "python_utils"))

import csv_utilities
import json_utilities

def main():

    json_file = os.path.join("js", "london_districts_latlong_with_centroids.json")
    json_data = json_utilities.read_json_file(json_file)
    list_of_features = json_data["features"]

    db = dataset.connect('sqlite:///../../database/smells.sqlite')
    table = db['locations']

    for feature in list_of_features:
        location_name = feature["properties"]["name"]
        centroid_lat = feature["properties"]["lat_centre"]
        centroid_lon = feature["properties"]["long_centr"]
        polygon_coordinates = str(feature["geometry"]["coordinates"])

        table.insert({'location_name': location_name,
                      'centroid_lat': centroid_lat,
                      'centroid_lon': centroid_lon,
                      'polygon_coordinates': polygon_coordinates,})
                      # 'URL': result.url,
                      # 'MOH': result.mohRegion})


    # OUTPUT VISUALISATION DATA

    # Get data from database: group by borough, year and category (for all years).
    sql = "select Borough, MOH,  Category, Year, centroid_lat, centroid_lon, count(*) no_smells " \
          "from (select Borough, MOH, Category, Year, centroid_lat, centroid_lon from smells join locations on location_name=Borough)" \
          "group by Borough, Category, Year " \
          "order by Borough, Category, Year;"
    result = list(db.query(sql))
    print(result)
    res = []
    for row in result:
        res.append(row.values())

    # Print the data to a csv file (for use in leaflet).
    csv_file = os.path.join("smells_data.csv")
    header = ["location_name", "MOH", "smell_category", "year", "centroid_lat", "centroid_lon", "no_smells"]
    csv_utilities.list_of_tuples_to_csv(res, csv_file, header)

if __name__ == "__main__":
    main()
