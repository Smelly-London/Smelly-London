#!/usr/bin/python3

# Contains CSV utilities

import csv
import os
import sqlite_utilities

def list_of_dicts_to_csv(dictionary, csvfile):
    """Writes a list of python dictionaries to a csv file where the headers in the csv are the dictionary keys. Outputs a csv file."""

    keys = dictionary[0].keys()
    print(keys)
    with open(csvfile, 'w') as outfile:
        writer = csv.DictWriter(outfile, list(keys))
#        for key, value in dictionary.items():
#            writer.writerow([key, value])
        writer.writeheader()
        writer.writerows(dictionary)

def list_of_tuples_to_csv(data, csvfile, header):
    '''Writes a list of tuples to a csv file. Allows user to define the column hheaders in the first line of the csv. Outputs a csv file.'''

    with open(csvfile, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(header)
        for row in data:
            csv_out.writerow(row)

if __name__ == '__main__':
 
    csvfile = '/home/jen/projects/smelly_london/test_data/dict_data.csv'
    print("OUTFILE:", csvfile)

    dictionary = sqlite_utilities.main() 
    list_of_dicts_to_csv(dictionary, csvfile)
