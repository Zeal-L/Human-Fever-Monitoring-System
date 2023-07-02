from src.pages.setting import settingPage
from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import page, node,romTempPage


class mainPage(node.Node):
    def __init__(self):
        super().__init__()
        self.pages = [romTempPage.RomTempPage(),settingPage.SettingNode(self)]
        self.pages.reverse()
        pass

    
    def showText(self) -> None:
        grove_rgb_lcd.setText_norefresh("Main Page")
        node.NodeScreen("/home/pi/project/Resource/home.png", "Home")
    
    def onButton(self) -> None:
        print("mainPage onButton")
        print(self.currentPage)
        if isinstance(self.pages[self.currentPage], node.Node):
            print("mainPage onButton issubclass")
            OledScreen.clear()
            page.currentPage = self.pages[self.currentPage]
            page.currentPage.currentPage = -1
            