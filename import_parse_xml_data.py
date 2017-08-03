"""
To go through each XML table file and look for Diphtheria

"""

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XMLParser
from glob import glob
from pprint import pprint
import csv



def save_csv_entry(csvwriter, header, rows, metadata):
	csvwriter.writerow([
		metadata["publisher_loc"],
		metadata["object_ID"],
		metadata["year"],
		metadata["label"],
		metadata["title"],
		metadata["file"],
	])
	csvwriter.writerow([""] * 6 + header)
	for row in rows:
		csvwriter.writerow([""] * 6 + row)


def get_diphteria_data():
	files = glob('/Users/deborah/Documents/scripts/python_work/project2016/MOH tables.xml/*/*/*.xml')

	# bucket_1 = open("bucket_1.txt", "w")
	# bucket_2 = open("bucket_2.txt", "w")
	# bucket_3 = open("bucket_3.txt", "w")

	csvfile = open("table_stuff.csv", 'w')
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["publisher_loc", "object_ID", "year", "label", "title", "file"])

	for file in files:
		try:
			parser = XMLParser(encoding="windows-1252")
			root = ET.parse(file, parser=parser).getroot()
		except:
			# Just ignore bad files
			pass

		document_text = str(ET.tostring(root).lower())
		# If diphtheria nowhere in xml, skip the whole file 
		if "diphtheria" not in document_text:
			continue
		# If death/mortality nowhere in xml, skip the whole file 
		if "death" not in document_text and "mortality" not in document_text:
			continue
		# It doesn't handle colspans/rowspans yet
		if "colspan" in document_text or "rowspan" in document_text:
			continue
		# to only extract cause of death
		if "causes of death" in document_text and "cause of death" not in document_text:
			continue

		# Find all matching rows and colums
		rows = [[(e.text.strip() if e.text else "") for e in row.findall("*")] for row in root.findall("*//table/*/tr")]
		cols = list(map(list, zip(*rows)))
		diphtheria_rows = [row for row in rows[1:] if "diphtheria" in " ".join(row).lower()]
		diphtheria_cols = [col for col in cols[1:] if "diphtheria" in " ".join(col).lower()]

		metadata = {
			"publisher_loc": root.find("*//publisher-loc").text,
			"object_ID": root.find("*//object-id").text,
			"year": root.find("*//pub-date/year").text,
			"label": root.find("*//label").text,
			"title": root.find("*//book-title").text,
			# "table_headers": [(e.text.strip() if e.text else "") for e in root.findall("*//table/thead/tr/th")],
			"file": file,
		}

		if diphtheria_rows:
			save_csv_entry(csvwriter, rows[0], diphtheria_rows, metadata)
			# pprint({"rows": diphtheria_rows, "header_row": rows[0], **metadata}, stream=bucket_1)
		if diphtheria_cols:
			save_csv_entry(csvwriter, cols[0], diphtheria_cols, metadata)
			# pprint({"cols": diphtheria_cols, "header_col": cols[0], **metadata}, stream=bucket_2)
		# if not diphtheria_rows and not diphtheria_cols:
		# 	pprint(metadata, stream=bucket_3)
	# bucket_1.close()
	# bucket_2.close()
	# bucket_3.close()
	csvfile.close()

get_diphteria_data()
