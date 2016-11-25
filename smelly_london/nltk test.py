# nltk test
import nltk

def convertPos(old_tag):
    if old_tag.startswith('J'):
        return 'adj'
    elif old_tag.startswith('V'):
        return 'v'
    elif old_tag.startswith('N'):
        return 'n'
    elif old_tag.startswith('R'):
        return 'adv'

tokens = nltk.word_tokenize('Fiat bought Chrysler')
pos_tagging = nltk.pos_tag(tokens)
print(pos_tagging)
wnl = nltk.WordNetLemmatizer()
lemmas	= [wnl.lemmatize(tag[0],convertPos(tag[1])) for tag in pos_tagging]
print(lemmas)
