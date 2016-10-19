
from map import mapping
# walk through the os and get all files
# read each file in tern and go through line by line
# print lines that contain smell and the report name
from os import listdir
import nltk.data
import json

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium']
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
                pos_tag = get_pos_tag(sentence)
                # pos_tag is a list of words with their pos_tag
                # print(pos_tag)
                lemasRes = []
                for word in pos_tag:
                    # print(word)
                    lemas = lemmatize(word)
                    if lemas:
                        lemasRes.append(lemas[0])
                # print()
                lematizedSentence = (' '.join(lemasRes))
                # break
                # print(leamatizedSentence)

                for word in SMELL_WORDS:
                    if word in lematizedSentence.lower():
                        references.append(lematizedSentence)
    return references


def convert_pos(old_tag):
    if old_tag.startswith('J'):
        return 'adj'
    elif old_tag.startswith('V'):
        return 'v'
    elif old_tag.startswith('N'):
        return 'n'
    elif old_tag.startswith('R'):
        return 'adv'


def tokenize_to_sentence(sentence):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    # split into sentences
    result = parser.tokenize(sentence.strip())
    return result


def get_pos_tag(result):
    # split into a list of words in a sentence
    tokens = nltk.word_tokenize(result)
    pos_tagging = nltk.pos_tag(tokens)
    return pos_tagging

def lemmatize(pos_tag):
    wnl = nltk.WordNetLemmatizer()
    lemmas = []
    try:
        lemmas.append(wnl.lemmatize(pos_tag[0],convert_pos(pos_tag[1])))
    except:
        print(pos_tag[0])
    return lemmas


def saveObject(results):
    '''Save results dictionary as file'''
    with open('processed_results.txt', 'w') as outfile:
        json.dump(results, outfile)

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
        print(f)
        print(references)
        # if references:
        #     performAnalysis(f, references)
    # print(finalResult)
    # saveObject(finalResult)


if __name__ == '__main__':
    main()
