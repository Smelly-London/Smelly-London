
'''This script datamines the reports by simple python operations to find smell related words in the reports and
categorises by smell types. Only nltk sentence tokenizer is used.
SQLite set up.
'''

from map2 import mapping
import concurrent.futures
from timeit import default_timer as timer

# walk through the os and get all files
# read each file in tern and go through line by line
from os import listdir
import nltk.data
import dataset

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium', 'effluvia']
REPORTS_DIR = '../Full text'


class SmellType(object):

    def __init__(self, name, synonyms):
        self.name = name
        self.synonyms = synonyms

class Smell(object):

    def __init__(self, borough, category, sentence, year, bID, url, mohRegion):
        self.borough = borough
        self.category = category
        self.sentence = sentence
        self.year = year
        self.bID = bID
        self.url = url
        self.mohRegion = mohRegion

    def __repr__(self):
        return "Smell(%s, %s, %s, %s)" % (repr(self.borough), repr(self.category), repr(self.sentence), repr(self.year))

    def __eq__(self, other):
        return repr(self) == repr(other)

# TEMPLATE: category = SmellType('category_name', ['synonym1', 'synonym2'])
# TODO: Create smell categories here
sewer = SmellType('sewer', ['sewer', 'drain', 'sewage', 'manhole', 'gully', 'gulley', 'gullies', 'cesspool', 'ventilator', 'ventilation'])
thames_water = SmellType('thames_water', ['water', 'thames', 'river'])
waste_rubbish = SmellType('waste_rubbish', ['refuse', 'dust', 'waste', 'dump', 'rubbish', 'offensive matter'])
waste_excrement = SmellType('waste_excrement', ['excrement', 'excreta', 'privy', 'privies', 'manure', 'dung'])
food = SmellType('food', ['food', 'yeast', 'pie', 'sauce', 'lemonade', 'bread', 'onion', 'vinegar', 'cherries', 'cherry', 'flavour', 'coffee', 'chocolate', 'cream', 'fruit', 'vegetable', 'salad', 'cheese',
                          'pickle', 'gherkin', 'fish', 'kipper', 'fillet', 'steak', 'mutton', 'tripe', 'cake', 'milk',
                          'yoghurt', 'butter', 'icing', 'caramel', 'canned', 'egg', 'preserve', 'cooking', 'veal',
                          'lamb', 'soup', 'peel', 'ham', 'sausage', 'cow', 'meat', 'sour', 'beef'])

trade = SmellType('trade', ['trade', 'business', 'laboratory', 'laboratories', 'copper', 'dry cleaning', 'launderette',
                            'laundrette', 'chemist', 'hide', 'bladder', 'glue', 'tannery', 'tanneries', 'rubber', 'gum', 'fat', 'oil', 'fellmonger', 'slaughter',
                            'costermonger', 'manure manufacture', 'ferment', 'butcher', 'burning'])
animal = SmellType('animal', ['animal', 'pig', 'stable', 'piggeries', 'piggery', 'manure', 'excrement', 'cowhouse'])
disinfectant = SmellType('disinfectant', ['disinfect', 'antiseptic'])
factory_fuel = SmellType('factory_fuel', ['factory', 'factories', 'industrial', 'rubber', 'naphtha', 'fuel', 'works'])
school = SmellType('school', ['school', 'lavatories', 'lavatory', 'discharging ears', 'playground'])
air_gas = SmellType('air_gas', ['gas', 'air', 'atmosphere', 'coal', 'carbonic acid', 'hydrogen', 'vapour', 'smoke', 'sulphide'])
decomposition = SmellType('decomposition', ['mortuary', 'coffin', 'decomposition', 'burial', 'dead', 'body', 'church', 'chapel'])
habitation = SmellType('habitation', ['house', 'flat', 'dwelling', 'cottage', 'room', 'home', 'ward', 'clothing', 'bedding', 'barge', 'cupola'])
no_smell = SmellType('no_smell', ['no offensive smell', 'smell-none', 'no smell', 'no nuisance from smell', 'absence of smell', 'no offensive odour', 'no bad odour', 'odourless', 'no disagreeable smell'])

def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def tokenize_to_sentence(sentence):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    # split into sentences
    result = parser.tokenize(sentence.strip())
    return result

def worker(file_name):
    dataminer = SmellDataMine()
    dataminer.process_file(file_name)
    return dataminer.results + dataminer.uncategorised


class SmellDataMine(object):

    def __init__(self):
        self.smellTypes = [sewer, thames_water, waste_rubbish, waste_excrement, trade, school, air_gas, factory_fuel,
                           decomposition, animal, food, habitation, no_smell, disinfectant]
        self.results = []
        self.uncategorised = []

    def save_to_database(self, results):
        # create table
        db = dataset.connect('sqlite:///../database/smells.sqlite')
        table = db['smells']
        for result in results:
            table.insert({'Category': result.category,
                          'Borough': result.borough,
                          'Year': result.year,
                          'Sentence': result.sentence,
                          'bID': result.bID,
                          'URL': result.url,
                          'MOH': result.mohRegion})

    def getUrl(self, bID):
        website = 'http://wellcomelibrary.org/item/'
        return website + bID

    def getMeta(self, fileName):
        splitReport = fileName.split('.')
        bID = splitReport[2]
        year = splitReport[1]
        url = self.getUrl(bID)
        try:
            region = mapping[bID][1]
            mohRegion = mapping[bID][0]
        except:
            # TODO there is a problem with mappings e.g Acton.1915.b19783905.txt. Region cannot be found
            print(fileName)
            return (None, None, None, None, None)
        return year, region, bID, url, mohRegion

    def process_file(self, fileName):
        path = REPORTS_DIR + '/' + fileName
        references = []
        year, region, bID, url, mohRegion = self.getMeta(fileName)
        if not all([year, region]):
            return

        # reassign global fns to local variable
        appendResults = self.results.append
        appendUncategorised = self.uncategorised.append

        with open(path) as f:
            for line in f:
                report_tokenized = tokenize_to_sentence(line)
                # break into sentences
                for sentence in report_tokenized:
                    for word in SMELL_WORDS:
                        if word in sentence.lower():
                            categories = self.categorise_sentence(sentence)

                            if categories:
                                for category in categories:
                                    o = Smell(region, category, sentence, year, bID, url, mohRegion)
                                    appendResults(o)
                                    break
                            else:
                                o = Smell(region, 'Uncategorised', sentence, year, bID, url, mohRegion)
                                appendUncategorised(o)
                                break

    def categorise_sentence(self, sentence):
        categories = []
        for category in self.smellTypes:
            for synonym in category.synonyms:
                if synonym in sentence.lower():
                    categories.append(category.name)
        return categories

def main():

    start = timer()

    files = get_file_names()
    smell_results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for file, smell in zip(files, executor.map(worker, files)):
            smell_results = smell_results + smell
    smell_results = [x for x in smell_results if x]

    end = timer()
    print(end - start)
    dataminer = SmellDataMine()
    dataminer.save_to_database(smell_results)

def delete_database():
    import os.path
    path = '../database/smells.sqlite'
    if os.path.isfile(path):
        os.remove(path)
        print('DB deleted!')
    else:
        print('No DB found for removal!')


if __name__ == '__main__':
    delete_database()
    main()
