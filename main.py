from src.hardware import hardware
from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage
from src.pages import page as page
import src.hardware.OledScreen
import time

hardware.temp_humidity()
hardware.movement()
hardware.RotaryAngle()
buttonValue = hardware.Button()
maxAngle = 1024
subAngle = maxAngle/3
# currPage = mainPage.mainPage()
page.currentPage = mainPage.mainPage()

if __name__ == "__main__":
    while True:
        timeNS = time.time_ns()
        page.currentPage.onRotary(hardware.rotaryAngleValue)
        hardware.temp_humidity()
        hardware.movement()
        hardware.RotaryAngle()
        if hardware.Button():
            page.currentPage.onButton()
            
        print("time Cost: ", (time.time_ns() - timeNS) / 1000000, "ms")