"""
Top level script for the smelly_london project
"""

## Notes on coding conventions:
##
## Comments beginning ### are notes to explain my coding approach (sort of tutorial comments)
## They should be stripped before publication.
##
## For now, I'm mostly developing this in a single file. Later, I'll refactor it so this file
## only contains main()
##

import glob
import os.path
import collections
from search_terms import SearchTerms
import re
import nltk


def get_report_ids(data_path):
    """
    Assuming pages have names like "b18220162_0_23.txt", "b18220162" would be the report ID

    :param data_path: Directory which is searched for *.txt
    :return: List of report IDs.
    """
    pattern = os.path.join(data_path, '*_*_*.txt')
    pages = glob.glob(pattern)
    return { os.path.basename(page).split('_')[0] for page in pages }


def get_smell_words(file_name):
    with open(file_name) as f:
        search_terms = SearchTerms(file_name)
        return { term[0] for term in search_terms.terms }

        # return { line.strip() for line in f }

### I've used a named tuple to make it explicit that the hit context is invariant.
### In principle, named tuples should also be slightly more memory efficient - and we have a lot of data!
### We probably won't be able to hold all our data in memory at once.
HitContext = collections.namedtuple(
    'HitContext', (
        'term', # Currently the word, perhaps later the specification of the hit term (normalised? attributes?)
        'page', # The page number from scanning. This may not be the page number in the text.
        'context', # the sentence containing the text. (Or we could make this a configurable number of characters/words)
    )
)

ReportData = collections.namedtuple(
    'ReportData', (
        'report_id', # Base name for the file
        'district', # Normalised (all descriptions of a district in the source give the same value)
        'year', # e.g. 1874
        'hits', # A tuple of HitContext
    )
)


def get_district(line):
    """
    If line contains the name of a borough, return it's normalised form

    :param line:
    :return:
    """
    """
    :param line:
    :return:
    """
    # TODO:
    # Cope with new lines / pages after the word "borough"
    # Normalise
    # Cope with multi-word boroughs

    lc_line = line.lower()
    if not "borough of " in lc_line:
        return None
    m = re.search("borough of (\w+)", lc_line)
    if not m:
        return None
    return m.group(1).capitalize()



def parse_page_pos(smell_words, last_page, this_page, next_page):
    """

    :param smell_words:
    :param last_page:
    :param this_page:
    :param next_page:
    :return:
    """


def parse_page(smell_words, last_page, this_page, next_page):
    """
    Search for hits, the district name and report year

    For now, I'll ignore the previous and next pages.
    :param smell_words: Definition of our search terms, currently a set of words
    :param last_page: Preceding page for context. May be None.
    :param this_page: Page to parse
    :param next_page: May be None.
    :return: district (normalised string), year (int), hits (list of HtContext)
    """
    hits = []
    year = None
    district = None

    with open(this_page) as f:
        last_line = ""
        m = re.search("_\d+_(\d+)\.txt$", this_page)
        assert m, this_page
        page_number = int(m.group(1)) ### Will fail if m is Null - which should be impossible

        for line in f:
            if not district: # For now, the first "borough of"
                district = get_district(line)

            words = line.strip().split(' ')
            for word in words:
                if not year: # For now, the year is the first 4 digit number beginning 19 or 20 in the report
                    ### This rather horrible match expression looks for 4 digits beginning 19 or 20,
                    ### optionally discarding a single following letter or digit . "1942," would match as "1942".
                    m = re.match('((?:19|20)\d\d)\W?', word)
                    if m:
                        year = int(m.group(1))

                if word in smell_words:
                    context = last_line + " " + line
                    hits.append( HitContext(word, page_number, context) )
            last_line = line

    return district, year, hits


def get_text_file_names(data_path, report_id):
    """
    Return text file names, sorted by report ID and page number

    :param data_path:
    :return: sorted text file names
    """
    def make_key(name):
        bits = name[:-4].split('_') # Exclude .txt
        return int(bits[-1])

    ret = glob.glob(os.path.join(data_path, report_id + '_*_*.txt'))
    ret.sort(key = make_key)

    return ret


def read_report(report_id, data_path, smell_words):
    """
    Turn a report into data

    Extract the district, year, locations and key phrases from the report

    We have both XML files and report files. Early versions of this function just
    parse the text files. Later we'll use the XML too, for example the position of text
    tells us if a hyphen represents a broken word.
    :param report_id: The base name of the report, excluding path
    :param data_path: Directory
    :param smell_words:
    :return: ReportData
    """
    district = None
    year = 0
    hits = []

    text_file_names = get_text_file_names(data_path, report_id)
    page_context = zip( [None] + text_file_names[:-1], text_file_names, text_file_names[1:] + [None] )
    for last_page, this_page, next_page in page_context:
        ### For now, I'm passing in file names.
        ### In future, I imagine passing in a single cleaned-up page, including only an appropriate fragment of the
        ### preceding and succeeding pages.
        d, y, h = parse_page(smell_words, last_page, this_page, next_page)
        if d and not district:
            # TODO: Error handling if we have more than one possible district
            district = d
        if y and not year:
            # TODO: Error handling
            year = y

        hits.extend(h)

    return ReportData(report_id, district, year, tuple(hits))


def make_report(reports):
    """
    Display the output. Some day, as a map, but for now as a text report
    :param reports: tuple(district, year) : ReportData
    :return: None
    """
    for key,report in reports.items():
        district, year = key
        smells = []
        for hit in report.hits:
            smells.append (hit.term)
        print (district,":", year,":", smells)
    print(reports.keys())


def run(data_path, smell_word_filename):
    smell_words = get_smell_words(smell_word_filename)

    ## The right sort of collection depends on how we use it.
    # Possible future form: Pandas data table with indexes by borough, year, keyword etc
    reports = {} # tuple(district, year) : ReportData

    for report_id in  get_report_ids(data_path):
        report = read_report(report_id, data_path, smell_words)

        # I'm assuming reports are unique to a borough and year.
        # If not, I want to know as it could lead to double-counting
        assert (report.district, report.year,) not in reports

        reports[(report.district, report.year,)] = report

    return(reports) ### Useful if running it at the command line so you can get the data structure and play with it


def hits_in_context_report(reports):
    for _, report in reports.items():
        print( "\n\n{}, {}".format(report.district, report.year))
        for hit in report.hits:
            pos = hit.context.find(hit.term)
            context_region = 30
            start = max(pos-context_region, 0)
            finish = min(pos+context_region, len(hit.context))
            print("{} {} p.{:3} {:20} {}".format(report.report_id, report.year, hit.page, hit.term, hit.context[start:finish]))


if __name__ == "__main__":
    DATA_PATH = r"../sample_data"
    # SMELL_WORD_FILENAME = r"smell_words.txt"
    SMELL_WORD_FILENAME = r'C:\Users\Michael\Dropbox\MOH 2016 Project\smell_ENG_vs2.txt'

    reports = run(DATA_PATH, SMELL_WORD_FILENAME)
    make_report(reports)
    hits_in_context_report(reports)