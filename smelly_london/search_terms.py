"""
Parse a file defining search terms and related grammatical information
"""

class SearchTerms:
    def __init__(self, file_name):
        self.categories = {} # ID -> name
        self.terms = {} # term -> list of category ID; term is a tuple of words

        with open(file_name) as f:
            sections_parsers = ( self.__parse_category, self.__parse_term ).__iter__()
            section_parser = None

            for line_number, line in enumerate(f):
                try:
                    line = line.strip()
                    if line == '%':
                        section_parser = next(sections_parsers)
                        continue

                    if line == '':
                        continue

                    section_parser(line)
                except:
                    print("line:", line_number, line )
                    raise


    def __parse_category(self, line):
        id, name = line.split('\t')
        self.categories[int(id)] = name

    def __parse_term(self, line):
        term, ids = line.split('\t')
        # The spec says IDs are tab-separated but the actual file has commas
        self.terms[ tuple(term.split(' ')) ] = [ int(id) for id in ids.split(',')]


if __name__ == "__main__":
    file_name = r'C:\Users\Michael\Dropbox\MOH 2016 Project\smell_ENG_vs2.txt'
    st = SearchTerms(file_name)
    print(st.categories)
    print(st.terms)

