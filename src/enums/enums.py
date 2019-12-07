"""
Contains the needed enums for using the CSVParser
"""
from enum import IntEnum


class Station(IntEnum):
    """
    Used for selecting the station from which we want the data
    """
    All = -1
    Druzhba = 1
    Nadezhda = 2
    KrasnoSelo = 3
    Pavlovo = 4
    Kopitoto = 5
    Mladost = 6


class Parameter(IntEnum):
    """
    Used for selecting the parameters from the stations
    """
    All = -1
    PM = 0
    NO2 = 1
    NO = 2
    C6H6 = 3
    CO = 4
    O3 = 5
    SO2 = 6
    Humidity = 7
    Pressure = 8
    Wind = 9
    Radiation = 10
    Temperature = 11
