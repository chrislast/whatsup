"""Display useful info on an e-ink display"""

# Core packages
import re
import json
from urllib.request import urlopen
import datetime

# External packages
import dateutil.parser
import dateutil.utils
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from bs4 import BeautifulSoup
from inky import InkyWHAT

# Local Packages
from customize import BIRTHDAYS, BUS_TIMES_URL, BACKGROUND
from customize import WEATHER_URL, NEWS_URL, BINS_URL

WEEKDAY = {
    0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
MONTH = {
    1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
    7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
DAY = {
    0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}
MON = {
    1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
    7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

TODAY = dateutil.utils.today()
NOW = datetime.datetime.now()

def get_background(background_img=BACKGROUND):
    """Start with a background image"""
    _img = Image.open(background_img)

    # Check the width and height of the image
    assert img.size == (400, 300), "Background must be 400x300"

    # Convert the image to use a white / black / red colour palette
    # hopefully it already did
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
    _img = _img.convert("RGB").quantize(palette=pal_img)

    return _img

def show_text(txt, x, y, alignment="left", colour=InkyWHAT.BLACK, font=HankenGroteskBold, font_size=16):
    """."""
    # Calculate the positioning and draw the text
    font = ImageFont.truetype(font, font_size)
    text_w, text_h = font.getsize(txt)
    if alignment == "left":
        draw.text((x, y), txt, colour, font=font)
    if alignment == "right":
        draw.text((x - text_w, y), txt, colour, font=font)
    if alignment == "centre":
        draw.text((x - text_w / 2, y), txt, colour, font=font)

def update_buses():
    """."""
    html = urlopen(BUS_TIMES_URL)
    soup = BeautifulSoup(html, "html.parser")

    number_of_buses = 4
    for row, text in enumerate(soup.find_all('tr')[:number_of_buses]):
        bus = ' '.join(text.stripped_strings)
        bus = re.sub("⚡", '*', bus)
        show_text(img, bus, 10, 100 + 15 * row)

def update_bins():
    """."""
    html = urlopen(BINS_URL)
    if html.code != 200:
        return
    data = json.loads(html.read().decode())
    collection_day = dict(DOMESTIC="Error", ORGANIC="Error", RECYCLE="Error")
    for event in reversed(data["collections"]):
        date = dateutil.parser.parse(event["date"])
        txt = "%s %d %s" % (DAY[date.weekday()], date.day, MON[date.month])
        for round_type in event["roundTypes"]:
            collection_day[round_type] = txt
    show_text("BLACK", 5, 175)
    show_text(collection_day["DOMESTIC"], 65, 175)
    show_text("BLUE", 5, 192)
    show_text(collection_day["RECYCLE"], 65, 192)
    show_text("GREEN", 5, 209)
    show_text(collection_day["ORGANIC"], 65, 209)


def update_news():
    """."""
    html = urlopen(NEWS_URL)
    if html.code != 200:
        show_text("HTML Error %d" % html.code, 75, 250)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("item")
    for row, item in enumerate(items[:6]):
        title = item.find("title").text
        show_text(title, 65, 236 + row * 10, font=HankenGroteskMedium, font_size=10)

def update_date():
    """."""
    show_text(WEEKDAY[TODAY.weekday()], 205, 5, font=HankenGroteskBold, font_size=18, alignment="centre")
    show_text(str(TODAY.day), 205, 24, colour=InkyWHAT.RED, font=HankenGroteskBold, font_size=36, alignment="centre")
    show_text(MONTH[TODAY.month], 205, 55, font=HankenGroteskBold, font_size=16, alignment="centre")
    show_text(str(TODAY.year), 205, 70, font=HankenGroteskBold, font_size=16, alignment="centre")


def update_weather():
    """."""
    #show_text(img, weather["Snow"], 208, 145, font_size=36, colour=InkyWHAT.RED, alignment="centre")
    html = urlopen(WEATHER_URL)
    data = json.loads(html.read().decode())
    forecasts = data["forecasts"]
    # location = data["location"]

    # show todays detailed report
    summary_report = forecasts[0]["summary"]["report"] # 'pollenIndex', 'pollenIndexText', 'windDirectionFull', 'gustSpeedMph', 'sunset', 'lowermaxTemperatureF', 'windSpeedMph', 'weatherType', 'pollenIndexIconText', 'mostLikelyLowTemperatureF', 'precipitationProbabilityText', 'precipitationProbabilityInPercent', 'uppermaxTemperatureF', 'lowerminTemperatureF', 'uvIndex', 'uvIndexBand', 'pollutionIndex', 'mostLikelyLowTemperatureC', 'lowerminTemperatureC', 'windDescription', 'localDate', 'pollutionIndexBand', 'maxTempF', 'pollutionIndexIconText', 'upperminTemperatureF', 'upperminTemperatureC', 'windSpeedKph', 'uvIndexText', 'sunrise', 'mostLikelyHighTemperatureC', 'maxTempC', 'pollutionIndexText', 'minTempF', 'minTempC', 'windDirection', 'uvIndexIconText', 'mostLikelyHighTemperatureF', 'lowermaxTemperatureC', 'gustSpeedKph', 'weatherTypeText', 'pollenIndexBand', 'enhancedWeatherDescription', 'uppermaxTemperatureC', 'windDirectionAbbreviation'
    _wd = summary_report["windDirectionAbbreviation"] # 'S'
    _ws = summary_report["windSpeedMph"] # int
    _sr = summary_report["sunrise"] # '6:56'
    _ss = summary_report["sunset"] # '17:32'
    _mn = summary_report["minTempC"] # int
    _mx = summary_report["maxTempC"] # int
    _wt = summary_report["weatherTypeText"] # str
    _pp = summary_report["precipitationProbabilityInPercent"] # int
    weather = Image.open("sunny.png", "r")
    img.paste(weather, (157, 99))
    show_text("Temp: %d-%d°C" % (_mn, _mx), 208, 157, font_size=14, alignment="centre")
    show_text("Sunrise: %s" % _sr, 208, 171, font_size=14, alignment="centre")
    show_text("Sunset: %s" % _ss, 208, 185, font_size=14, alignment="centre")
    show_text("Wind: %s %dmph" % (_wd, _ws), 208, 199, font_size=14, alignment="centre")
    show_text(_wt, 208, 213, alignment="centre")

    # Show 3 day summary
    for day in (1, 2, 3):
        voffset = (day - 1) * 58
        summary_report = forecasts[day]["summary"]["report"] # 'pollenIndex', 'pollenIndexText', 'windDirectionFull', 'gustSpeedMph', 'sunset', 'lowermaxTemperatureF', 'windSpeedMph', 'weatherType', 'pollenIndexIconText', 'mostLikelyLowTemperatureF', 'precipitationProbabilityText', 'precipitationProbabilityInPercent', 'uppermaxTemperatureF', 'lowerminTemperatureF', 'uvIndex', 'uvIndexBand', 'pollutionIndex', 'mostLikelyLowTemperatureC', 'lowerminTemperatureC', 'windDescription', 'localDate', 'pollutionIndexBand', 'maxTempF', 'pollutionIndexIconText', 'upperminTemperatureF', 'upperminTemperatureC', 'windSpeedKph', 'uvIndexText', 'sunrise', 'mostLikelyHighTemperatureC', 'maxTempC', 'pollutionIndexText', 'minTempF', 'minTempC', 'windDirection', 'uvIndexIconText', 'mostLikelyHighTemperatureF', 'lowermaxTemperatureC', 'gustSpeedKph', 'weatherTypeText', 'pollenIndexBand', 'enhancedWeatherDescription', 'uppermaxTemperatureC', 'windDirectionAbbreviation'
        _wd = summary_report["windDirectionAbbreviation"]
        _ws = summary_report["windSpeedMph"]
        _mn = summary_report["minTempC"]
        _mx = summary_report["maxTempC"]
        _wt = summary_report["weatherTypeText"]
        show_text(WEEKDAY[(TODAY.weekday()+day)%7], 330, 1+voffset, font=HankenGroteskBold, alignment="centre", colour=InkyWHAT.RED)
        show_text("Temp: %d-%d°C" % (_mn, _mx), 275, 19+voffset, font_size=14)
        show_text("Wind: %s %d mph" % (_wd, _ws), 275, 32+voffset, font_size=14)
        show_text(_wt, 275, 45+voffset, font_size=14)

    # Show 14 day rainfall graph
    origin = [314, 186, 321, 186] # day 1 column at 100 %
    for day in range(14):
        hoffset = day * 6
        summary_report = forecasts[day]["summary"]["report"]
        ppp = summary_report["precipitationProbabilityInPercent"]
        bar_height = (100 - ppp) // 3
        bar = [origin[0] + hoffset, origin[1], origin[2] + hoffset, origin[3] + bar_height]
        draw.rectangle(bar, fill=InkyWHAT.WHITE)

    # Write the days of the week on X axis of rainfall graph
    wkday = TODAY.weekday()
    wkimg = Image.open("fortnight.png") # 20 * 6px x 7px
    # Crop the correct 14 days from the 20 in the image
    wkimg = wkimg.crop((wkday*6, 0, (wkday+14)*6, 8))
    img.paste(wkimg, (315, 223))


def update_birthdays():
    """."""
    if (TODAY.day, TODAY.month) in BIRTHDAYS:
        draw.rectangle((0, 236, 400, 300), fill=InkyWHAT.WHITE)
        show_text(
            "Happy Birthday %s!" % BIRTHDAYS[(TODAY.day, TODAY.month)],
            200, 248, font=Intuitive, alignment="centre", colour=InkyWHAT.RED, font_size=40)

def main():
    """."""
    update_buses()
    update_bins()
    update_news()
    update_date()
    update_weather()
    update_birthdays()

    # Display the final image on Inky wHAT
    inky_display.set_image()
    inky_display.show()

if __name__ == "__main__":
    # Set up the inky wHAT display and border colour
    inky_display = InkyWHAT('red')
    inky_display.set_border(inky_display.BLACK)

    img = get_background()
    draw = ImageDraw.Draw(img)

    main()
