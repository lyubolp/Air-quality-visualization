"""
Holds functions to convert the json data to csv format
"""
import json
from datetime import datetime
import csv


def convert(file_name, output_file):
    """
    Converts a json file containing data to a csv file
    """
    json_file = open(file_name, "r")
    json_string = json_file.read()
    json_data = json.loads(json_string)
    # remove first row with the titles of the columns
    if len(json_data) >= 1 and json_data[0][0] == "timest":
        json_data = json_data[1:]

    data = []
    for i in json_data:
        i[0] = datetime.strptime(i[0][:-6], "%Y-%m-%d %H")  # convert date
        i = i[:-1]  # remove invalid field
        i[1] = int(i[1])  # convert station to int
        i[2] = int(i[2])  # convert param to int
        i[3] = float(i[3])  # convert level to float

        data.append(i)

    with open(output_file, 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(data)


convert("../data/data.json", "../data/data.csv")
