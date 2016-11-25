
from map import mapping
# walk through the os and get all files
# read each file in tern and go through line by line
# print lines that contain smell and the report name
from os import listdir
import nltk.data

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium']
REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'

global finalResult
finalResult = {}

def addToDic(d, report, rDate, val):
    d.setDefault(report, []).append(val)
    return d

def getFileNames():
    '''Retrieve file names'''
    fileNames = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames

def processFile(fileName):
    path = REPORTS_DIR + '/' + fileName
    references = []
    with open(path) as f:
        for line in f:
            report_tokenized = tokenize(line)
            for scentence in report_tokenized:
                for word in SMELL_WORDS:
                    if word in scentence.lower():
                        references.append(scentence)
    return references

def tokenize(sentence):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    result = parser.tokenize(sentence.strip())
    return result

def performAnalysis(fileName, references):
    '''Create the resuts output'''
    # splits a fileName into :['Acton', '1900', 'b19783358', 'txt']
    splitReport = fileName.split('.')
    bID = splitReport[2]
    year = splitReport[1]

    try:
        region = mapping[bID]
    except:
        return
        # print bID

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
    # tokenize(s)
    fileNames = getFileNames()
    # f1 = fileNames[0]
    # processFile(f1)
    fileNames = fileNames[:100]
    for f in fileNames:
        references = processFile(f)
        if references:
            performAnalysis(f, references)
    print(finalResult)

if __name__ == '__main__':
    main()