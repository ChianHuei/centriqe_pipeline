#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
import json
import collections


def transformHtmlTableToJson(inputPath, fileName):

    inputFile = open(inputPath,"r")

    table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(inputFile.read(), 'html.parser')("tr")]
    inputFile.close()

    dataName = fileName.split(".")[0]
    data = collections.OrderedDict()
    data[dataName] = []
    for row in table_data[1:]:
        context = collections.OrderedDict()
        for idx in range(len(table_data[0])):
            context[table_data[0][idx]] = row[idx]
        data[dataName].append(context)

    outputFileName = dataName+'.json'
    with open(outputFileName, 'w') as outfile:
        json.dump(data,outfile,indent=4)




def main():
    if len(sys.argv) < 2:
        print(f'Usage: one arguments are required: inputFilePath.')
        return
    inputFilePath = sys.argv[1]
    outputFileName = inputFilePath.split("/")[-1]

    transformHtmlTableToJson(inputFilePath, outputFileName)
    print(f"{inputFilePath} is Done!")


if __name__ == '__main__':
    main()