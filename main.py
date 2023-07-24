from src.hardware import hardware

hardware.Buzzer.start(0.1)

from src.hardware import OledScreen, grove_rgb_lcd

from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage
from src.pages import page as page
from src.camera import camera
import src.multiprocessHost as MultiprocessHost
hardware.Buzzer.start(0.1)

import time

handWares = [hardware.Movement, hardware.RotaryAngle, hardware.Button, hardware.Temp_humidity, hardware.Switch, hardware.ButtonLed, hardware.PTZ ,hardware.Buzzer]

[handWare.setup() for handWare in handWares]

# init complete
hardware.Buzzer.start(0.3)
hardware.Buzzer.start(0.1)

page.currentPage = mainPage.mainPage()

def cleanup():
    print("Performing cleanup tasks...")
    hardware.PTZ.setAngle(0,0)
    OledScreen.clear()
    OledScreen.disp.image(OledScreen.image)
    OledScreen.disp.display()
    grove_rgb_lcd.clearText()
        
timeGap = 0.1 * 10**9
if __name__ == "__main__":
    count = 0
    stoping = False
    process = MultiprocessHost.multiprocessing.Process(target=camera.Camera.run, args=(MultiprocessHost.Rtemp, MultiprocessHost.frame, MultiprocessHost.Ftemp))
    process.start()
    try:
        while True:
            print("Rtemp", MultiprocessHost.Rtemp.value, "frame", MultiprocessHost.frame.value, "Ftemp", MultiprocessHost.Ftemp.value)
            if  hardware.Switch.value:
                stoping = False
                timeNow = time.monotonic_ns()
                [handWare.loadValue() for handWare in handWares]
                page.currentPage.onRotary(hardware.RotaryAngle.value)
                if hardware.Button.value:
                    page.currentPage.onButton()
                timeCost = time.monotonic_ns() - timeNow
                hardware.screeBacklight.load()
                grove_rgb_lcd.setText_norefresh("temp = %.02f C  progress = %.00f%%"%(39, 100))
            else:
                if not stoping:
                    stoping = True
                    cleanup()
                time.sleep(1)
                hardware.Switch.loadValue()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        cleanup()
            