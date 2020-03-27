#!/usr/bin/env python3
"""
pullDataFromWebsite.py is a simple web crawler, pulling data from a web-page and saving it in a csv file.
three arguments are required, which are a file containing URLs, a json-like file containing classes, and a outputFilePath.
"""
import requests
from bs4 import BeautifulSoup
import csv
import sys
import json
from extractHTML import getHtmlFile
from extractAndTransToCSV import extractToCSV
import os


def readOutDict(inputFilePath: str) ->dict:
    """
    reading string out of a file, and converting it to a dictionary.
    the content of the file should be {main_class:{label_1:subClass_, label_2 subClass_2,...}}
    :param inputFilePath:string
    :return:
    """
    if not os.path.isfile(inputFilePath):
        print(f'Error:{inputFilePath} is not valid. ')
        return {}

    inputFile = open(inputFilePath, "r")
    try:
        tmp = json.loads(inputFile.read())
    except:
        print(f'Error:the format of {inputFilePath} is not valid. ')
        inputFile.close()
        return {}
    inputFile.close()
    return tmp


def main():
    if len(sys.argv) < 4:
        print(f'Usage: three more arguments are required. a file containing URLs,'
              f' a file containing classes, and a outputFilePath')
        return
    firstFilePath = sys.argv[1]
    classDict = readOutDict(sys.argv[2])
    outputPath = sys.argv[3]

    if not classDict:
        return
    for key in classDict:
        mainCl = key
        subClDict = classDict[mainCl]
        break
    if type(subClDict) != dict:
        print(f'the format of subclasses should be a dictionary.')
        return
    if not os.path.isfile(firstFilePath):
        print(f'{firstFilePath} is not valid.')
        return
    intermediateFile = "html_main_class.txt"
    f = open(firstFilePath,"r")
    count = 1
    for address in f:
        if getHtmlFile(address, intermediateFile, mainCl):
            extractToCSV(intermediateFile, outputPath, mainCl, subClDict)
            print(f'page {count} is done.')
            count += 1
    print("All done!")


if __name__ == '__main__':
    main()

