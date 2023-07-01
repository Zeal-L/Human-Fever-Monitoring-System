from src.hardware import hardware, grove_rgb_lcd
from src.pages import page

class RomTempPage(page.Page):
    def __init__(self):
        print(hardware.tempValue)
        pass

    def showText(self) -> str:
        grove_rgb_lcd.setText_norefresh("temp = %.02f C  humidity = %.02f%%"%(hardware.getTempValue(), hardware.getHumidityValue()))
    
    def onButton(self) -> None:
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    def onRotary(self, value: int) -> None:
        # return "did not implement onRotary()"
        print("did not implement onRotary()")
