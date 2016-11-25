# saving in python

dictToSave = {'banana': 1, 'kale':3}

import json
with open('data_smoothie.txt', 'w') as outfile:
    json.dump(dictToSave, outfile)


with open('data_smoothie.txt') as infile:
    d = json.load(infile)

print(d)