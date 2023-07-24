from PIL import Image
from PIL import ImageDraw
# import Adafruit_SSD1306

# from __future__ import division
import logging
import time

import Adafruit_SSD1306

width = 128
height = 64
    
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# # Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# # Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
print("OledScreen.py: OledScreen initialized")


def clear():
    # pass
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    print("OledScreen.py: OledScreen cleared")