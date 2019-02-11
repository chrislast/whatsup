"""Display useful info on an e-ink display"""
from inky import InkyWHAT

from bus_info import update_buses
from cal_info import update_calendar
from bin_info import update_bins
from news_info import update_headlines

inkywhat = InkyWHAT('red')

def update_background():
    pass

def main():
    """."""
    update_background()
    update_buses()
    update_calendar()
    update_bins()
    update_headlines()

if __name__ == "__main__":
    main()