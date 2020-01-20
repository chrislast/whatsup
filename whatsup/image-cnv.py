import argparse
from PIL import Image

def rgb_to_redwhiteblack(img_file):
    """Convert an image to a 3-color palette suitable for InkyWHAT"""

    # Open the input image file
    img = Image.open(img_file)

    # Create a 3-color palette
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    # Convert the image to the 3 color palette
    img = img.convert("RGB").quantize(palette=pal_img)

    return img

if __name__ == "__main__":
# Command line arguments to set display type and colour, and enter your name
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--image', '-i', type=str, required=True, help="Input image to be converted/displayed")
    PARSER.add_argument('--out', '-o', type=str, required=False, help="Output file")
    ARGS = PARSER.parse_args()
    IMG = rgb_to_redwhiteblack(ARGS.image)
    OUT = ARGS.__dict__.get("out", "out.png")
    IMG.save(OUT)
