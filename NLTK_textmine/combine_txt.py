'''Script to combine text by by file names of the same year'''

from os import walk
from collections import defaultdict
from pprint import pprint


FOLDER = '/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Full text'
OUTPUT_FOLDER = '/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Combined text/'

def create_mapping():
    mapping = defaultdict(list)
    for (dirpath, dirnames, fileNames) in walk(FOLDER):
        for fileName in fileNames:
            year = fileName.split('.')[1]
            mapping[year].append(fileName)
    return mapping


def concatenate_files(mapping):
    for key in mapping.keys():
        files = mapping[key]
        new_filename = OUTPUT_FOLDER + key + '.txt'
        with open(new_filename, 'w') as outfile:
            for fname in files:
                filePath = FOLDER + '/' + fname
                with open(filePath) as infile:
                    for line in infile:
                        outfile.write(line)



def main():
    mapping = create_mapping()
    pprint(mapping)
    concatenate_files(mapping)


if __name__ == "__main__":
    main()
