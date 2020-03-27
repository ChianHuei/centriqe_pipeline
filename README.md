# Documentation
for extractHTML.py, extractAndTransToCSV.py, and pullDataFromWebsite.py
## A. Command Lines

### Extracting data from one web page
1.download the html file

```console
$ ad="https://www.tripadvisor.com/Hotel_Review-g297592-d454351-Reviews-or5-Hotel_Maurya_Patna-Patna_Patna_District_Bihar.html#REVIEWS"

$ python3 extractHTML.py $ad intermediate.txt 
```

2.extract data from the file above

```console
$ mainClass="hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"
$ subClass="ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"

$ python3 extractAndTransToCSV.py intermediate.txt outputFile.csv $mainClass $subClass
```

### Batch-processing
1.prepare a file contains a batch of URL.

for example:

https://www.tripadvisor.com/Hotel_Review-g297592-d454351-Reviews-or5-Hotel_Maurya_Patna-Patna_Patna_District_Bihar.html
https://www.tripadvisor.com/Hotel_Review-g297592-d454351-Reviews-or5-Hotel_Maurya_Patna-Patna_Patna_District_Bihar.html#REVIEWS

2.prepare a file that contains a batch of CSS classes. The format has to be {main_class:{label_1:subClass_, label_2: subClass_2,...}}

for example:

{"hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H":
    {"reviewer_name":"ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC", 
    "text":"location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"}
    }

```console
$ ./pullDataFromWebsite.py address_file.txt classes_file.txt output_file_name.csv
```

## B. Importing python scripts into your code and call the functions


```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys

def getHtmlFile(address: str, outputFileName: str, classToExtract=None) -> bool:
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


```

1.download the html file

For example:


```python
import extractHTML as eh

ad = "https://www.tripadvisor.com/Hotel_Review-g297592-d454351-Reviews-or5-Hotel_Maurya_Patna-Patna_Patna_District_Bihar.html#REVIEWS"
mainClass = "hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"
eh.getHtmlFile(ad, "intermediate.txt",mainClass)
```


```python
#!/usr/bin/env python3


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
```

2.extract data from the file created at step 1

For example:


```python
import extractAndTransToCSV as ea

inputF="intermediate.txt"
outputF="output.csv"
mainCl="hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"
subCl={"reviewer_name":"ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC",
         "text":"location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"}
ea.extractToCSV(inputF, outputF, mainCl, subCl)
```
