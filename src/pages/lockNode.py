from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page, servoPage
from src.pages.setting import sleepPage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class LockNode(node.Node):

    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        self.servoPage = servoPage.ServoPage()
        pass

    def showText(self, offset: int = 0):
        
        node.NodeScreen("/home/pi/project/Resource/lock.png", "Lock", offset)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
    def onButton(self) -> None:
        # OledScreen.clear()
        # page.currentPage = self.pages[0]
        # page.currentPage.currentPage = -1
        pass

    def onRotary(self, rotaryValue: int):
        pass
    
        
