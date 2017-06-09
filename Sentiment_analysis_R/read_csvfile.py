import csv

csvfile = open('sentiment-moh.csv', 'rb')
reader = csv.reader(csvfile)

for row in reader:
    print (row)