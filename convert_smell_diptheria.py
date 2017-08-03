"""
To go through json data and get total number of smells and sewer (and to combine with diptheria) for all year
Json file already mapped

"""
import json
import csv


totals = {}

with open('visualisation/leaflet/data/leaflet_markers.json') as json_data:
    d = json.load(json_data)
    # print(d)

    for f in d:
    	# print(f)
    	location = f["location_name"]
    	smells = {smell["name"]:smell["value"] for smell in f["smells"]}
    	total = sum(smells.values())
    	sewer = smells.get("sewer", 0)

    	if location not in totals:
    		totals[location] = [0, 0]
    	totals[location][0] += total
    	totals[location][1] += sewer
    	# print(location)
    	# print(smells)
    	# print(total)
    	# print(sewer)
    	# print("")

#print(totals)

csvfile = open('totals_smells_sewer.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Borough', 'Total Smells', 'Total Sewer'])
for location, (total, sewer) in totals.items():
    csvwriter.writerow([location, total, sewer])

csvfile.close()
