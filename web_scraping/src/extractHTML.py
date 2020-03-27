#!/usr/bin/env python3

"""
extractHTML.py is to pull HTML contents out from a web-page.
"""
import requests
from bs4 import BeautifulSoup
import sys

def getHtmlFile(address: str, outputFileName: str, classToExtract=None) -> bool:
    """
    scraping html context down from internet and opening a new file to store it.
    Caution: if the outputFileName exists, the old file will be replaced.
    :param address: string (URL)
    :param outputFileName: string (file path)
    :param classToExtract: string (assign the class name of CSS that should be extracted.
                                   The default is to scrape all html tags.)
    """
    res = requests.get(address)
    if res.status_code != requests.codes.ok:
        print(f'Request of {address} failed with status code: {res.status_code}.')
        return False

    if classToExtract:
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.findAll(class_=classToExtract)
        content = str(results)
    else:
        content = res.text

    outputFile = open(outputFileName,"w")
    outputFile.write(content)
    outputFile.close()
    return True

def main():
    if len(sys.argv) < 3:
        print(f'Error: two more arguments are required- URL and "outputFilePath".')
        return
    cssClass = None
    intermediateFile = sys.argv[2]
    if len(sys.argv) >= 4:
        cssClass = sys.argv[3]
    getHtmlFile(sys.argv[1], intermediateFile, cssClass)


if __name__ == '__main__':
    main()

