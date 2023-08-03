from src.hardware import hardware, OledScreen
from src.pages import node, page, mainPage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
from src.storage import readAndWrite

class LockedPage(node.Node):

    def __init__(self):
        super().__init__()
        self.curretSelect = 0
        self.enteredPassword = 0
        self.curretEnter = ""
        pass

    def showText(self, offset: int = 0):
        OledScreen.clear()
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", size=18)
        digit_width, digit_height = OledScreen.draw.textsize("0", font=font)
        padding = 2

        # text="Enter Old password, 4 digits"
        text = f"Locked, Enter password, 4 digits"
        textF = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", size=9)
        text_width, text_height = OledScreen.draw.textsize(text, font=textF)
        OledScreen.draw.text(((OledScreen.width - text_width) / 2, 0), text, font=textF, fill=255)

        selecter_x = self.curretSelect * (digit_width + padding) + 4
        selecter_y = 6 + text_height
        OledScreen.draw.rectangle((selecter_x, selecter_y, selecter_x + digit_width, selecter_y + digit_height), outline=255)

        # show keyborad
        for i in range(0, 10):
            x = i * (digit_width + padding) + 5
            y = 5 + text_height
            OledScreen.draw.text((x, y), str(i), font=font, fill=255)

        # show entered password as *
        for i in range(0, self.enteredPassword):
            x = i * (digit_width + padding) + 5
            y = selecter_y + digit_height + text_height
            OledScreen.draw.text((x, y), "*", font=font, fill=255)

        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
    
    def getMaxSleepTime(self):
        return 60
    
    def onRotary(self, rotaryValue: int):
        OledScreen.clear()
        subAngle = 1024 / 10
        index = int(rotaryValue / subAngle)
        index = 9 - index
        self.curretSelect = index
        self.showText()
        
        
    def onButton(self) -> None:
        realPassword = readAndWrite.ReadAndWrite.getValue("password")
        self.curretEnter += str(self.curretSelect)
        self.enteredPassword = len(self.curretEnter)
        if self.enteredPassword == 4:
            if self.curretEnter == realPassword:
                self.curretEnter = ""
                self.enteredPassword = 0
                self.curretSelect = 0
                page.currentPage = mainPage.mainPage()
                hardware.screeBacklight.backLight["type"] = hardware.backLightType.normal
            else:
                node.showErrorScreen("password does not match")
        