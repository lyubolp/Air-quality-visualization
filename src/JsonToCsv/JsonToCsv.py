import json
from datetime import datetime
import csv

def convert(fileName, outputFile):
    jsonFile = open(fileName, "r")
    jsonString = jsonFile.read()
    jsonData = json.loads(jsonString)
    # remove first row with the titles of the columns
    if (len(jsonData) >= 1 and jsonData[0][0] == "timest"):
        jsonData = jsonData[1:]

    data = []
    for i in jsonData:
        i[0] = datetime.strptime(i[0][:-6], "%Y-%m-%d %H") # convert date
        i = i[:-1] # remove invalid field
        i[1] = int(i[1]) # convert station to int
        i[2] = int(i[2]) # convert param to int
        i[3] = float(i[3]) # convert level to float

        data.append(i)

    with open(outputFile, 'w') as writeFile:
    	writer = csv.writer(writeFile)
    	writer.writerows(data)

convert("../data/data.json", "../data/data.csv")