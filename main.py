from src.hardware import hardware
from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage
from src.pages import page as page
import src.hardware.OledScreen
import time
import _thread

hardware.temp_humidity()
hardware.movement()
hardware.RotaryAngle()
buttonValue = hardware.Button()
maxAngle = 1024
subAngle = maxAngle/3
# currPage = mainPage.mainPage()
page.currentPage = mainPage.mainPage()

def temp_humidity():
    while True:
        hardware.movement()

if __name__ == "__main__":
    while True:
        hardware.movement()
        hardware.temp_humidity()
        hardware.movement()
        hardware.RotaryAngle()
        page.currentPage.onRotary(hardware.rotaryAngleValue)
        if hardware.Button():
            page.currentPage.onButton()
            