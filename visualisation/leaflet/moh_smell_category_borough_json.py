#To create json file for displaying Borough, MOH and smell categories/ numbers on the leaflet map

import json
import dataset
import os



def connect_to_db():
	db = dataset.connect('sqlite:///../../database/smells.sqlite')
	return db

def get_sql():
	"""Get sql query"""
	sql = """select Year, Borough, MOH, bID, Category, count(*)
		from smells
		   group by Year, Borough, MOH, bID, Category"""

	return sql

def get_results_from_db(sql):
	db = connect_to_db()
	res = db.query(sql)
	return res

def save_as_json(results):
	"""convert the information to json and output to a json file"""
	json_file_out = os.path.join("data", "deb_test.json")
	print('saving to path: {}'.format(json_file_out))

	with open(json_file_out, 'w') as outfile:
	    json.dump(results, outfile)


def main():
	db = connect_to_db()
	sql = get_sql()
	results = get_results_from_db(sql)
	# print(list(results))
	# for result in results:
	# 	print(result)
	results = list(results)
	res = {}
	for ord_dic in results:
		year = ord_dic['Year']
		borough = ord_dic['Borough']
		cat = ord_dic['Category']
		count = ord_dic['count(*)']
		moh = ord_dic['MOH']
		bID = ord_dic['bID']
		key = borough + " " + year
		if key not in res:
			res[key] = {}
		if moh not in res[key]:
			res[key][moh] = {
				'bID': bID,
				'smells': []
			}
		res[key][moh]["smells"].append({
		    'cat': cat, 
		    'count': count,
		})

	save_as_json(res)


if __name__ == "__main__":
    main()
