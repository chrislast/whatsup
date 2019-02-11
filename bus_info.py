"""Bus Times."""

from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

TEMPLATE = f"{bus_number} - {time} {live}"

# Upper Cambourne bus stop, opposite Lysander Close
URL = "https://bustimes.org/stops/0500SCAMB024"

def update_what():
    pass

def update_info():
    """
    Get the 
    """
    html = urlopen(URL)

    soup = BeautifulSoup(html, 'lxml')
    type(soup)

    # Get the title
    title = soup.title
    print(title)

    # Print out the text
    text = soup.get_text()
    #print(soup.text)

    soup.find_all('a')

    all_links = soup.find_all("a")
    for link in all_links:
        print(link.get("href"))


    # Print the first 10 rows for sanity check
    rows = soup.find_all('tr')
    print(rows[:10])

    for row in rows:
        row_td = row.find_all('td')
    print(row_td)
    type(row_td)


    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    print(cleantext)

    import re

    list_rows = []
    for row in rows:
        cells = row.find_all('td')
        str_cells = str(cells)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '',str_cells))
        list_rows.append(clean2)
    print(clean2)
    type(clean2)

    # list_rows[0] = '[\n4\n, Cambourne, \n13:15⚡\n]'

    df = pd.DataFrame(list_rows)
    df.head(10)

    df1 = df[0].str.split(',', expand=True)
    df1.head(10)

    col_labels = soup.find_all('th')

    all_header = []
    col_str = str(col_labels)
    cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
    all_header.append(cleantext2)
    print(all_header)

    df2 = pd.DataFrame(all_header)
    df2.head()

    df3 = df2[0].str.split(',', expand=True)
    df3.head()

    frames = [df3, df1]

    df4 = pd.concat(frames)
    df4.head(10)

    # Below shows how to assign the first row to be the table header
    df5 = df4.rename(columns=df4.iloc[0])
    df5.head()


    df5.info()
    df5.shape


def update_buses():
    update_info()
    update_what()

if __name__ == "__main__":
    update_buses()
