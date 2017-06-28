"""
To go through each XML table file and look for Diphtheria

"""

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XMLParser
from glob import glob
from pprint import pprint

def get_diphteria_data():
	files = glob('/Users/deborah/Documents/scripts/python_work/project2016/MOH tables.xml/*/*/*.xml')

	bucket_1 = open("bucket_1.txt", "w")
	bucket_2 = open("bucket_2.txt", "w")
	bucket_3 = open("bucket_3.txt", "w")

	for file in files:
		try:
			parser = XMLParser(encoding="windows-1252")
			root = ET.parse(file, parser=parser).getroot()
		except:
			# Just ignore bad files
			pass

		# If diphtheria nowhere in xml, skip the whole file 
		if "diphtheria" not in str(ET.tostring(root).lower()):
			continue

		# Find all matching rows and colums
		rows = [[(e.text.strip() if e.text else "") for e in row.findall("*")] for row in root.findall("*//table/*/tr")]
		cols = list(map(list, zip(*rows)))
		diphtheria_rows = [row for row in rows if "diphtheria" in " ".join(row).lower()]
		diphtheria_cols = [col for col in cols if "diphtheria" in " ".join(col).lower()]

		data = {
			"publisher_loc": root.find("*//publisher-loc").text,
			"object_ID": root.find("*//object-id").text,
			"year": root.find("*//pub-date/year").text,
			"label": root.find("*//label").text,
			"title": root.find("*//book-title").text,
			# "table_headers": [(e.text.strip() if e.text else "") for e in root.findall("*//table/thead/tr/th")],
			"file": file,
		}

		if diphtheria_rows:
			pprint({"rows": diphtheria_rows, **data}, stream=bucket_1)
		if diphtheria_cols:
			pprint({"cols": diphtheria_cols, **data}, stream=bucket_2)
		if not diphtheria_rows and not diphtheria_cols:
			pprint(data, stream=bucket_3)
	bucket_1.close()
	bucket_2.close()
	bucket_3.close()

get_diphteria_data()
