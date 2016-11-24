#!usr/bin/python3

def sort_list(list_in):
    '''Sort a list on a field and output the list in that order.'''

    sorted_data = sorted(list_in, key=lambda item: item["formatted_year"])

    return sorted_data


