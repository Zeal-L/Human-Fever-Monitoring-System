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
        # grove_rgb_lcd.setText_norefresh("Setting Page   \n               \x00")
        
        icon = Image.open("/home/pi/project/Resource/export.png")
        icon.thumbnail((OledScreen.width, OledScreen.height - 20))
        icon_width, icon_height = icon.size
        icon_x = (OledScreen.width - icon_width) // 2 - 30
        icon_y = (OledScreen.height - icon_height) // 2 - 10
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))
        
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)
        text = "usb1"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = icon_x + icon_width + 5
        text_y = (OledScreen.height - text_height) // 2 - 5
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        
        font = ImageFont.load_default()
        text = "export to USB"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = (OledScreen.width - text_width) // 2
        text_y = icon_y + icon_height + 5  # Adjust the value as needed
        OledScreen.draw.text((text_x-offset, text_y), text, font=font, fill=255)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        