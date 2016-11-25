
'''This script datamines the reports by simple python operations to find smell related words in the reports and categorises by smell types.

Can print categorised and uncategorised.

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
from collections import defaultdict
import dataset

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium', 'effluvia']
REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'


class SmellType(object):

    def __init__(self, name, synonyms):
        self.name = name
        self.synonyms = synonyms

class Smell(object):

    def __init__(self, borough, category, sentence, year):
        self.borough = borough
        self.category = category
        self.sentence = sentence
        self.year = year

# TEMPLATE: category = SmellType('category_name', ['synonym1', 'synonym2'])
# TODO: Create smell categories here
sewer = SmellType('sewer', ['sewer', 'drain', 'sewage', 'manhole', 'gully', 'gulley', 'gullies' 'cesspool', 'ventilation'])
thames_water = SmellType('thames_water', ['water', 'thames', 'river'])
waste_rubbish = SmellType('waste_rubbish', ['refuse', 'dust', 'waste', 'dump', 'rubbish', 'offensive matter'])
waste_excrement = SmellType('waste_excrement', ['excrement', 'excreta', 'privy', 'privies', 'manure', 'dung'])
food  = SmellType('food', ['food', 'flavour', 'coffee', 'chocolate', 'cream', 'fruit', 'vegetable', 'salad', 'cheese', 'pickle', 'gherkin', 'fish', 'kipper', 'fillet', 'steak', 'mutton', 'tripe', 'cake', 'milk', 'yoghurt', 'butter', 'icing', 'caramel', 'canned', 'egg', 'preserve', 'cooking', 'veal', 'lamp', 'soup', 'ham', 'sausage', 'cow', 'meat', 'sour'])
trade  = SmellType('trade', ['trade', 'business', 'laboratory', 'laboratories', 'copper', 'dry cleaning', 'launderette', 'laundrette', 'chemist', 'glue', 'gum', 'fat', 'oil', 'fellmonger', 'slaughter', 'costermonger', 'manure manufacture', 'ferment', 'butcher', 'burning'])
animal = SmellType('animal', ['animal', 'stable', 'piggeries', 'piggery', 'manure', 'excrement', 'cowhouse'])
factory_fuel = SmellType('factory_fuel', ['factory', 'factories', 'industrial', 'rubber' 'naphtha', 'fuel', 'works'])
school = SmellType('school', ['school', 'lavatories', 'lavatory', 'discharging ears'])
air_gas = SmellType('air_gas', ['gas', 'air', 'atmosphere', 'coal', 'carbonic acid', 'hydrogen', 'vapour', 'smoke', 'sulphide'])
decomposition = SmellType('decomposition', ['mortuary', 'burial', 'dead', 'body', 'church', 'chapel'])
habitation = SmellType('habitation', ['house', 'room', 'home', 'ward', 'barge', 'cupola'])
no_smell = SmellType('no_smell', ['no offensive smell', 'absence of smell', 'no offensive odour', 'odourless', 'no disagreeable smell'])

def add_to_dic(d, report, rDate, val):
    d.setDefault(report, []).append(val)
    return d


def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def tokenize_to_sentence(sentence):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    # split into sentences
    result = parser.tokenize(sentence.strip())
    return result



def saveObject(results):
    '''Save results dictionary as file'''
    with open('processed_results.txt', 'w') as outfile:
        json.dump(results, outfile)


def performAnalysis(self, fileName, references):
    '''Create the results output'''

    # splits a fileName into :['Acton', '1900', 'b19783358', 'txt']
    splitReport = fileName.split('.')
    bID = splitReport[2]
    year = splitReport[1]

    try:
        region = mapping[bID]
    except:
        return

    if region in self.finalResult:
        nestedDic = self.finalResult[region]
    else:
        nestedDic = {}

    nestedDic[year] = references
    self.finalResult[region] = nestedDic

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

def get_categorised_results(results_list, categories):
    for category in categories:
        for result in results_list:
            if result.category == category:
                pp({category: {result.borough: {result.year:result.sentence}}})

def get_uncategorised_results(results_list):
    for result in results_list:
        pp({'uncategorised': {result.borough: {result.year:result.sentence}}})

def get_all_results(categorised_results, uncategorised_results):
    results = categorised_results + uncategorised_results
    for result in results:
        pp({result.borough: {result.year:result.sentence}})


class SmellDataMine(object):

    def __init__(self):
        self.smellTypes = [sewer, thames_water, waste_rubbish, waste_excrement, food, trade, animal, factory_fuel, school, air_gas, decomposition, habitation, no_smell]
        self.uncategorised = []
        self.fileNames = get_file_names()
        self.results = []
        self.db = dataset.connect('sqlite:///database')

    def save_to_database(self, results):
        # create table
        table = self.db['smells']
        for result in results:
            try:
                table.insert({'Category': result.category,
                              'Borough': result.borough,
                              'Year': result.year,
                              'Sentence': result.sentence})
            except:
                print(result)

    def run(self):
        for fileName in self.fileNames:
            references = self.process_file(fileName)
            # if references:
            #     performAnalysis(f, references)

        # pp(self.finalResult)
        # saveObject(finalResult)

    def getMeta(self, fileName):
        splitReport = fileName.split('.')
        bID = splitReport[2]
        year = splitReport[1]
        try:
            region = mapping[bID]
        except:
            # TODO there is a problem with mappings e.g Acton.1915.b19783905.txt. Region cannot be found
            print(fileName)
            return (None, None)
        return year, region

    def process_file(self, fileName):
        path = REPORTS_DIR + '/' + fileName
        references = []
        year, region = self.getMeta(fileName)
        if not all([year, region]):
            return

        with open(path) as f:
            for line in f:
                # break into sentences
                report_tokenized = tokenize_to_sentence(line)

                for sentence in report_tokenized:
                    for word in SMELL_WORDS:
                        if word in sentence.lower():
                            category = self.categorise_sentence(sentence)
                            if category:
                                o = Smell(region, category, sentence, year)
                                self.results.append(o)
                            else:
                                o = Smell(region, 'Uncategorised', sentence, year)
                                self.uncategorised.append(o)

    def categorise_sentence(self, sentence):
        for category in self.smellTypes:
            for synonym in category.synonyms:
                if synonym in sentence.lower():
                    return category.name



def main():
    runner = SmellDataMine()
    runner.run()
    print(runner.results)
    # categories = [category.name for category in runner.smellTypes]

    # run this to get categorised smell results
    # get_categorised_results(runner.results, categories)

    # run this to get uncategorised smell results
    # get_uncategorised_results(runner.uncategorised)

    # run this to get all smell results
    # get_all_results(runner.results, runner.uncategorised)

    results = runner.results + runner.uncategorised
    runner.save_to_database(results)


if __name__ == '__main__':
    main()