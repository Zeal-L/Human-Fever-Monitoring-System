# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)


# Draw an icon
icon = Image.open("/home/pi/project/Resource/temp.png")
icon.thumbnail((width, 20))  # Resize the icon to fit within the screen height
icon_width, icon_height = icon.size
icon_x = 13
icon_y = (height - icon_height) // 2 - 15  # Adjust the value as needed
image.paste(icon, (icon_x, icon_y))

# Draw an icon
icon = Image.open("/home/pi/project/Resource/humid.png")
icon.thumbnail((width, 20))  # Resize the icon to fit within the screen height
icon_width, icon_height = icon.size
icon_x = 10
icon_y = (height - icon_height) // 2 + 15  # Adjust the value as needed
image.paste(icon, (icon_x, icon_y))

# Load a default font
font = ImageFont.load_default()
# change font size
font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)

# Display temperature
temperature = "25°C"  # Replace with the actual temperature value
temperature_width, temperature_height = font.getsize(temperature)
temperature_x = width - temperature_width - 48
temperature_y = (height - temperature_height) // 2 - 15  # Adjust the value as needed
draw.text((temperature_x, temperature_y), temperature, font=font, fill=255)

# Display humidity
humidity = "50%"  # Replace with the actual humidity value
humidity_width, humidity_height = font.getsize(humidity)
humidity_x = width - humidity_width - 50
humidity_y = (height - humidity_height) // 2 + 15  # Adjust the value as needed
draw.text((humidity_x, humidity_y), humidity, font=font, fill=255)

timeNow = time.monotonic_ns()
disp.image(image)
disp.display()   
print("time cost: ", (time.monotonic_ns() - timeNow)/1000000, "ms")