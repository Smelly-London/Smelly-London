
from map import mapping
# walk through the os and get all files

# read each file in tern and go through line by line

# print lines that contain smell and the report name
from os import listdir

def addToDic(d, report, rDate, val):
    d.setDefault(report, []).append(val)
    return d

REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'
SMELL_WORDS = ['smell', 'stench', 'stink', 'odour', 'sniff', 'effluvium']

reports = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
result = {}

for report in reports:
    path = REPORTS_DIR + '/' + report
    references = []
    with open(path) as f:
        for line in f:
            content = line.split('.')
            for line in content:
                for word in SMELL_WORDS:
                    if word in line.lower():
                        references.append(line)

    splitReport = report.split('.')
    bID = splitReport[2]
    try:
        region = mapping[bID]
    except:
        print bID
        continue

    if result.has_key(region):
        nestedDic = result[region]
    else:
        nestedDic = {}
    
    if nestedDic.has_key(splitReport[1]):
        val = nestedDic[splitReport[1]]
        nestedDic[splitReport[1]] = len(references) + val
    else:
        if len(references):
            nestedDic[splitReport[1]] = len(references)
    # nestedDic.setDefault(splitReport[1], 0).__add__(len(references))
    result[region] = nestedDic

print(result)
# for k,v in result.iteritems():
