# Script to lemmatize the files of the Smelly London project
# To adapt this for smell_datamine_multiprocessing.py 
# March 2017

# Import modules:

from os import listdir
from os.path import isfile, join
import os
import codecs
import nltk
from nltk.tokenize import sent_tokenize

# Files and directories:

dir_in = "../Full text"
dir_out = "../lemmatized"
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# Function that converts part-of-speech codes to abbreviated parts-of-speech:

def get_new_pos(old_pos):
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

# -------------------------
# Text processing
# -------------------------

files = [f for f in listdir(dir_in) if isfile(join(dir_in, f)) and f.endswith(".txt")]

count = 0
for file in files:
    count += 1
    if count < 3:
        file_out = file.replace(".txt", "_lemmas.txt")
        print(str(file))
        text = codecs.open(os.path.join(dir_in, file), 'r', encoding="utf-8").read()

        # Write output file:
        output = open(os.path.join(dir_out, file_out), "w")

        # Sentence segmentation:
        sentences = sent_tokenize(text)

        for sentence in sentences:
            # Word tokenization:
            tokens = nltk.word_tokenize(sentence)

            # Part-of-speech tagging:
            pos_tagging = nltk.pos_tag(tokens)

            # Lemmatization:
            wnl = nltk.WordNetLemmatizer()

            for w in pos_tagging:
                print(str(w))
                word = w[0].lower()
                if get_new_pos(w[1]) in ["adv", "adj", "n", "v", "pro"]:
                    lemma = wnl.lemmatize(word, get_new_pos(w[1]))
                else:
                    lemma = w[0]

                if w[0].istitle():
                    lemma = lemma.capitalize()
                elif w[0].upper() == w[0]:
                    lemma = lemma.upper()

                output.write(lemma + "\t" + w[1] + "\n")

            output.write("\n")
        output.close()



