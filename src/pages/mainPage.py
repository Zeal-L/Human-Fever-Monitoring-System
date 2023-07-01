from src.hardware import hardware, grove_rgb_lcd
from src.pages import page,romTempPage,settingPage


class mainPage(page.Page):
    def __init__(self):
        self.pages = [romTempPage.RomTempPage(),settingPage.SettingPage()]
        # reverse the list
        self.pages.reverse()
        pass

    def showText(self) -> None:
        grove_rgb_lcd.setText_norefresh("Main Page")
    
    def onButton(self) -> None:
        print("did not implement onButton()")
    
    def onRotary(self, value: int) -> None:
        subAngle = 1024/len(self.pages)
        for i in range(len(self.pages)):
            if value > subAngle*i and value < subAngle*(i+1):
                print(value,subAngle*i,subAngle*(i+1))
                self.pages[i].showText()
                break