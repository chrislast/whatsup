#!/usr/bin/env python

import argparse
from PIL import Image
from inky import InkyWHAT

print("""Inky wHAT: Dither image

Converts and displays dithered images on Inky wHAT.
""")

# Command line arguments to set display type and colour, and enter your name

parser = argparse.ArgumentParser()
parser.add_argument('--colour', '-c', type=str, required=True, choices=["red", "black", "yellow"], help="ePaper display colour")
parser.add_argument('--image', '-i', type=str, required=True, help="Input image to be converted/displayed")
args = parser.parse_args()

colour = args.colour
img_file = args.image

# Set up the inky wHAT display and border colour

inky_display = InkyWHAT(colour)
inky_display.set_border(inky_display.WHITE)

# Open our image file that was passed in from the command line

img = Image.open(img_file)

pal_img = Image.new("P", (1, 1))
pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

img = img.convert("RGB").quantize(palette=pal_img)

img.save("out.png")

# Display the final image on Inky wHAT
exit()
inky_display.set_image(img)
inky_display.show()
