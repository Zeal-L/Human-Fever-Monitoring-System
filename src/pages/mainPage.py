from src.pages.setting import settingPage
from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import page, node,romTempPage, faceTempPage, exportNode


class mainPage(node.Node):
    def __init__(self):
        super().__init__()
        self.pages = [exportNode.ExportNode(self),faceTempPage.FaceTempPage(), romTempPage.RomTempPage(),settingPage.SettingNode(self)]
        self.pages.reverse()
        pass


    def showText(self, offset: int = 0) -> None:
        grove_rgb_lcd.setText_norefresh("Main Page")
        node.NodeScreen("/home/pi/project/Resource/home.png", "Home", offset)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
            