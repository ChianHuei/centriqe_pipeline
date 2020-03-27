#!/usr/bin/python3

"""
pullDataFromWebsite.py is a simple web crawler, pulling data from a web-page and saving it in a csv file.
"""
import requests
from bs4 import BeautifulSoup
import csv
import sys

def getHtmlFile(address: str, outputFileName: str, classToExtract=None) -> None:
    """
    scraping html context down from internet and opening a new file to store it.
    Caution: if the outputFileName exists, the old file will be replaced.
    :param address: string (http address)
    :param outputFileName: string (file path)
    :param classToExtract: string (assign the class name of CSS that should be extracted.
                                   The default is to scrape all html tags.)
    """
    res = requests.get(address)
    if res.status_code != requests.codes.ok:
        print(f'Request of {address} failed with status code: {res.status_code}.')
        return

    if classToExtract:
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.findAll(class_=classToExtract)
        content = str(results)
    else:
        content = res.text

    outputFile = open(outputFileName,"w")
    outputFile.write(content)
    outputFile.close()
    print("html file is done.")

def readOutDict(inputFilePath: str) ->dict:
    inputFile = open(inputFilePath, "r")
    return inputFile.read()


def extractToCSV(inputFilePath: str, outputFileName: str, mainClass:str, subClasses) -> None:
    """
    extracting data from html context and transforming data into csv format.
    :param inputFilePath: string (file path)
    :param outputFileName: string (file path)
    :param mainClass: string ( the main class of CSS that should be pulled out)
    :param subClasses: dict {label:CSS class} (assign the sub-classes under main class to extract.)
    :return:
    """

    outputFile = open(outputFileName, "w")
    outputFile_writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    inputFile = open(inputFilePath,"r")
    soup = BeautifulSoup(inputFile.read(), 'html.parser')
    inputFile.close()
    results = soup.findAll(class_=mainClass)
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
    if len(sys.argv) < 3:
        print(f'Error: two more arguments are required- "http address" and "outputFilePath".')
        return
    cssClass = None
    intermediateFile = sys.argv[2]
    if len(sys.argv) >= 4:
        cssClass = sys.argv[3]
    getHtmlFile(sys.argv[1], intermediateFile, cssClass)
    if input(f'Continue to extract data from The file {intermediateFile}? y or n') != "y":
        print("done!")
        return
    outputFileName = input("input the output-File Path:")
    mainClass = input("input the CSS class: ")
    subClasseFile = input("input a file which contains the sub classes in the 'Dict' format of python.")
    subClasses = readOutDict(subClasseFile)
    extractToCSV(intermediateFile, outputFileName,mainClass,subClasses)
    print("Done!")


if __name__ == '__main__':
    main()

