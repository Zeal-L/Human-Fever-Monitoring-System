from . import Page
# import hardware from subdirectory
import sys 
from .. import hardware, grove_rgb_lcd
# import hardware
# import grove_rgb_lcd

class RomTempPage(Page.Page):
    def __init__(self):
        print(hardware.tempValue)
        pass

    def showText(self) -> str:
        grove_rgb_lcd.setText_norefresh("temp = %.02f C  humidity = %.02f%%"%(hardware.getTempValue(), hardware.getHumidityValue()))
    
    def onButton(self, value: bool) -> None:
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    def onRotary(self, value: int) -> None:
        # return "did not implement onRotary()"
        print("did not implement onRotary()")



