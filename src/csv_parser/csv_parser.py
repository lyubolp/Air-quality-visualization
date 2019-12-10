"""
Contains the CsvParser class, used for working with CSV objects
Example usage

`s = csv_parser("../data/data.csv")`

## Get for station Druzhba all parameters, for the time between 2016/1/20 and 2016/1/21
```
r = s.get([Station.Druzhba], [Parameter.All], datetime(2016, 1, 20), datetime(2016, 1, 21))
for i in r:
    print(i)
```

## Get for station Kopitoto CO and Temperature data
## for the time between 2016/1/20 16 o'clock and 2016/1/20 17 o'clock

```
r = s.get([Station.Kopitoto], [Parameter.CO, Parameter.Pressure],
datetime(2016, 1, 20, 16), datetime(2016, 1, 20, 17))
for i in r:
    print(i)
```

## Get for all stations Pressure data

```
r = s.get([Station.All], [Parameter.Pressure])
for i in r:
    print(i)
```
"""
import csv
from datetime import datetime
from src.parser.parser import Parser
import pandas as pd


class CsvParser(Parser):
    """
    Given a file with CSV, this class will parse the
    file to a list
    """

    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name
        self.data = pd.read_csv(file_name, header=None, names=["time", "station", "param", "level"])
        self.data['time'] = pd.to_datetime(self.data['time'])
