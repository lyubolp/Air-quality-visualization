from src.plotter.plotter import Plotter
from src.enums.enums import Station, Parameter
from datetime import datetime
if __name__ == "__main__":

    print("Press 1 to show single day plot\n"
          "Press 2 to show multiple days plot")
    user_input = input()
    plotter = Plotter("data/data.csv")

    if user_input == '1':
        plotter.plot_single_region_day(Station.Druzhba, Parameter.Temperature, datetime(2017, 1, 21, 0))
    elif user_input == '2':
        plotter.plot_single_region_time_range(Station.Druzhba, Parameter.Temperature,
                                              datetime(2017, 1, 21, 0), datetime(2017, 1, 25, 0))