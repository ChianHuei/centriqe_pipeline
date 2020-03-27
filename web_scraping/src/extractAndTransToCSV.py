#!/usr/bin/env python3

"""
extractAndTransToCSV.py is to extract data from HTML contents and store it as a csv file.
    :param inputFilePath: string (file path)
    :param outputFileName: string (file path)
    :param mainClass: string ( the main class of CSS that should be pulled out)
    :param subClass: string (assign only one sub-class under main class to extract.)
"""
from bs4 import BeautifulSoup
import csv
import sys
import os.path

def extractToCSV(inputFilePath: str, outputFilePath: str, mainClass:str, subClasses) -> None:
    """
    extracting data from html context and transforming data into csv format.
    :param inputFilePath: string (file path)
    :param outputFilePath: string (file path) if it is an existing regular file, append at EOF.
    :param mainClass: string ( the main class of CSS that should be pulled out)
    :param subClasses: dict {"label_1":"CSS_class", "label_2": "CSS_class_2"}
            (assign the sub-classes under main class to extract.)
    :return:
    """
    addHeader = False
    if not os.path.isfile(outputFilePath):
        outputFile = open(outputFilePath,"w")
        addHeader = True
    else:
        outputFile = open(outputFilePath, "a+")
    outputFile_writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    inputFile = open(inputFilePath,"r")
    soup = BeautifulSoup(inputFile.read(), 'html.parser')
    inputFile.close()
    results = soup.findAll(class_=mainClass)

    if addHeader:
        csvHeader = []
        if subClasses:
            for label in subClasses:
                csvHeader.append(label)
        outputFile_writer.writerow(csvHeader)

    for result in results:
        r = []

        if subClasses:
            for label, cl in subClasses.items():
                extract = result.find(class_=cl)
                if extract:
                    r.append(extract.text)
                else:
                    r.append("")
        else:
            try:
                r.append(result.text)
            except:
                print(f'Invalid CSS main class.')
                r.append("")

        outputFile_writer.writerow(r)

    outputFile.close()


def main():
    if len(sys.argv) < 5:
        print(f'Error: four arguments are required- inputFilePath, outputFileName, mainClass, and subClass.')
        return
    intermediateFile = sys.argv[1]
    outputFileName = sys.argv[2]
    mainClass = sys.argv[3]
    subClass = sys.argv[4]
    extractToCSV(intermediateFile, outputFileName, mainClass, {"subClass": subClass})
    print("Done!")


if __name__ == '__main__':
    main()

