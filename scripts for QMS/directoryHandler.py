from iterateFiles import *
from pushDataToMongo import *
import sys
# variable settings
URI = ""  #put uri here such as 'mongodb://<username>:<password>@localhost:27017'
DBNAME = ""  #databse name if this database is no there, you have to create it before using this script
COLLECTION = ""  # collection name
############

def main():
    if len(sys.argv) < 2:
        print(f'Error: one more argument is required: directory path.')
        return
    dirPath = sys.argv[1]
    count = 1
    client = MongoClient(URI)

    for file in iterateFiles(dirPath):
        if pushDataToMongo(client, DBNAME, COLLECTION, file):
            count += 1

    print(f'Total: {count} files')




if __name__ == "__main__":
    main()
