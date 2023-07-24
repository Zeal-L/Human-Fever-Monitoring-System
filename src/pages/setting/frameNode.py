from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from src.storage import readAndWrite
from src.pages.setting import framePage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class FrameNode(node.Node):

    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        self.frame = readAndWrite.ReadAndWrite.getValue("frame")
        self.framePage = framePage.FramePage()
        pass

    def showText(self, offset: int = 0):
        icon = Image.open("/home/pi/project/Resource/frame.png")
        icon.thumbnail((OledScreen.width, OledScreen.height - 20))
        icon_width, icon_height = icon.size
        icon_x = (OledScreen.width - icon_width) // 2 - 30
        icon_y = (OledScreen.height - icon_height) // 2 + 10
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))
        
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)
        text = str(self.frame) + " fps"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = icon_x + icon_width + 5
        text_y = (OledScreen.height - text_height) // 2 + 15
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        
        font = ImageFont.load_default()
        text = "Frame"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = (OledScreen.width - text_width) // 2
        text_y = 5
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
    def onButton(self) -> None:
        OledScreen.clear()
        readAndWrite.ReadAndWrite.setValue("frame", self.framePage.frame)
        self.frame = self.framePage.frame
        page.currentPage = self.pages[0]
        page.currentPage.currentPage = -1

    def onRotary(self, rotaryValue: int):
        print(rotaryValue)
        OledScreen.clear()
        subAngle = 1024 / 20
        index = int(rotaryValue / subAngle) + 1
        self.framePage.frame = index
        self.framePage.showText()
    
        
