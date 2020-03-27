#!/usr/bin/env python3

import sys
import mysql.connector
import csv
from mysql.connector import Error

def insertVariblesIntoTable(connection, reviewer_name,from_city,rating,contributions,helpful,text,stay_date):
    try:

        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO tpd_review_with_rating (reviewer_name,from_city,rating,contributions,helpful,text,stay_date) 
                                VALUES (%s, %s,%s, %s, %s, %s,%s) """

        recordTuple = (reviewer_name,from_city,rating,contributions,helpful,text,stay_date)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        print("Record inserted successfully into tpd_review_with_rating table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))



#insertVariblesIntoTable(2, 'Area 51M', 6999, '2019-04-14')
#insertVariblesIntoTable(3, 'MacBook Pro', 2499, '2019-06-20')

def main():
    if len(sys.argv) < 2:
        print(f'Error: one arguments is required- file to insert to mysql.')
        return
    file_path = sys.argv[1]
    try:
        connection = mysql.connector.connect(
            host='ls-49e29f9801ff832c186e4ebc55b93b1094509dd6.cgwsutpfaoyn.us-west-2.rds.amazonaws.com',
            database='test1',
            user='insight',
            password='L`w8yjX9IshQ!D|HgA<*6EjwZwkOBZ1H')
    except:
        print("conncet error.")
        return

    csvFile = open(file_path,"r")
    csv_reader = csv.reader(csvFile)
    for row in csv_reader:
        insertVariblesIntoTable(connection, row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    csvFile.close()
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

if __name__ == '__main__':
    main()