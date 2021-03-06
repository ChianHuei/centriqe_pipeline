#!/usr/bin/env python
import os
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import json
import sys


# environment settings
URL = ""  #put url here
USERNAME = ""
USERPASSWORD = ""
INDEX = ""  # database's name. If the database doesn't exist, please create it before using this script.
TYPE = ""
############

def main():
    def generate_actions():
        for report in reports:
            yield report

    if len(sys.argv) < 2:
        print(f'Usage: one argument is required: inputFilePath.')
        return
    fp = sys.argv[1]
    if not os.path.isfile(fp):
        print(f'Error: inputFilePath is invalid.')
        return

    print("Loading dataset...")
    with open(fp, 'r') as f:
        tmp_dict = json.load(f)

    keyName = fp.split("/")[-1].split(".")[0]
    # this uses the file name as the key to get the list of docs
    try:
        reports = tmp_dict[keyName]  # list
    except:
        print(f'Error: dictionary reading failed.')
        return
    number_of_docs = len(reports)
    client = Elasticsearch(hosts=[URL], http_auth=(USERNAME, USERPASSWORD))

    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0

    for ok, action in streaming_bulk(client=client, index=INDEX, doc_type=TYPE, actions=generate_actions()):
        progress.update(1)
        successes += ok
    print(" %d/%d documents are uploaded." % (successes, number_of_docs))


if __name__ == "__main__":
    main()