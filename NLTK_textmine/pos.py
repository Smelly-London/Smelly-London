"""
Part of speech processing
"""
import nltk

def pos():
    file_name = r'C:\Users\Michael\home\src\python\smelly_london\smelly_london\sample_data\b18220162_0_69.txt'
    with open(file_name) as f:
        text = f.read()
        tokens = nltk.word_tokenize(text)

        lemmatizer = nltk.WordNetLemmatizer()
        lemmas = [ lemmatizer.lemmatize(t) for t in tokens ]

        pos_tagging = nltk.pos_tag(tokens)

        return lemmas, tokens, pos_tagging, lemmatizer


if __name__ == "__main__":
        lemmas, tokens = pos()
        print(lemmas)

