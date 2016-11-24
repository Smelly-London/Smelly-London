#!/usr/bin/python3

#This script generates the data file required to be used with the leaflet software which is used to display the data on a map. 

import sys
import os
import sqlite3

# Set the python path.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "python_utils"))

import csv_utilities
import json_utilities
import sqlite_utilities

def main():

    # Set up for copying the database.
    database_in = os.path.join("..", "..", "smelly_london", "database")
    database_out = os.path.join("..", "..", "data", "database_out")

    # Copy original database (so that more data can be added).
    sqlite_utilities.copy_sqlite_file(database_in, database_out)

    # Open the copy of the database.
    conn, cur = sqlite_utilities.connect_to_sqlite_db(database_out)

    # Read JSON file.
    json_file = os.path.join("..", "..", "data", "london_districts_latlong_with_centroids.json")
    json_data = json_utilities.read_json_file(json_file)

    # Creates a table to add the JSON file data to copied database.
    create_table_sql = """create table if not exists locations 
                          ( location_name text PRIMARY KEY,
                            centroid_lat numeric, 
                            centroid_lon numeric, 
                            polygon_coordinates text)"""

    sqlite_utilities.execute_sql(conn, cur, create_table_sql)

    # Add JSON data to database.
#    dict_keys = json_utilities.dict_keys_of_json_file(json_data)
    list_of_features = json_data["features"]

    for feature in list_of_features:
        location_name = feature["properties"]["name"]
        centroid_lat = feature["properties"]["lat_centre"]
        centroid_lon = feature["properties"]["long_centr"]
        polygon_coordinates = str(feature["geometry"]["coordinates"])
        
        print(feature["properties"]["name"], feature["properties"]["lat_centre"], feature["properties"]["long_centr"], feature["geometry"]["coordinates"])
        
        cur.execute("insert into locations values (?, ?, ?, ?)", (location_name, centroid_lat, centroid_lon, polygon_coordinates))

    conn.commit()
    conn.close()

    #### Generate data.####

    # TEST 1 - all data from 1858 with only totals of smells (to get markers on map and change size of marker).
    
    # Get data from database: group by borough and year for 1858 (test for visualisation).
    conn, cur = sqlite_utilities.connect_to_sqlite_db(database_out)

    sql = "select Borough, Year, centroid_lat, centroid_lon, count(*) no_smells from (select Borough,  Year, centroid_lat, centroid_lon from smells join locations on location_name=Borough) group by Borough,  Year having Year='1858' order by Borough, Year;"
    data_list = sqlite_utilities.get_data(conn, cur, sql)
    print(data_list)

    # Print the data to a csv file (for use in leaflet).
    csv_file = os.path.join("..", "..", "data", "smells_data_1858_summary.csv")
    header = ["location_name", "year", "centroid_lat", "centroid_lon", "no_smells"]
    csv_utilities.list_of_tuples_to_csv(data_list, csv_file, header)
    
    # TEST 2 - all data from 1858 with smells in categories (to create piecharts with categories and change radius with total number of smells)

    # Get data from database: group by borough, year and category and test firstly with 1858.
    conn, cur = sqlite_utilities.connect_to_sqlite_db(database_out)

    sql = "select Borough, Category, Year, centroid_lat, centroid_lon, count(*) no_smells from (select Borough, Category, Year, centroid_lat, centroid_lon from smells join locations on location_name=Borough) group by Borough, Category, Year having Year='1858' order by Borough, Category, Year;"
    data_list = sqlite_utilities.get_data(conn, cur, sql)
    print(data_list)

    # Print the data to a csv file (for use in leaflet).
    csv_file = os.path.join("..", "..", "data", "smells_data_1858.csv")
    header = ["location_name", "smell_category", "year", "centroid_lat", "centroid_lon", "no_smells"]
    csv_utilities.list_of_tuples_to_csv(data_list, csv_file, header)

    # OUTPUT VISUALISATION DATA

    # Get data from database: group by borough, year and category (for all years).
    conn, cur = sqlite_utilities.connect_to_sqlite_db(database_out)

    sql = "select Borough, Category, Year, centroid_lat, centroid_lon, count(*) no_smells from (select Borough, Category, Year, centroid_lat, centroid_lon from smells join locations on location_name=Borough) group by Borough, Category, Year order by Borough, Category, Year;"
    data_list = sqlite_utilities.get_data(conn, cur, sql)
    print(data_list)

    # Print the data to a csv file (for use in leaflet).
    csv_file = os.path.join("..", "..", "data", "smells_data.csv")
    header = ["location_name", "smell_category", "year", "centroid_lat", "centroid_lon", "no_smells"]
    csv_utilities.list_of_tuples_to_csv(data_list, csv_file, header)

if __name__ == "__main__":
    main()
    
