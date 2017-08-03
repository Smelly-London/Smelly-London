"""
To go through diptheria data and get total number for all year
including mapping

"""

import csv
from NLTK_textmine.map2 import mapping

totals ={}

with open('table_stuff.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # print (row)

        location = row[0]
        bID = row[1].lower()

        if location == '':
            continue

        try:
            region = mapping[bID][1]
            mohRegion = mapping[bID][0]
        except:
            continue

        # print(location, bID, region, mohRegion)

        if region not in totals:
            totals[region] = 0
        totals[region] += 1

# print(totals)

csvfile = open('table_stuff_processed.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Borough', 'Total Diptheria'])
for region, (total) in totals.items():
    csvwriter.writerow([region, total])

csvfile.close()
