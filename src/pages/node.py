from abc import ABC, abstractmethod
from typing import Optional
from src.pages import page
from src.hardware import OledScreen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math

class Node(page.Page):
    def __init__(self):
        self.pages = [self]
        self.currentPage = -1
    
    @abstractmethod
    def onButton(self):
        print("did not implement onButton()")
    
    def onRotary(self, rotaryValue: int):
        subAngle = 1024 / len(self.pages)
        index = int(rotaryValue / subAngle)
        # index = math.max(0, index)
        # index = math.min(len(self.pages) - 1, index)
        index = 0 if index < 0 else index
        index = len(self.pages) - 1 if index >= len(self.pages) else index
        if index != self.currentPage:
            OledScreen.clear()
            self.currentPage = index
            print("index: ", index)
            self.pages[index].showText()
        if self.pages[index].showTextChangable():
            self.pages[index].showText()

def NodeScreen(iconPath: str, text: str):
    icon = Image.open(iconPath)
    icon.thumbnail((OledScreen.width, OledScreen.height - 20))
    icon_width, icon_height = icon.size
    icon_x = (OledScreen.width - icon_width) // 2
    icon_y = (OledScreen.height - icon_height) // 2 - 10
    OledScreen.image.paste(icon, (icon_x, icon_y))
    
    font = ImageFont.load_default()
    text_width, text_height = OledScreen.draw.textsize(text, font=font)
    text_x = (OledScreen.width - text_width) // 2
    text_y = icon_y + icon_height + 5  # Adjust the value as needed
    OledScreen.draw.text((text_x, text_y), text, font=font, fill=255)

    OledScreen.disp.image(OledScreen.image)
    OledScreen.disp.display()
