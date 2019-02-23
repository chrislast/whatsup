"""Display useful info on an e-ink display"""
import re
from urllib.request import urlopen
#import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive

from inky import InkyWHAT

def get_background(background_img):
    # Open our image file that was passed in from the command line
    img = Image.open(background_img)

    # Get the width and height of the image
    w, h = img.size

    # Calculate the new height and width of the image
    h_new = 300
    w_new = int((float(w) / h) * h_new)
    w_cropped = 400

    # Resize the image with high-quality resampling
    img = img.resize((w_new, h_new), resample=Image.LANCZOS)

    # Calculate coordinates to crop image to 400 pixels wide
    x0 = (w_new - w_cropped) / 2
    x1 = x0 + w_cropped
    y0 = 0
    y1 = h_new

    # Crop image
    img = img.crop((x0, y0, x1, y1))

    # Convert the image to use a white / black / red colour palette
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    img = img.convert("RGB").quantize(palette=pal_img)

    img.save("out.png")

    return img


def update_buses(img):
    URL = "https://bustimes.org/stops/0500SCAMB024"
    NUMBER_OF_BUSES = 4

    html = urlopen(URL)
    soup = BeautifulSoup(html, "html.parser")

    for row, text in enumerate(soup.find_all('tr')[:NUMBER_OF_BUSES]):
        bus = ' '.join(text.stripped_strings)
        bus = re.sub("⚡", '*', bus)

        # Calculate the positioning and draw the "my name is" text
        hanken_medium_font = ImageFont.truetype(HankenGroteskBold, 16)
        mynameis_w, mynameis_h = hanken_medium_font.getsize(bus)
        mynameis_x = 10
        mynameis_y = 100 + row * 14
        draw.text((mynameis_x, mynameis_y), bus, inky_display.BLACK, font=hanken_medium_font)

def update_bins(img):
    URL = "https://www.scambs.gov.uk/bins/find-your-bin-collection-day/#id=144154"
    html = urlopen(URL)
    soup = BeautifulSoup(html, "html.parser")


    URL="https://refusecalendarapi.azurewebsites.net/collection/search/144154/?numberOfCollections=3"
    html = urlopen(URL)
    if html.code != 200:
	return
    data = json.loads(html.read().decode())




def update_news(img):
    pass
def update_date(img):
    pass
def update_weather(img):
    pass
def update_planner(img):
    pass

# Set up the inky wHAT display and border colour
inky_display = InkyWHAT('red')
inky_display.set_border(inky_display.BLACK)
img = get_background('/home/pi/git/whatsup/whatsupbg.png')
draw = ImageDraw.Draw(img)
scale_size = 2.20
padding = 15

def main():
    """."""

    update_buses(img)
    update_bins(img)
    update_news(img)
    update_date(img)
    update_weather(img)
    update_planner(img)

    # Display the final image on Inky wHAT
    inky_display.set_image(img)
    inky_display.show()

if __name__ == "__main__":
    main()
