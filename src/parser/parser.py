from src.enums.enums import Parameter, Station
from datetime import datetime

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def convert_station_list(station: list) -> list:
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

    @staticmethod
    def convert_parameter_list(parameter: list) -> list:
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

    def get(self, stations: list, parameters: list,
            start: datetime = None, end: datetime = None) -> list:
        """
        Given a datetime, a list of stations and a list of parameters
        return the data which matches these parameters for these stations and
        that time
        """
        stations = self.convert_station_list(stations)
        parameters = self.convert_parameter_list(parameters)
        # Filter for stations and parameters
        filtered = [x for x in self.data if x[1] in stations and x[2] in parameters]
        if start is None:
            return filtered
        if end is None:
            end = start
        return [x for x in filtered if start <= x[0] <= end]


