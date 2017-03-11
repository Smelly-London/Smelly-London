#!/usr/bin/env python3

# This script connects to and performs queries on an SQLite database using Python. 

import dataset


def connect_to_db():
    """ Connect to an SQLite database. Return a connection."""
    db = dataset.connect('sqlite:///../database/smells.sqlite')
    return db


def sql_get_data_colnames(cur, sql, column_names):
    """Perform an SQL command to get data from an SQL database. Return data in a list of dictionaries with
     column headers as keys and their associated values."""
    print(sql)
    sql = sql.replace('{column_names}', ",".join(column_names))
    cur.execute(sql)
    all_rows = cur.fetchall()

    data = []
    for row in all_rows: 
        d={}
        i=0
        for column_name in column_names:
            d[column_name] = row[i]
            i=i+1

        data.append(d)
    
    return data

def get_data(db, sql):
    '''Get data from a database using the connection and cursor and defined sql.Output the data in a python list.'''
    table = db['smells'] 
    return all_rows

def copy_sqlite_file(original_sqlite_file, destination_sqlite_file):
    '''Creates a copy of an sqlite file. Outputs an exact copy as an sqlite file.'''
    shutil.copy(original_sqlite_file, destination_sqlite_file)


def main():
    db = dataset.connect('sqlite:///../database/smells.sqlite')

    sqlite_file = '/home/jen/projects/smelly_london/git/smelly_london/database'
    column_names = ['category', 'location', 'number_of_smells', 'centroid_lat', 'centroid_lon', 'id', 'year', 'sentence']
    sql = 'select {column_names} from (select Category category, Borough location, Id id, Year year, Sentence sentence, count(*) number_of_smells from smells group by Category, Borough having Year = "1904") join locations on location = name;'

    conn, cur = connect_to_sqlite_db(sqlite_file)
    data = sql_get_data_colnames(cur, sql, column_names)
    
    close_sqlite_connection(conn)    

    return data

if __name__ == '__main__':

    main()
