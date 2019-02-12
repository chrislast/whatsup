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
    #type(soup)

    # Get the title
    #title = soup.title
    #print(title)

    # Print out the text
    # text = soup.get_text()

    # soup.find_all('a')

    # Print the first 10 rows for sanity check
    #for row in soup.find_all('tr'):
    #    row_td = row.find_all('td')

    #str_cells = str(row_td)
    #cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    #print(cleantext)

    for row in soup.find_all('tr'): #[:NUMBER_OF_BUSES]:
        bus = ' '.join(row.stripped_strings)
        print(re.sub("⚡", ' *', bus))

def update_buses():
    update_info()
    update_what()

if __name__ == "__main__":
    update_buses()
