from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class PasswordNode(node.Node):

    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        pass

    def showText(self, offset: int = 0):
        grove_rgb_lcd.setText_norefresh("Setting Page   \n               \x00")
        
        node.NodeScreen("/home/pi/project/Resource/password.png", "Password", offset)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
    def onButton(self) -> None:
        OledScreen.clear()
        page.currentPage = self.pages[0]
        page.currentPage.currentPage = -1

    def onRotary(self, rotaryValue: int):
        pass
    
        
