from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

width = 128
height = 64
    
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
print("OledScreen.py: OledScreen initialized")


def clear():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.display()
    print("OledScreen.py: OledScreen cleared")