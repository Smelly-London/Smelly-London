from os import listdir
import nltk.data

REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full text online'

reports = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
# print(reports)
result = {}
WNL = nltk.WordNetLemmatizer()
#sentence tokenizer


def wordTokenize(result):
    for sentence in result:
    	tokens = nltk.word_tokenize(sentence)
    	print (tokens)




def wordTokenize(result):
    for sentence in result:
        tokens = nltk.word_tokenize(sentence)
        for word in tokens:
            # posTagging([word])
            lemmaStuff(word)

def posTagging(word):
    pos_tagging = nltk.pos_tag(word)
    # nltk.ne_chunk(pos_tagging)
    print(pos_tagging)

def lemmaStuff(word):
    lemmas	= WNL.lemmatize(word)
    print(lemmas)

# posTagging(['dog'])

lemmaStuff('sings')

# for filename in reports[:1]:
#     filepath = REPORTS_DIR + '/' + filename
#     with open(filepath, 'r') as f:
#         text = f.read()
#         parser = nltk.data.load('tokenizers/punkt/english.pickle')
#         result = parser.tokenize(text.strip())
#         # print(result)
#         wordTokenize(result)
    # print(nltk.ne_chunk(pos_tagging))


#DL notes: word tokens, pos_tagged, lemmas to be used with sentence-tokenizer

#tokens = nltk.word_tokenize('Cat likes fish')
#print (tokens)

#pos_tagging = nltk.pos_tag(tokens)
#nltk.ne_chunk(pos_tagging)
#print (pos_tagging)
#print (nltk.ne_chunk(pos_tagging))

#DL notes: this is to lemmatize
#wnl = nltk.WordNetLemmatizer()
#lemmas	= [wnl.lemmatize(t) for t in tokens]
#print (lemmas)
