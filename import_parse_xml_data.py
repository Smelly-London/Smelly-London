"""
To go through each XML table file and look for Diphtheria

"""

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XMLParser
from glob import glob
from pprint import pprint

def get_diphteria_data():
	files = glob('/Users/deborah/Documents/scripts/python_work/project2016/MOH tables.xml/*/*/*.xml')
	for file in files:
		try:
			parser = XMLParser(encoding="windows-1252")
			root = ET.parse(file, parser=parser).getroot()
		except:
			# Just ignore bad files
			pass
		rows = [[(e.text.strip() if e.text else "") for e in row.findall("td")] for row in root.findall("*//table/tbody/tr")]
		diphtheria_rows = [row for row in rows if "diphtheria" in " ".join(row).lower()]
		if diphtheria_rows:
			#print(file)
			data = {
				"publisher_loc": root.find("*//publisher-loc").text,
				"year": root.find("*//pub-date/year").text,
				"label": root.find("*//label").text,
				"title": root.find("*//book-title").text,
				"table_headers": [(e.text.strip() if e.text else "") for e in root.findall("*//table/thead/tr/th")],
				"table_contents": diphtheria_rows,
				"file": file,
			}
			pprint(data)

get_diphteria_data()
