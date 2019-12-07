"""
Example usage
`s = json_parser("../data/data.json")`

Get for station Druzhba all parameters, for the time between 2016/1/20 and 2016/1/21

```
r = s.get([Station.Druzhba], [Parameter.All], datetime(2016, 1, 20), datetime(2016, 1, 21))
for i in r:
    print(i)
```

Get for station Kopitoto CO and Temperature data
for the time between 2016/1/20 16 o'clock and 2016/1/20 17 o'clock

```
r = s.get([Station.Kopitoto], [Parameter.CO, Parameter.Pressure],
          datetime(2016, 1, 20, 16), datetime(2016, 1, 20, 17))
for i in r:
    print(i)
```

Get for all stations Pressure data

```
r = s.get([Station.All], [Parameter.Pressure])
for i in r:
    print(i)
```
"""
import json
from datetime import datetime
from src.parser.parser import Parser


class JsonParser(Parser):
    """
    Given a file with JSON, this class will parse the
    file to a json object and will allow queries over this object
    """

    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name
        json_file = open(file_name, "r")
        json_string = json_file.read()
        json_data = json.loads(json_string)
        # remove first row with the titles of the columns
        if len(json_data) >= 1 and json_data[0][0] == "timest":
            json_data = json_data[1:]

        self.data = []
        for i in json_data:
            i[0] = datetime.strptime(i[0][:-6], "%Y-%m-%d %H")  # convert date
            i = i[:-1]  # remove invalid field
            i[1] = int(i[1])  # convert station to int
            i[2] = int(i[2])  # convert param to int
            i[3] = float(i[3])  # convert level to float

            self.data.append(i)
