"""Display useful info on an e-ink display"""
import re
from urllib.request import urlopen
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
import json
import dateutil.parser
import dateutil.utils

from bs4 import BeautifulSoup
from inky import InkyWHAT

from birthdays import BIRTHDAYS

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
BIRTHDAYS = {
    (6,12): "Kati",
    (19,9): "Chris",
    (14,4): "Tetley",
    (23,10): "Nana"}

TODAY = dateutil.utils.today()

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

def show_text(img, txt, x, y, alignment="left", colour=InkyWHAT.BLACK, font=HankenGroteskBold, font_size=16):
    # Calculate the positioning and draw the text
    font = ImageFont.truetype(font, font_size)
    text_w, text_h = font.getsize(txt)
    if alignment == "left":
        draw.text((x, y), txt, colour, font=font)
    if alignment == "right":
        draw.text((x - text_w, y), txt, colour, font=font)
    if alignment == "centre":
        draw.text((x - text_w / 2, y), txt, colour, font=font)

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
        date = dateutil.parser.parse(event["date"])
        txt = "%s %d %s" % (DAY[date.weekday()], date.day, MON[date.month])
        for round_type in event["roundTypes"]:
            collection_day[round_type] = txt
    show_text(img, "BLACK", 5, 175)
    show_text(img, collection_day["DOMESTIC"], 65, 175)
    show_text(img, "BLUE", 5, 192)
    show_text(img, collection_day["RECYCLE"], 65, 192)
    show_text(img, "GREEN", 5, 209)
    show_text(img, collection_day["ORGANIC"], 65, 209)


def update_news(img):
    URL="http://feeds.bbci.co.uk/news/rss.xml?edition=uk"
    html = urlopen(URL)
    if html.code != 200:
        show_text(img, "HTML Error %d" % html.code, 75, 250)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("item")
    for row, item in enumerate(items[:6]):
        title = item.find("title").text
        show_text(img, title, 65, 236 + row * 10, font=HankenGroteskMedium, font_size=10)

def update_date(img, test=False):
    if test:
        show_text(img, "Wednesday", 205, 5, font=HankenGroteskBold, font_size=18, alignment="centre")
        show_text(img, "19", 205, 24, colour=InkyWHAT.RED, font=HankenGroteskBold, font_size=36, alignment="centre")
        show_text(img, "September", 205, 55, font=HankenGroteskBold, font_size=16, alignment="centre")
        show_text(img, "1968", 205, 70, font=HankenGroteskBold, font_size=16, alignment="centre")
    else:
        show_text(img, WEEKDAY[TODAY.weekday()], 205, 5, font=HankenGroteskBold, font_size=18, alignment="centre")
        show_text(img, str(TODAY.day), 205, 24, colour=InkyWHAT.RED, font=HankenGroteskBold, font_size=36, alignment="centre")
        show_text(img, MONTH[TODAY.month], 205, 55, font=HankenGroteskBold, font_size=16, alignment="centre")
        show_text(img, str(TODAY.year), 205, 70, font=HankenGroteskBold, font_size=16, alignment="centre")


