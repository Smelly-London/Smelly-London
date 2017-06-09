from collections import Counter
from os import walk
from pprint import pprint

FOLDER = '/Users/deborah/Documents/scripts/python_work/project2016/smelly_london/Full text'


def do_count_for_borough():
    res = []
    for (dirpath, dirnames, fileNames) in walk(FOLDER):
        for fileName in fileNames:
            if '.txt' in fileName:
                res.append(fileName.split('.')[0])
    pprint(Counter(res))

def do_count_for_year():
    res = []
    for (dirpath, dirnames, fileNames) in walk(FOLDER):
        for fileName in fileNames:
            if '.txt' in fileName:
                res.append(fileName.split('.')[1])
    pprint(Counter(res))

def main():
    do_count_for_borough()
    do_count_for_year()

if __name__ == "__main__":
    main()
