from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XMLParser

filename = '/Users/deborah/Documents/scripts/python_work/project2016/MOH tables.xml/1920-1929.xml/Acton.1920.b19783504.xml/10197835000540034.xml'
#import pdb; pdb.set_trace()

parser = XMLParser(encoding="windows-1252")
root = ET.parse(filename, parser=parser).getroot()
#print(root)
#calling dir(root) to review the root object's methods
#print(dir(root))

#a list of Element objects: 'book', 'book-meta' & 'book-front'. 'book-front' contains the information I need.
#print(list(root))

#to get all 'table-wrap' children
data = root.findall('./book-front/table-wrap/*')
#print(data)

print(root.find('*//publisher-loc').text)
print(root.find('*//object-id').text)
print(root.find('*//label').text)
print(root.find('*//caption/p').text)

print([e.text for e in root.findall('*//table/thead/tr/th')])
print([e.text for e in root.findall('*//table/tbody/tr/td')])






# data = root.find('Data')

# all_data = []

# for table in data:
#     record = {}
#     for item in table:

#         lookup_key = list(item.attrib.keys())[0]

#         if lookup_key == 'Numeric':
#             rec_key = 'NUMERIC'
#             rec_value = item.attrib['Numeric']
#         else:
#             rec_key = item.attrib[lookup_key]
#             rec_value = item.attrib['Code']

#         record[rec_key] = rec_value
#     all_data.append(record)

# print all_data
