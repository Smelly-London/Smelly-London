#!/usr/bin/env python3

# This script connects to and performs queries on an SQLite database using Python. 

# Jen Thomas, Oct 2016.

#########################################################

import sqlite3
import shutil

def connect_to_sqlite_db(sqlite_file):
    """ Connect to an SQLite database. Return a connection."""

    try:
        conn = sqlite3.connect(sqlite_file)
        cur = conn.cursor()
        return conn, cur
    except Error as e:
        print(e)

    return None

def close_sqlite_connection(conn):
    """ Close the connection to an SQLite database."""

    conn.close()

def sql_get_data_colnames(cur, sql, column_names):
    """Perform an SQL command to get data from an SQL database. Return data in a list of dictionaries with column headers as keys and their associated values."""
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

def get_data(conn, cur, sql):
    '''Get data from a database using the connection and cursor and defined sql.Output the data in a python list.'''

    cur.execute(sql)
    all_rows = cur.fetchall()

    return all_rows

def copy_sqlite_file(original_sqlite_file, destination_sqlite_file):
    '''Creates a copy of an sqlite file. Outputs an exact copy as an sqlite file.'''
    shutil.copy(original_sqlite_file, destination_sqlite_file)

def execute_sql(conn, cur, sql):
    ''' Execute some sql on the database.'''
  
    try:
        cur.execute(sql)
    except Error as e:
       print(e)

def main():

    sqlite_file = '/home/jen/projects/smelly_london/git/smelly_london/database'
    column_names = ['category', 'location', 'number_of_smells', 'centroid_lat', 'centroid_lon', 'id', 'year', 'sentence']
    sql = 'select {column_names} from (select Category category, Borough location, Id id, Year year, Sentence sentence, count(*) number_of_smells from smells group by Category, Borough having Year = "1904") join locations on location = name;'

    conn, cur = connect_to_sqlite_db(sqlite_file)
    data = sql_get_data_colnames(cur, sql, column_names)
    
    close_sqlite_connection(conn)    

    return data

if __name__ == '__main__':

    main()
