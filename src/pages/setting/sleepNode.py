from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from src.pages.setting import sleepPage
from src.storage import readAndWrite
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class SleepNode(node.Node):

    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        self.sleepPage = sleepPage.SleepPage()
        self.sleepTime = readAndWrite.ReadAndWrite.getValue("sleep")
        pass

    def showText(self, offset: int = 0):
        
        icon = Image.open("/home/pi/project/Resource/sleep.png")
        icon.thumbnail((OledScreen.width, OledScreen.height - 20))
        icon_width, icon_height = icon.size
        icon_x = (OledScreen.width - icon_width) // 2 - 30
        icon_y = (OledScreen.height - icon_height) // 2 + 10
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))
        
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)
        text = "off   " if str(self.sleepTime) == "0" else str(self.sleepTime) + " minuts"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = icon_x + icon_width + 5
        text_y = (OledScreen.height - text_height) // 2 + 15
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        
        font = ImageFont.load_default()
        text = "Hibernation"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = (OledScreen.width - text_width) // 2
        text_y = 0
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
    def onButton(self) -> None:
        OledScreen.clear()
        print("sleep time: " + str(self.sleepPage.sleepTime))
        readAndWrite.ReadAndWrite.setValue("sleep", self.sleepPage.sleepTime)
        self.sleepTime = self.sleepPage.sleepTime
        page.currentPage = self.pages[0]
        page.currentPage.currentPage = -1

    def onRotary(self, rotaryValue: int):
        print(rotaryValue)
        OledScreen.clear()
        subAngle = 1024 / self.sleepPage.getMaxSleepTime()
        index = int(rotaryValue / subAngle)
        self.sleepPage.sleepTime = index
        self.sleepPage.showText()
    
        
