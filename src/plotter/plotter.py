"""
Contains sample code for plotting the data from the stations
"""
import matplotlib.dates
from src.csv_parser import csv_parser, Parameter, Station
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons


class Plotter:
    # 2016-01-20 -> 2018-06-19

    def __init__(self, file_path=None):
        if file_path is None:
            self.parser = None
        else:
            self.parser = csv_parser.CsvParser(file_path)

        self.result = []
        self.station = None
        self.parameter = None
        self.day = None
        self.plot = None
        self.dates = []
        self.values = []
        self.figure = None
        self.axes = None
        self.max_values = {
            Parameter.NO2: 200,
            Parameter.NO: 200,
            Parameter.C6H6: 5,
            Parameter.CO: 10,
            Parameter.O3: 180,
            Parameter.SO2: 350,
            Parameter.Humidity: 60
        }
        self.START_DATE = matplotlib.dates.datestr2num("2016-01-20")
        self.END_DATE = matplotlib.dates.datestr2num("2018-06-19")
        self.spos = None

    def __parse_data_result(self):
        self.dates = []
        self.values = []

        for i in self.result:
            self.dates.append(i[0])
            self.values.append(i[3])

        self.dates = matplotlib.dates.date2num(self.dates)

    def __replot_data(self):
        self.plot.set_xdata(self.dates)
        self.plot.set_ydata(self.values)
        self.figure.canvas.draw_idle()
        self.axes.relim()  # make sure all the data fits
        self.axes.autoscale()  # auto-scale

        # if self.parameter in self.max_values:
        #     plt.hlines(self.max_values[self.parameter], self.dates[0], self.dates[-1])  # the maximum allowed level

    def change_source(self, label):
        if label == 'Дружба':
            self.station = Station.Druzhba
        elif label == 'Копитото':
            self.station = Station.Kopitoto
        elif label == 'Красно село':
            self.station = Station.KrasnoSelo
        elif label == 'Младост':
            self.station = Station.Mladost
        elif label == 'Надежда':
            self.station = Station.Nadezhda
        elif label == 'Павлово':
            self.station = Station.Pavlovo
        elif label == 'Всички':
            pass
        else:
            # Should not be thrown - mainly for debugging purposes
            raise Exception("Invalid label")

        self.result = self.parser.get([self.station], [self.parameter], self.day, self.day + timedelta(days=1))
        self.__parse_data_result()
        self.__replot_data()

    def change_parameter(self, label):
        if label == 'Всички':
            pass
            #self.result = self.parser.get([self.station], [Parameter.All], self.day, self.day + timedelta(days=1))
        elif label == 'PM':
            self.parameter = Parameter.PM
        elif label == 'NO2':
            self.parameter = Parameter.NO2
        elif label == 'NO':
            self.parameter = Parameter.NO
        elif label == 'C6H6':
            self.parameter = Parameter.C6H6
        elif label == 'CO':
            self.parameter = Parameter.CO
        elif label == 'O3':
            self.parameter = Parameter.O3
        elif label == 'SO2':
            self.parameter = Parameter.SO2
        elif label == 'Влажност':
            self.parameter = Parameter.Humidity
        elif label == 'Налягане':
            self.parameter = Parameter.Pressure
        elif label == 'Вятър':
            self.parameter = Parameter.Wind
        elif label == 'Радиация':
            self.parameter = Parameter.Radiation
        elif label == 'Температура':
            self.parameter = Parameter.Temperature
        else:
            # Should not be thrown - mainly for debugging purposes
            raise Exception("Invalid parameter")

        self.result = self.parser.get([self.station], [self.parameter], self.day, self.day + timedelta(days=1))
        self.__parse_data_result()
        self.__replot_data()

    def change_date(self, value):
        self.day = matplotlib.dates.num2date(value, tz=None)
        self.day = self.day.replace(tzinfo=None)
        self.result = self.parser.get([self.station], [self.parameter], self.day, self.day + timedelta(days=1))
        self.spos.valfmt = '{:%Y-%m-%d}'.format(matplotlib.dates.num2date(self.spos.val))
        self.__parse_data_result()
        self.__replot_data()

    def plot_single_region_day(self, region: Station, parameter: Parameter, day: datetime):
        self.station = region
        self.parameter = parameter
        self.day = day
        self.result = self.parser.get([region], [parameter], self.day, self.day + timedelta(days=1))
        self.__parse_data_result()
        self.figure, _ = plt.subplots()

        plt.subplots_adjust(left=0.20, bottom=0.25)
        self.plot, = plt.plot_date(self.dates, self.values, markersize=5)

        # if self.parameter in self.max_values:
        #     plt.hlines(self.max_values[parameter], self.dates[0], self.dates[-1])  # the maximum allowed level

        self.axes = plt.gca()

        axcolor = 'lightgoldenrodyellow'
        axamp = plt.axes([0.25, 0.15, 0.60, 0.03], facecolor=axcolor)
        self.spos = Slider(axamp, 'Дата', self.START_DATE, self.END_DATE, valstep=1)
        self.spos.valfmt = '{:%Y-%m-%d}'.format(matplotlib.dates.num2date(self.spos.val))
        self.spos.on_changed(self.change_date)

        change_station_position = plt.axes([0.025, 0.6, 0.12, 0.25], facecolor=axcolor)

        change_station_button = RadioButtons(change_station_position,
                                             ['Всички', 'Дружба', 'Копитото', 'Красно село',
                                              'Младост', 'Надежда', 'Павлово'],
                                             active=1)
        change_station_button.on_clicked(self.change_source)

        change_parameter_position = plt.axes([0.025, 0.2, 0.12, 0.25], facecolor=axcolor)
        change_parameter_button = RadioButtons(change_parameter_position,
                                               ['Всички', 'PM', 'NO2', 'NO', 'C6H6', 'CO',
                                                'O3', 'SO2', 'Влажност', 'Налягане',
                                                'Вятър', 'Радиация', 'Температура'],
                                               active=12)
        change_parameter_button.on_clicked(self.change_parameter)

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()

        plt.show()

# PARSER = csv_parser.CsvParser("data/data.csv")
# RESULT = PARSER.get([Station.Kopitoto], [Parameter.CO])
#
# DATES = []
# VALUES = []
# for i in RESULT:
#     DATES.append(i[0])
#     VALUES.append(i[3])
#
# # convert the dates to matplotlib format
# DATES = matplotlib.dates.date2num(DATES)
# # print(dates)
# plt.hlines(100, DATES[0], DATES[-1])  # the maximum allowed level
#
# # plot all the dots for the dates
# plt.plot_date(DATES, VALUES, markersize=3)
# # plt.plot(result[3])
# plt.show()
