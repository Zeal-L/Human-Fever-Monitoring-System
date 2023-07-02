from src.pages.setting import settingPage
from src.hardware import hardware, grove_rgb_lcd
from src.pages import page, node,romTempPage


class mainPage(node.Node):
    def __init__(self):
        self.pages = [romTempPage.RomTempPage(),settingPage.SettingNode(self)]
        self.pages.reverse()
        self.currentPage = self.pages[0]
        pass

    
    def showText(self) -> None:
        grove_rgb_lcd.setText_norefresh("Main Page")
    
    def onButton(self) -> None:
        print("mainPage onButton")
        if issubclass(type(self.currentPage), node.Node):
            print("mainPage onButton issubclass")
            page.currentPage = self.currentPage
        
    
    def onRotary(self, rotaryValue: int) -> None:
        subAngle = 1024 / len(self.pages)
        index = int(rotaryValue / subAngle)
        if 0 <= index < len(self.pages):
            print(rotaryValue, subAngle * index, subAngle * (index + 1))
            self.pages[index].showText()
    