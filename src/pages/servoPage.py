from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class ServoPage(page.Page):

    def __init__(self):
        super().__init__()
        self.angle = hardware.Servo.currentAngle

    def showText(self, offset: int = 0):
        OledScreen.clear()
        icon = Image.open("/home/pi/project/Resource/servo.png")  # Load the icon
        icon.thumbnail((OledScreen.width, OledScreen.height-30))  # Resize the icon to fit within the screen height
        icon_width, icon_height = icon.size
        icon_x = 13
        icon_y = (OledScreen.height - icon_height) // 2  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x, icon_y))

        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)
        
        text = str(self.angle) + "°"
        text_width, text_height = font.getsize(text)
        text_x = OledScreen.width - text_width - 8
        text_y = (OledScreen.height - text_height) // 2
        OledScreen.draw.text((text_x, text_y), text, font=font, fill=255)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
    
    def getMaxSleepTime(self):
        return 60
        
