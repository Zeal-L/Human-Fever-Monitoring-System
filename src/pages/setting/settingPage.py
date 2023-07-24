from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from src.pages.setting import sleepNode, passwordNode, frameNode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class SettingNode(node.Node):
    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode, sleepNode.SleepNode(self), passwordNode.PasswordNode(self), frameNode.FrameNode(self)]
        self.pages.reverse()
        pass

    def showText(self, offset: int = 0):
        
        node.NodeScreen("/home/pi/project/Resource/setting.png", "Settings", offset)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
