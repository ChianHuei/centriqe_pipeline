#!/usr/bin/env python3
import os
from pymongo import MongoClient
import json
import sys


# variable settings
URI = ""  #put uri here such as 'mongodb://<username>:<password>@localhost:27017/'
DBNAME = ""  #databse name if this database is no there, you have to create it before using this script
COLLECTION = ""  # collection name
############

def main():

    if len(sys.argv) < 2:
        print(f'Usage: one arguments are required: inputFilePath.')
        return

    fp = sys.argv[1]
    if not os.path.isfile(fp):
        print(f'Error: inputFilePath is invalid.')
        return

    print("Loading dataset...")
    with open(fp, 'r') as f:
        dictionary = json.load(f)

    keyName = fp.split("/")[-1].split(".")[0]

    try:
        dataList = dictionary[keyName]
    except:
        print(f'dictionary reading failed.')
        return

    client = MongoClient(URI)
    db = client[DBNAME]
    collection = db[COLLECTION]
    collection.insert_many(dataList)
    print(f'{len(dataList)} documents are upload.')


if __name__ == "__main__":
    main()