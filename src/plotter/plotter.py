"""
Contains sample code for plotting the data from the stations
"""
import matplotlib.dates
from src.csv_parser import csv_parser, Parameter, Station
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons


class Plotter:
    def __init__(self, file_path=None):
        if file_path is None:
            self.parser = None
        else:
            self.parser = csv_parser.CsvParser(file_path)

        self.result = []
        self.station = None
        self.parameter = None
        self.start = None
        self.end = None
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
        self.date_slider = None
        self.max_level = None

    def __parse_data_result(self):
        if self.station is not Station.All and self.parameter is not Parameter.All:
            self.dates = []
            self.values = []

            for i in self.result:
                self.dates.append(i[0])
                self.values.append(i[3])

            self.dates = matplotlib.dates.date2num(self.dates)

    def __replot_data(self):
        self.plot.set_xdata(self.dates)
        self.plot.set_ydata(self.values)

        # if self.parameter in self.max_values:
        #     self.max_level.set_visible(True)
        #     horizontal_line = []
        #     for i in range(len(self.dates)):
        #         horizontal_line.append(self.max_values[self.parameter])
        #     self.max_level.set_ydata(horizontal_line)
        # else:
        #     self.max_level.set_ydata(self.values)
        #     self.max_level.set_visible(False)

        self.figure.canvas.draw_idle()
        self.axes.relim()  # make sure all the data fits
        self.axes.autoscale()  # auto-scale

        if len(self.result) is 0:
            self.missing_data_text.set_visible(True)
        else:
            self.missing_data_text.set_visible(False)

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
        else:
            # Should not be thrown - mainly for debugging purposes
            raise Exception("Invalid label")

        self.result = self.parser.get([self.station], [self.parameter], self.start, self.end)
        self.__parse_data_result()
        self.__replot_data()

    def change_parameter(self, label):
        if label == 'PM':
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
        self.result = self.parser.get([self.station], [self.parameter], self.start, self.end)
        self.__parse_data_result()
        self.__replot_data()

    def change_date(self, value):
        self.start = matplotlib.dates.num2date(value, tz=None)
        self.start = self.start.replace(tzinfo=None)
        self.result = self.parser.get([self.station], [self.parameter], self.start, self.start + timedelta(days=1))
        self.date_slider.valfmt = '{:%Y-%m-%d}'.format(matplotlib.dates.num2date(self.date_slider.val))
        self.__parse_data_result()
        self.__replot_data()

    def plot_single_region_day(self, region: Station, parameter: Parameter, day: datetime):
        self.station = region
        self.parameter = parameter
        self.start = day
        self.end = self.start + timedelta(days=1)
        self.result = self.parser.get([region], [parameter], self.start, self.start + timedelta(days=1))

        self.__parse_data_result()
        self.figure, _ = plt.subplots()

        self.missing_data_text = self.figure.text(0.63, 0.07, 'Липсващи данни',
                                                  verticalalignment='bottom', horizontalalignment='right',
                                                  color='red', fontsize=25)

        if len(self.result) is 0:
            self.missing_data_text.set_visible(True)
        else:
            self.missing_data_text.set_visible(False)

        plt.subplots_adjust(left=0.20, bottom=0.25)

        self.plot, = plt.plot_date(self.dates, self.values, markersize=5)
        self.axes = plt.gca()

        # if self.parameter in self.max_values:
        #     horizontal_line = []
        #     for i in range(len(self.dates)):
        #         horizontal_line.append(self.max_values[self.parameter])
        #     self.max_level, = plt.plot(self.dates, horizontal_line, markersize=5)
        # else:
        #     horizontal_line = []
        #     for i in range(len(self.dates)):
        #         horizontal_line.append(self.values[2])
        #     self.max_level, = plt.plot(self.dates, horizontal_line, markersize=5)
        #     self.max_level.set_visible(False)


        axcolor = 'lightgoldenrodyellow'
        axamp = plt.axes([0.25, 0.15, 0.60, 0.03], facecolor=axcolor)
        self.date_slider = Slider(axamp, 'Дата', self.START_DATE, self.END_DATE, valstep=1,
                                  valinit=matplotlib.dates.date2num(self.start))
        self.date_slider.valfmt = '{:%Y-%m-%d}'.format(matplotlib.dates.num2date(self.date_slider.val))
        self.date_slider.on_changed(self.change_date)

        change_station_position = plt.axes([0.025, 0.6, 0.12, 0.25], facecolor=axcolor)
        change_station_button = RadioButtons(change_station_position,
                                             ['Дружба', 'Надежда', 'Красно село',
                                              'Павлово', 'Копитото', 'Младост'],
                                             active=1)

        change_station_button.active = self.station - 1
        change_station_button.on_clicked(self.change_source)

        change_parameter_position = plt.axes([0.025, 0.2, 0.12, 0.25], facecolor=axcolor)
        change_parameter_button = RadioButtons(change_parameter_position,
                                               ['PM', 'NO2', 'NO', 'C6H6', 'CO',
                                                'O3', 'SO2', 'Влажност', 'Налягане',
                                                'Вятър', 'Радиация', 'Температура'],
                                               active=11)

        change_parameter_button.active = self.parameter
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
