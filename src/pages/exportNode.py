from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from src.pages.setting import sleepNode, passwordNode, frameNode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class ExportNode(node.Node):
    def __init__(self, prevNode: node.Node):
        super().__init__()
        # self.pages = []
        # self.pages.reverse()
        pass

    def showText(self, offset: int = 0):
        
        icon = Image.open("/home/pi/project/Resource/export.png")
        icon.thumbnail((OledScreen.width, OledScreen.height - 20))
        icon_width, icon_height = icon.size
        icon_x = (OledScreen.width - icon_width) // 2 - 30
        icon_y = (OledScreen.height - icon_height) // 2 + 10 
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))
        
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 10)
        text = lsusb()

        max_text_width = OledScreen.width - (icon_x + icon_width + 5 + offset)
        if OledScreen.draw.textsize(text, font=font)[0] > max_text_width:
            while OledScreen.draw.textsize(text + "...", font=font)[0] > max_text_width:
                text = text[:-1]
            text += "..."

        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = icon_x + icon_width + 5
        text_y = (OledScreen.height - text_height) // 2 + 15
        OledScreen.draw.text((text_x - offset, text_y), text, font=font, fill=255)


        font = ImageFont.load_default()
        text = "export to USB"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = (OledScreen.width - text_width) // 2
        text_y = 0
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
def onButton(self) -> None:
    if lsusb() == "Usb not found":
        node.showErrorScreen("Usb not found")
        return

    else:
        node.showErrorScreen("exporting")
        return

def lsusb():
    import os
    for i in os.listdir("/media/pi"):
        return i
    return "Usb not found"