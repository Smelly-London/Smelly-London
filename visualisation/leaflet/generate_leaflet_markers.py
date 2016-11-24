#!usr/bin/python3

# Create the markers that are required for the leaflet map using the data output by generate_leaflet_data. The markers should include the lat, lon, {smell_ca1: 2, smell_cat2: 5, smell_cat3: 6}, date (which will be from the year of the report.

#TODO
# Do we need the place name and report url in the marker info as well so that info can be pulled up about it?

import csv
import sys
import os
import json

# Set the python path.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "python_utils"))

import csv_utilities

def year_to_date_time_format(year):
    '''Read in a year and output a string of the date and time in the format yyyy-mm-dd hh24:mm:ss+01'''

    year_string = str(year)
    formatted_year = year+"-01-01 00:00:00+01"

#    print(formatted_year)
    return formatted_year

def calculate_total_smells(data_list, location, year):
    ''' Read in each item of a list and calculate the total number of smells for each location in one year. Output the total number of smells.'''

    total_smells_location_year = 0

    for dictionary in data_list:
        if dictionary["location_name"] == location and dictionary["year"] == year:
            total_smells_location_year = total_smells_location_year + dictionary["no_smells"]

    return total_smells_location_year

def create_dict_of_smells(data_list, location, year):
    '''Read in each item of a list and output a dictionary of the smell categores and number of smells in each category.'''

    smell_list = []
    
    for dictionary in data_list:
        if dictionary["location_name"] == location and dictionary["year"] == year:
             smell_dictionary = {}
             category = dictionary["category"]
             no_smells = dictionary["no_smells"]
             smell_dictionary["name"] = category
             smell_dictionary["value"] =int(no_smells)
             smell_list.append(smell_dictionary)

    return smell_list

def main():

    # read in data csv file
    csvfile_in = os.path.join("..", "..", "data", "smells_data.csv")
    with open(csvfile_in, 'r') as infile:
        data_reader = csv.reader(infile, delimiter = ',')
        
        first_line = True
 
        data_list = []
        for row in data_reader:
            # skip header
            if first_line == True:
                first_line = False
                continue

            data_out = {}
            print(row)
            data_out["location_name"] = row[0]
            data_out["category"] = row[1]
            data_out["year"] = row[2]
            data_out["centroid_lat"] = float(row[3])
            data_out["centroid_lon"] = float(row[4])
#            print(row[5])
            data_out["no_smells"] = int(row[5])
    # convert year to date time format
            data_out["formatted_year"] = year_to_date_time_format(data_out["year"])

            # append the dictionaries to a list (which will allow iteration over items in list)      
            data_list.append(data_out)
#        print(data_list)

        # create output lists of data
        markers_information = []
        # create a list of distinct locations and years for the grouping of data.
        known_location_years = []

        # create output dictionary
        for item in data_list:
            loc_year = (item["location_name"], item["year"])

            if loc_year in known_location_years:
                continue

            # calculate the total number of smells per year for each location
            total_smells_location_year = calculate_total_smells(data_list, item["location_name"], item["year"])

            # create a dictionary of smell categories and assign number of smells.        
            smell_list = create_dict_of_smells(data_list, item["location_name"], item["year"])

            marker_information = {}
            marker_information["location_name"] = item["location_name"]
            marker_information["formatted_year"] = item["formatted_year"]
            marker_information["centroid_lat"] = item["centroid_lat"]
            marker_information["centroid_lon"] = item["centroid_lon"]
            marker_information["smells"] = smell_list
            marker_information["total_smells_location_year"] = total_smells_location_year

            # append the data to the list if there are no existing rows for the specific location and year.
            known_location_years.append(loc_year)
            markers_information.append(marker_information)

        print(markers_information)

        # convert the marker information to json and output to a json file
        json_file_out = os.path.join("..", "..", "data", "leaflet_markers.json")

        with open(json_file_out, 'w') as outfile:
            json.dump(markers_information, outfile)
 
if __name__ == "__main__":
    main()

