from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class PasswordPage(page.Page):

    def __init__(self):
        super().__init__()
        self.curretSelect = 0
        self.enteredPassword = 0
        self.status = 'old'
        pass

    def showText(self, offset: int = 0):
        grove_rgb_lcd.setText_norefresh("Setting Page   \n               \x00")
        OledScreen.clear()
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", size=18)
        digit_width, digit_height = OledScreen.draw.textsize("0", font=font)
        padding = 2

        # text="Enter Old password, 4 digits"
        text = f"Enter {self.status} password, 4 digits"
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
        
