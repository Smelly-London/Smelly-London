

# walk through the os and get all files

# read each file in tern and go through line by line

# print lines that contain smell and the report name
from os import listdir

REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'

reports = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]
result = {}

for report in reports:
    path = REPORTS_DIR + '/' + report
    references = []
    with open(path) as f:
        for line in f:
            content = line.split('.')
            for line in content:
                if 'smell' in line.lower():
                    references.append(line)

    splitReport = report.split('.')

    result[report] = len(references)

print(result)