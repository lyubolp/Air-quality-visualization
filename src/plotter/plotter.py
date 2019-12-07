"""
Contains sample code for plotting the data from the stations
"""
import matplotlib.pyplot as plt
import matplotlib.dates
from src.csv_parser import csv_parser
from src.enums.enums import Station, Parameter

PARSER = csv_parser.CsvParser("data/data.csv")
RESULT = PARSER.get([Station.Kopitoto], [Parameter.CO])

DATES = []
VALUES = []
for i in RESULT:
    DATES.append(i[0])
    VALUES.append(i[3])

# convert the dates to matplotlib format
DATES = matplotlib.dates.date2num(DATES)
# print(dates)
plt.hlines(100, DATES[0], DATES[-1])  # the maximum allowed level

# plot all the dots for the dates
plt.plot_date(DATES, VALUES, markersize=3)
# plt.plot(result[3])
plt.show()
