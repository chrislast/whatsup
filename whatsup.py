"""Display useful info on an e-ink display"""
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
import json

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

def show_text(img, txt, x, y, alignment="left", colour=inky_display.BLACK, font=HankenGroteskBold, font_size=16):
    # Calculate the positioning and draw the text
    font = ImageFont.truetype(font, font_size)
    text_w, text_h = font.getsize(txt)
    draw.text((x, y), txt, colour, font=font)

def update_buses(img):
    URL = "https://bustimes.org/stops/0500SCAMB024"
    NUMBER_OF_BUSES = 4

    html = urlopen(URL)
    soup = BeautifulSoup(html, "html.parser")

    for row, text in enumerate(soup.find_all('tr')[:NUMBER_OF_BUSES]):
        bus = ' '.join(text.stripped_strings)
        bus = re.sub("⚡", '*', bus)
        show_text(img, bus, 10, 100 + 15 * row)

def update_bins(img):
    URL="https://refusecalendarapi.azurewebsites.net/collection/search/144154/?numberOfCollections=3"
    html = urlopen(URL)
    if html.code != 200:
    	return
    data = json.loads(html.read().decode())
    collection_day = dict(DOMESTIC="Error", ORGANIC="Error", RECYCLE="Error")
    for event in reversed(data["collections"]):
        date = dateutil.parser.parse(event.date)
        days = dict(0="Mon", 1="Tue", 2="Wed", 3="Thu", 4="Fri", 5="Sat", 6="Sun")
        months = dict(1="Jan", 2="Feb", 3="Mar", 4="Apr", 5="May", 6="Jun",
                      7="Jul", 8="Aug", 9="Sep", 10="Oct", 11="Nov", 12="Dec")
        txt = "%s %d %s %d" % (days[date.weekday], date.day, months[date.month], date.year[-2:])
        for round_type in event["roundTypes"]:
            collection_day[round_type] = txt
    show_text(img, "BLK %s" % collection_day["DOMESTIC"], 50, 200)
    show_text(img, "BLU %s" % collection_day["RECYCLE"], 50, 200)
    show_text(img, "GRN %s" % collection_day["ORGANIC"], 50, 200)


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
