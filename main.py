from src.hardware import hardware
from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage
from src.pages import page as page
import src.hardware.OledScreen
import time
import _thread

# hardware.Movement.setup()
# hardware.RotaryAngle.setup()
# hardware.Button.setup()
# hardware.Temp_humidity.setup()
# hardware.Switch.setup()
handWares = [hardware.Movement, hardware.RotaryAngle, hardware.Button, hardware.Temp_humidity, hardware.Switch, hardware.ButtonLed, hardware.Servo]

[handWare.setup() for handWare in handWares]
    
page.currentPage = mainPage.mainPage()

def temp_humidity():
    while True:
        hardware.movement()
timeGap = 0.1 * 10**9
if __name__ == "__main__":
    count = 0
    while True:
        timeNow = time.monotonic_ns()
        [handWare.loadValue() for handWare in handWares]
        page.currentPage.onRotary(hardware.RotaryAngle.value)
        if hardware.Button.value:
            page.currentPage.onButton()
        timeCost = time.monotonic_ns() - timeNow
        print("timeCost: ", timeCost/10**9)
        # if timeCost < timeGap:
        #     time.sleep((timeGap - timeCost) / 10**9)
        
            