"""Bus Times."""

import re
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup


# Upper Cambourne bus stop, opposite Lysander Close
URL = "https://bustimes.org/stops/0500SCAMB024"
NUMBER_OF_BUSES = 5

def update_what():
    pass

def update_info():
    """
    Get the 
    """
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'lxml')

    for row in soup.find_all('tr'): #[:NUMBER_OF_BUSES]:
        bus = ' '.join(row.stripped_strings)
        print(re.sub("⚡", ' *', bus))

def update_buses():
    update_info()
    update_what()

if __name__ == "__main__":
    update_buses()
