
'''This script datamines the reports by simple python operations to find smell related words in the reports and
categorises by smell types. Only nltk sentence tokenizer is used.
SQLite set up.
'''

import progressbar
from map2 import mapping
import concurrent.futures
from timeit import default_timer as timer

# walk through the os and get all files
# read each file in tern and go through line by line
#problematic reports Acton.1915.b19783905.txt LondonCountyCouncil.1929.b1825276x.txt
#PortandCityofLondon.1975.b19884084.txt PortandCityofLondon.1976.b19884096.txt
#PortandCityofLondon.1978.b19884114.txt

from os import listdir
import nltk.data
import dataset

SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium', 'aroma', 'pungent', 'pungency']
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
# Smell categories here
sewer = SmellType('sewer', ['sewer', 'drain', 'sewage', 'manhole', 'gully', 'gulley', 'cesspool', 'ventilator', 'ventilation'])
thames = SmellType('thames', ['quay', 'sediment', 'thames', 'river'])
water = SmellType('water', ['water'])
waste_rubbish = SmellType('waste-rubbish', ['refuse', 'dust', 'waste', 'dump', 'rubbish', 'offensive matter'])
waste_excrement = SmellType('waste-excrement', ['excrement', 'excreta', 'privy', 'manure', 'dung'])
food = SmellType('food', ['food', 'stock', 'yeast', 'pie', 'sauce', 'lemonade', 'bread', 'onion', 'vinegar', 'cherry', 'flavour', 'coffee', 'chocolate', 'cream', 'fruit', 'vegetable', 'salad', 'cheese',
                          'pickle', 'tea', 'gherkin', 'fish', 'kipper', 'fillet', 'steak', 'mutton', 'tripe', 'cake', 'milk',
                          'yoghurt', 'butter', 'ice', 'caramel', 'can', 'egg', 'preserve', 'cook', 'veal',
                          'lamb', 'soup', 'peel', 'ham', 'sausage', 'cow', 'meat', 'sour', 'beef', 'rice', 'trough'])

trade = SmellType('trade', ['trade', 'business', 'laboratory', 'copper', 'dry cleaning', 'launderette',
                            'laundrette', 'chemist', 'hide', 'bladder', 'glue', 'tannery', 'tanneries', 'rubber', 'gum', 'fat', 'oil', 'fellmonger', 'slaughter',
                            'costermonger', 'manure manufacture', 'ferment', 'butcher', 'burning'])
animal = SmellType('animal', ['animal', 'pig', 'stable', 'piggeries', 'piggery', 'manure', 'excrement', 'cowhouse'])
disinfectant = SmellType('disinfectant', ['disinfect', 'antiseptic'])
factory_fuel = SmellType('factory-fuel', ['factory', 'factories', 'industrial', 'rubber', 'naphtha', 'fuel', 'works'])
school = SmellType('school', ['school', 'lavatories', 'lavatory', 'discharge', 'playground'])
air = SmellType('air', ['gas', 'air', 'atmosphere', 'coal', 'carbonic acid', 'hydrogen', 'vapour', 'smoke', 'sulphide'])
decomposition = SmellType('decomposition', ['mortuary', 'coffin', 'decomposition', 'burial', 'dead', 'body', 'church', 'chapel'])
habitation = SmellType('habitation', ['house', 'premise' 'flat', 'dwell', 'cottage', 'room', 'home', 'ward', 'clothing', 'bed', 'barge', 'cupola'])
absence_of_smell = SmellType('absence of smell', ['no offensive smell', 'no effluvium', 'smell-none', 'no smell', 'no nuisance from smell', 'absence of smell', 'no offensive odour', 'no bad odour', 'odourless', 'no disagreeable smell', 'devoid of aroma', 'no aroma','deficient in aroma', 'deficient of aroma'])


def get_file_names():
    """Retrieve file names"""
    fileNames = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames

def get_new_pos(old_pos):
    """This is a function that converts part-of-speech codes to abbreviated parts-of-speech"""
    new_pos = ""
    if old_pos.startswith('J'):
        new_pos = "a"
    elif old_pos.startswith('V'):
        new_pos = "v"
    elif old_pos.startswith('N'):
        new_pos = "n"
    elif old_pos.startswith('R'):
        new_pos = "r"
    else:
        new_pos = ""

    return new_pos

def lemmatize_sentence(sentence):
    """This is a fuction that takes a sentence and lemmatize the sentence."""
    lemmatized = []
    tokens = nltk.word_tokenize(sentence)
    pos_tagging = nltk.pos_tag(tokens)

    wnl = nltk.WordNetLemmatizer()

    for (word, pos) in pos_tagging:
        wordnet_pos = get_new_pos(pos)
        if wordnet_pos != "":
            lemma = wnl.lemmatize(word.lower(), wordnet_pos)
        else:
            lemma = word.lower()

        if word.istitle():
            lemma = lemma.capitalize()
        elif word.upper() == word:
            lemma = lemma.upper()

        # if word != lemma:
        #     print((word, lemma, pos, wordnet_pos))
        lemmatized.append(lemma)

    return " ".join(lemmatized)

def tokenize_to_sentence(text):
    parser = nltk.data.load('tokenizers/punkt/english.pickle')
    # split into sentences
    sentences = parser.tokenize(text.strip())
    return [lemmatize_sentence(sentence) for sentence in sentences]

def worker(file_name):
    """This is a function used to calculate the result in concurrent futures."""
    dataminer = SmellDataMine()
    dataminer.process_file(file_name)
    return dataminer.results + dataminer.uncategorised


class SmellDataMine(object):

    def __init__(self):
        self.smellTypes = [sewer, thames, water, waste_rubbish, waste_excrement, trade, school, air, factory_fuel,
                           decomposition, animal, food, habitation, absence_of_smell, disinfectant]
        self.results = []
        self.uncategorised = []

    def save_to_database(self, results):
        """Save results to the database."""
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
        """Return url for the website given bID."""
        website = 'http://wellcomelibrary.org/item/'
        return website + bID

    def getMeta(self, fileName):
        """Return the meta data for a given fileName e.g year, url, MOH, borough, bID.  """
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
        """ This is a function that categorises"""
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

    bar = progressbar.ProgressBar(max_value=len(files))
    processed_files = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for file, smell in zip(files, executor.map(worker, files)):
            smell_results = smell_results + smell
            processed_files += 1
            bar.update(processed_files)
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

