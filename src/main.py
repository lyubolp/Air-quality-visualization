from src.plotter.plotter import Plotter
from src.enums.enums import Station, Parameter
from datetime import datetime
if __name__ == "__main__":
    plotter = Plotter("data/data.csv")
    plotter.plot_single_region_day(Station.Druzhba, Parameter.CO, datetime(2017, 5, 21, 0))
