from src.plotter.plotter import Plotter
from src.enums.enums import Station, Parameter
from datetime import datetime
if __name__ == "__main__":
    plotter = Plotter("data/data.csv")
    plotter.plot_single_region_time_range(Station.Druzhba, Parameter.Temperature,
                                          datetime(2017, 1, 21, 0), datetime(2017, 1, 25, 0))
