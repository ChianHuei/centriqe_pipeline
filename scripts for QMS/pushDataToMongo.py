#!/usr/bin/env python3
import os
from pymongo import MongoClient
import json
import sys


# variable settings
URI = ""  #put uri here such as 'mongodb://<username>:<password>@localhost:27017/'
DBNAME = ""  #databse name if this database is not there, you have to create it before using this script
COLLECTION = ""  # collection name
############

def pushDataToMongo(client, dbName, collectionName, filePath):

    with open(filePath, 'r') as f:
        dictionary = json.load(f)

    key = filePath.split("/")[-1].split(".")[0]

    try:
        dataList = dictionary[key]
    except:
        print(f'Error: unable to read the dictionary from {filePath}.')
        return

    db = client[dbName]
    collection = db[collectionName]
    try:
        collection.insert_many(dataList)
        print(f'{filePath} is done, {len(dataList)} documents are upload.')
        return True
    except Exception as err:
        print("uploading Fail: " + str(err))
        return False


def main():

    if len(sys.argv) < 2:
        print(f'Usage: one more argument is required: inputFilePath.')
        return

    fp = sys.argv[1]
    if not os.path.isfile(fp):
        print(f'Error: inputFilePath is invalid.')
        return

    client = MongoClient(URI)
    pushDataToMongo(client, DBNAME, COLLECTION, fp)


if __name__ == "__main__":
    main()