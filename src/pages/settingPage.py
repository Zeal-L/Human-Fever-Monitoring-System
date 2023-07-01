from src.hardware import hardware, grove_rgb_lcd
from src.pages import page

class SettingPage(page.Page):
    def __init__(self):
        print(hardware.tempValue)
        pass

    def showText(self) -> str:
        grove_rgb_lcd.setText_norefresh("Setting Page\n               \x00")
    
    def onButton(self) -> None:
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    def onRotary(self, value: int) -> None:
        # return "did not implement onRotary()"
        print("did not implement onRotary()")
