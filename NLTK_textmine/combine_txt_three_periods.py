'''Script to combine text by by file names of main three periods: 1848-1900; 1901-1948; 1949-1978'''

from os import walk
import os
from collections import defaultdict
from pprint import pprint


FOLDER = '/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Full text'
OUTPUT_FOLDER = '/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Combined text_by_period/'

def create_mapping():
    mapping = defaultdict(list)
    for (dirpath, dirnames, fileNames) in walk(FOLDER):
        for fileName in fileNames:
            year = fileName.split('.')[1]
            year_bucket = get_year_bucket(year)
            if not year_bucket:
                continue

            mapping[year_bucket].append(fileName)
    return mapping

def get_year_bucket(year):
    try:
        year = int(year)
    except:
        return None

    if year in range(1848, 1901):
        return '1848-1900'
    if year in range(1901, 1950):
        return '1901-1948'
    if year in range(1949, 1979):
        return '1949-1978'
    return year
        

def concatenate_files(mapping):
    for year in mapping.keys():
        files = mapping[year]
        new_filename = OUTPUT_FOLDER + year + '.txt'
        with open(new_filename, 'w') as outfile:
            for fname in files:
                filePath = FOLDER + '/' + fname
                with open(filePath) as infile:
                    for line in infile:
                        outfile.write(line)



def main():
    mapping = create_mapping()
    # pprint(mapping)
    concatenate_files(mapping)


if __name__ == "__main__":
    main()
