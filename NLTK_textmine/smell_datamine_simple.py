
'''This script datamines the reports by simple python operations to find smell related words in the reports.

Only nltk sentence tokenizer is used.

Uses prettyprint to display the results nicely.
'''


from map import mapping
# walk through the os and get all files
# read each file in tern and go through line by line
# print lines that contain smell and the report name
from os import listdir
import nltk.data
import json
from pprint import pprint as pp

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium', 'effluvia']
REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'

global finalResult
finalResult = {}


def add_to_dic(d, report, rDate, val):
    d.setDefault(report, []).append(val)
    return d


def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def process_file(fileName):
    path = REPORTS_DIR + '/' + fileName
    references = []
    with open(path) as f:
        for line in f:
            # break into sentences
            report_tokenized = tokenize_to_sentence(line)

            for sentence in report_tokenized:
                for word in SMELL_WORDS:
                    if word in sentence.lower():
                        references.append(sentence)
    return references


def tokenize_to_sentence(sentence):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    # split into sentences
    result = parser.tokenize(sentence.strip())
    return result

def saveObject(results):
    '''Save results dictionary as file'''
    with open('processed_results.txt', 'w') as outfile:
        json.dump(results, outfile)

def performAnalysis(fileName, references):
    '''Create the results output'''

    # splits a fileName into :['Acton', '1900', 'b19783358', 'txt']
    splitReport = fileName.split('.')
    bID = splitReport[2]
    year = splitReport[1]

    try:
        region = mapping[bID]
    except:
        return

    if region in finalResult:
        nestedDic = finalResult[region]
    else:
        nestedDic = {}

    nestedDic[year] = references
    finalResult[region] = nestedDic

    # if nestedDic[splitReport[1]]:
    #     val = nestedDic[splitReport[1]]
    #     nestedDic[splitReport[1]] = len(references) + val
    # else:
    #     if len(references):
    #         nestedDic[splitReport[1]] = len(references)
    # # nestedDic.setDefault(splitReport[1], 0).__add__(len(references))
    # result[region] = nestedDic

# print(result)
# for k,v in result.iteritems():

def main():
    fileNames = get_file_names()
    fileNames = fileNames[:10]
    for f in fileNames:
        references = process_file(f)
        # print(f)
        # print(references)
        if references:
            performAnalysis(f, references)
    pp(finalResult)
    save_to_database()
    # saveObject(finalResult)


if __name__ == '__main__':
    main()
