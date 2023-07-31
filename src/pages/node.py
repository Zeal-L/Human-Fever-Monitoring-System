from abc import ABC, abstractmethod
from typing import Optional
from src.pages import page, dynamicPage
from src.hardware import OledScreen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import time
import textwrap

class Node(page.Page):
    def __init__(self):
        self.pages = [self]
        self.currentPage = -1
    
    def onButton(self) -> None:
        if isinstance(self.pages[self.currentPage], dynamicPage.DPage):
            self.pages[self.currentPage].onButton()
        elif isinstance(self.pages[self.currentPage], Node):
            print("mainPage onButton issubclass")
            OledScreen.clear()
            page.currentPage = self.pages[self.currentPage]
            page.currentPage.currentPage = -1
    
    def onRotary(self, rotaryValue: int):
        subAngle = 1024 / len(self.pages)
        index = int(rotaryValue / subAngle)
        index = 0 if index < 0 else index
        index = len(self.pages) - 1 if index >= len(self.pages) else index
        if index != self.currentPage:
            # if self.currentPage == -1:
                self.currentPage = index
                OledScreen.clear()
                self.pages[index].showText()
                return
            
            # if index < self.currentPage:
            #     for i in range(0, 129, 64):
            #         print("i: ", i)
            #         OledScreen.clear()
            #         self.pages[self.currentPage].showText(i)
            #         self.pages[index].showText(i - 128)
            #         OledScreen.disp.image(OledScreen.image)
            #         OledScreen.disp.display()
            # else:
            #     for i in range(0, -129, -64):
            #         print("i: ", i)
            #         OledScreen.clear()
            #         self.pages[self.currentPage].showText(i)
            #         self.pages[index].showText(i + 128)
            #         OledScreen.disp.image(OledScreen.image)
            #         OledScreen.disp.display()
            # self.currentPage = index
                
        elif self.pages[index].showTextChangable():
            self.pages[index].showText()

def NodeScreen(iconPath: str, text: str, offset: int = 0):
    icon = Image.open(iconPath)
    icon.thumbnail((OledScreen.width, OledScreen.height - 20))
    icon_width, icon_height = icon.size
    icon_x = (OledScreen.width - icon_width) // 2
    icon_y = (OledScreen.height - icon_height) // 2 + 10  # Adjust the value as needed
    OledScreen.image.paste(icon, (icon_x - offset, icon_y))
    
    font = ImageFont.load_default()
    text_width, text_height = OledScreen.draw.textsize(text, font=font)
    text_x = (OledScreen.width - text_width) // 2
    text_y = icon_y - text_height - 5  # Adjust the value as needed
    OledScreen.draw.text((text_x - offset, text_y), text, font=font, fill=255)

def ErrorScreen(text: str):
    icon = Image.open("/home/pi/project/Resource/error.png") 
    icon.thumbnail((OledScreen.width // 4, OledScreen.height - 40)) 
    icon_width, icon_height = icon.size
    icon_x = (OledScreen.width - icon_width) // 2
    icon_y = (OledScreen.height - icon_height) // 2 + 10
    OledScreen.image.paste(icon, (icon_x, icon_y))
    font = ImageFont.load_default()
    error_text_lines = textwrap.wrap(text,20)
    text_height = sum(OledScreen.draw.textsize(line, font=font)[1] for line in error_text_lines)
    text_width = max(OledScreen.draw.textsize(line, font=font)[0] for line in error_text_lines)
    text_position = ((OledScreen.width) // 2 - text_width // 2, 0)
    
    for line in error_text_lines:
        text_width, text_height = OledScreen.draw.textsize(line, font=font)
        line_position = (text_position[0], text_position[1])
        OledScreen.draw.text(line_position, line, font=font, fill=1)
        text_position = (text_position[0], text_position[1] + text_height)


def showErrorScreen(text: str):
    OledScreen.clear()
    ErrorScreen(text)
    OledScreen.disp.image(OledScreen.image)
    OledScreen.disp.display()
    time.sleep(1)