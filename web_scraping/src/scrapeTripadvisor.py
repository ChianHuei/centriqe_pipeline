#!/usr/bin/env python3
"""
scrapeTripadvisor.py is specific for TripAdvisor, pulling data from TripAdvisor and saving it in a csv file.
two arguments are required, which are a file containing URLs  and a outputFilePath.
"""
import requests
from bs4 import BeautifulSoup
import csv
import sys
import json
from extractHTML import getHtmlFile
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


def extractTransformTpd(inputFilePath, outputFilePath):
    """
       extracting data from html context and transforming data into csv format.
       :param inputFilePath: string (file path)
       :param outputFilePath: string (file path) if it is an existing regular file, append at EOF.
       :return:
       """
    if not os.path.isfile(outputFilePath):
        outputFile = open(outputFilePath, "w")
    else:
        outputFile = open(outputFilePath, "a+")
    outputFile_writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    inputFile = open(inputFilePath, "r")
    soup = BeautifulSoup(inputFile.read(), 'html.parser')
    inputFile.close()
    results = soup.findAll(class_="hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H")
    #csvHeader = ["reviewer_name", "from_city","rating", "contributions", "helpful", "text", "stay_date"]

    for result in results:
        r = []

        reviewer_name = result.find(class_="ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC")
        r.append(reviewer_name.text)

        from_city = result.find(class_="default social-member-common-MemberHometown__hometown--3kM9S small")
        if from_city:
            try:
                r.append(from_city.text)
            except:
                r.append("")
        else:
            r.append("")

        bubble = result.find(class_="location-review-review-list-parts-RatingLine__bubbles--GcJvM")

        try:
            string = bubble.find("span").get("class")[1]
            num = string.split("_")[1]
            r.append(int(num))
        except:
            r.append("")

        contributions = result.findAll(class_="social-member-MemberHeaderStats__bold--3z3qh")
        c = []
        try:
            for item in contributions:
                c.append(int(item.text.replace(",", "")))
            while len(c) < 2:
                c.append(0)
            r += c
        except:
            r += [0,0]

        review = result.find(class_="location-review-review-list-parts-ExpandableReview__reviewText--gOmRC")
        if review:
            try:
                r.append(review.text)
            except:
                r.append("")
        else:
            r.append("")

        stay_date = result.find(class_="location-review-review-list-parts-EventDate__event_date--1epHa")
        if stay_date:
            try:
                r.append(stay_date.text.split(": ")[1])
            except:
                r.append("")
        else:
            r.append("")

        outputFile_writer.writerow(r)

    outputFile.close()

def main():
    if len(sys.argv) < 3:
        print(f'Usage: two arguments are required. a file containing URLs, and a outputFilePath')
        return
    firstFilePath = sys.argv[1]
    outputPath = sys.argv[2]

    if not os.path.isfile(firstFilePath):
        print(f'{firstFilePath} is not valid.')
        return

    intermediateFile = "html_main_class.txt"
    f = open(firstFilePath,"r")
    count = 1
    maincl = "hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"
    for address in f:
        if getHtmlFile(address, intermediateFile,maincl):
            extractTransformTpd(intermediateFile, outputPath)
            print(f'page {count} is done.')
            count += 1
    print("All done!")


if __name__ == '__main__':
    main()