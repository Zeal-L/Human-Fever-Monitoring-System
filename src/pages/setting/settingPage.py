from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class SettingNode(node.Node):
    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        pass

    def showText(self):
        grove_rgb_lcd.setText_norefresh("Setting Page   \n               \x00")
        
        node.NodeScreen("/home/pi/project/Resource/setting.png", "Settings")
    
    def onButton(self):
        print("did not implement onButton()")
        OledScreen.clear()
        if isinstance(self.pages[self.currentPage], node.Node):
            print("mainPage onButton issubclass")
            OledScreen.clear()
            page.currentPage = self.pages[self.currentPage]
            page.currentPage.currentPage = -1
        
