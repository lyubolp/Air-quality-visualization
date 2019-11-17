import json
from datetime import datetime
from Enums import Station, Parameter

class JsonParser:
    """
    Given a file with JSON, this class will parse the
    file to a json object and will allow queries over this object
    """
    def __init__(self, fileName: str):
        self.fileName = fileName
        jsonFile = open(fileName, "r")
        jsonString = jsonFile.read()
        jsonData = json.loads(jsonString)
        # remove first row with the titles of the columns
        if (len(jsonData) >= 1 and jsonData[0][0] == "timest"):
            jsonData = jsonData[1:]

        self.data = []
        for i in jsonData:
            i[0] = datetime.strptime(i[0][:-6], "%Y-%m-%d %H") # convert date
            i = i[:-1] # remove invalid field
            i[1] = int(i[1]) # convert station to int
            i[2] = int(i[2]) # convert param to int
            i[3] = float(i[3]) # convert level to float

            self.data.append(i)
    
    def convertStationList(self, station: list) -> list:
        """
        Convert a list of Station enums to a list of ints
        If the provided list contains invalid objects return empty list
        """
        out = []
        for i in station:
            if isinstance(i, Station):
                out.append(i.value)
            else:
                return []
        
        if -1 in out:
            out = list(map(int, Station))
            out.remove(-1)
        
        return out

    def convertParameterList(self, parameter: list) -> list:
        """
        Convert a list of Parameter enums to a list of ints
        If the provided list contains invalid objects return empty list
        """
        out = []
        for i in parameter:
            if isinstance(i, Parameter):
                out.append(i.value)
            else:
                return []
        
        if -1 in out:
            out = list(map(int, Parameter))
            out.remove(-1)
        
        return out

    def get(self, stations: list, parameters: list, start: datetime = None, end: datetime = None) -> list:
        """
        Given a datetime, a list of stations and a list of parameters
        return the data which matches these parameters for these stations and
        that time
        """
        stations = self.convertStationList(stations)
        parameters = self.convertParameterList(parameters)
        print(parameters)
        # Filter for stations and parameters
        filtered = [x for x in self.data if x[1] in stations and x[2] in parameters]
        
        if (start == None):
            return filtered
        if (end == None):
            end = start

        return [x for x in filtered if x[0] >= start and x[0] <= end]


"Example usage"
s = JsonParser("../data/data_head.json")

"""
Get for station Druzhba all parameters, for the time between 2016/1/20 and 2016/1/21
"""
# r = s.get([Station.Druzhba], [Parameter.All], datetime(2016, 1, 20), datetime(2016, 1, 21))
# for i in r:
#     print(i)

"""
Get for station Kopitoto CO and Temperature data
for the time between 2016/1/20 16 o'clock and 2016/1/20 17 o'clock
"""
# r = s.get([Station.Kopitoto], [Parameter.CO, Parameter.Pressure], datetime(2016, 1, 20, 16), datetime(2016, 1, 20, 17))
# for i in r:
#     print(i)

"""
Get for all stations Pressure data
"""
# r = s.get([Station.All], [Parameter.Pressure])
# for i in r:
#     print(i)
