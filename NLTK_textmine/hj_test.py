

# walk through the os and get all files

# read each file in tern and go through line by line

# print lines that contain smell and the report name
from os import listdir

REPORTS_DIR = '/Users/deborah/Documents/scripts/python_work/project2016/Full Text Online'

reports = [f for f in listdir(REPORTS_DIR) if f.endswith('txt')]

for report in reports:
    path = REPORTS_DIR + '/' + report

    with open(path) as f:
    	for line in f:
        	content = line.split('.')
	        for line in content:
	            if 'raw bacon' in line.lower():
	            	print (line)

	# for line in f.split(''):
	# 	print line
	# 	break
		# if 'smell' in line.lower():
		# 	print line
		# 	