def update_weather(img):
    #show_text(img, weather["Snow"], 208, 145, font_size=36, colour=InkyWHAT.RED, alignment="centre")
    import bs4, urllib, json
    URL="https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/9409226"
    html = urllib.request.urlopen(URL)
    data = json.loads(html.read().decode())
    forecasts = data["forecasts"]
    location = data["location"]
    draw = ImageDraw.Draw(img)

    # show todays detailed report
    summary_report = forecasts[0]["summary"]["report"] # 'pollenIndex', 'pollenIndexText', 'windDirectionFull', 'gustSpeedMph', 'sunset', 'lowermaxTemperatureF', 'windSpeedMph', 'weatherType', 'pollenIndexIconText', 'mostLikelyLowTemperatureF', 'precipitationProbabilityText', 'precipitationProbabilityInPercent', 'uppermaxTemperatureF', 'lowerminTemperatureF', 'uvIndex', 'uvIndexBand', 'pollutionIndex', 'mostLikelyLowTemperatureC', 'lowerminTemperatureC', 'windDescription', 'localDate', 'pollutionIndexBand', 'maxTempF', 'pollutionIndexIconText', 'upperminTemperatureF', 'upperminTemperatureC', 'windSpeedKph', 'uvIndexText', 'sunrise', 'mostLikelyHighTemperatureC', 'maxTempC', 'pollutionIndexText', 'minTempF', 'minTempC', 'windDirection', 'uvIndexIconText', 'mostLikelyHighTemperatureF', 'lowermaxTemperatureC', 'gustSpeedKph', 'weatherTypeText', 'pollenIndexBand', 'enhancedWeatherDescription', 'uppermaxTemperatureC', 'windDirectionAbbreviation'
    wd = summary_report["windDirectionAbbreviation"] # 'S'
    ws = summary_report["windSpeedMph"] # 7
    sr = summary_report["sunrise"] # '6:56'
    ss = summary_report["sunset"] # '17:32'
    mn = summary_report["minTempC"] # 0
    mx = summary_report["maxTempC"] # 18
    wt = summary_report["weatherTypeText"] # 
    pp = summary_report["precipitationProbabilityInPercent"] # 2
    weather = Image.open("sunny.png","r")
    img.paste(weather, (157,99))
    show_text(img, "Temp: %d-%d°C" % (mn,mx), 208, 157, font_size=14, alignment="centre")
    show_text(img, "Sunrise: %s" % sr, 208, 171, font_size=14, alignment="centre")
    show_text(img, "Sunset: %s" % ss, 208, 185, font_size=14, alignment="centre")
    show_text(img, "Wind: %s %dmph" % (wd, ws), 208, 199, font_size=14, alignment="centre")
    show_text(img, wt, 208, 213, alignment="centre")

    # Show 3 day summary
    for day in (1, 2, 3):
        voffset = (day - 1) * 58
        summary_report = forecasts[day]["summary"]["report"] # 'pollenIndex', 'pollenIndexText', 'windDirectionFull', 'gustSpeedMph', 'sunset', 'lowermaxTemperatureF', 'windSpeedMph', 'weatherType', 'pollenIndexIconText', 'mostLikelyLowTemperatureF', 'precipitationProbabilityText', 'precipitationProbabilityInPercent', 'uppermaxTemperatureF', 'lowerminTemperatureF', 'uvIndex', 'uvIndexBand', 'pollutionIndex', 'mostLikelyLowTemperatureC', 'lowerminTemperatureC', 'windDescription', 'localDate', 'pollutionIndexBand', 'maxTempF', 'pollutionIndexIconText', 'upperminTemperatureF', 'upperminTemperatureC', 'windSpeedKph', 'uvIndexText', 'sunrise', 'mostLikelyHighTemperatureC', 'maxTempC', 'pollutionIndexText', 'minTempF', 'minTempC', 'windDirection', 'uvIndexIconText', 'mostLikelyHighTemperatureF', 'lowermaxTemperatureC', 'gustSpeedKph', 'weatherTypeText', 'pollenIndexBand', 'enhancedWeatherDescription', 'uppermaxTemperatureC', 'windDirectionAbbreviation'
        wd = summary_report["windDirectionAbbreviation"] # 'S'
        ws = summary_report["windSpeedMph"] # 7
        mn = summary_report["minTempC"] # 0
        mx = summary_report["maxTempC"] # 18
        wt = summary_report["weatherTypeText"] # 
        show_text(img, WEEKDAY[(TODAY.weekday()+day)%7], 330, 1+voffset, font=HankenGroteskBold, alignment="centre", colour=InkyWHAT.RED)
        show_text(img, "Temp: %d-%d°C" % (mn,mx), 275, 19+voffset, font_size=14)
        show_text(img, "Wind: %s %d mph" % (wd, ws), 275, 32+voffset, font_size=14)
        show_text(img, wt, 275, 45+voffset, font_size=14)

    # Show 14 day rainfall graph
    origin = [314, 186, 321, 186] # day 1 column at 100 %
    for day in range(14):
        hoffset = day * 6
        summary_report = forecasts[day]["summary"]["report"]
        pp = summary_report["precipitationProbabilityInPercent"]
        bar_height = (100 - pp) // 3
        bar = [origin[0] + hoffset, origin[1], origin[2] + hoffset, origin[3] + bar_height]
        draw.rectangle(bar, fill=InkyWHAT.WHITE)

def update_birthdays(img):
    if (TODAY.day, TODAY.month) in BIRTHDAYS:
        draw = ImageDraw.Draw(img)
        draw.rectangle((0,236,400,300), fill=InkyWHAT.WHITE)
        show_text(img, "Happy Birthday %s!" % BIRTHDAYS[(TODAY.day, TODAY.month)],
            200, 248, font=Intuitive, alignment="centre", colour=InkyWHAT.RED, font_size=40)

def update_cinema(img):
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
    update_birthdays(img)

    # Display the final image on Inky wHAT
    inky_display.set_image(img)
    inky_display.show()

if __name__ == "__main__":
    main()
