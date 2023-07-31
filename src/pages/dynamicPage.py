from abc import ABC, abstractmethod
from typing import Optional
from src.pages import page
from src.hardware import OledScreen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import time
import textwrap

class DPage(page.Page):
    def __init__(self):
        self.pages = [self]
        self.currentPage = -1
    
    def onButton(self) -> None:
        pass
    
    def onRotary(self, rotaryValue: int):
        pass
    