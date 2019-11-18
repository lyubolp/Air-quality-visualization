from CsvParser import CsvParser
import matplotlib.pyplot as plt
import matplotlib
from Enums import *
from datetime import datetime

parser = CsvParser("../data/data.csv")
result = parser.get([Station.Kopitoto], [Parameter.CO])

dates = []
values = []
for i in result:
	dates.append(i[0])
	values.append(i[3])

# convert the dates to matplotlib format
dates = matplotlib.dates.date2num(dates)
# print(dates)
plt.hlines(100, dates[0], dates[-1]) # the maximum allowed level

# plot all the dots for the dates
plt.plot_date(dates, values, markersize = 3)
# plt.plot(result[3])
plt.show()