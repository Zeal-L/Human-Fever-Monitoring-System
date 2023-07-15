from src.hardware import hardware,OledScreen, grove_rgb_lcd
from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage
from src.pages import page as page
# from src.camera import camera
import time
import _thread

handWares = [hardware.Movement, hardware.RotaryAngle, hardware.Button, hardware.Temp_humidity, hardware.Switch, hardware.ButtonLed, hardware.PTZ]

[handWare.setup() for handWare in handWares]
    
page.currentPage = mainPage.mainPage()

def cleanup():
    print("Performing cleanup tasks...")
    OledScreen.clear()
    OledScreen.disp.image(OledScreen.image)
    OledScreen.disp.display()
    grove_rgb_lcd.clearText()
        
timeGap = 0.1 * 10**9
if __name__ == "__main__":
    # _thread.start_new_thread(camera.Camera.run, ())
    count = 0
    stoping = False
    try:
        while True:
            
            if  hardware.Switch.value:
                stoping = False
                timeNow = time.monotonic_ns()
                [handWare.loadValue() for handWare in handWares]
                page.currentPage.onRotary(hardware.RotaryAngle.value)
                if hardware.Button.value:
                    page.currentPage.onButton()
                timeCost = time.monotonic_ns() - timeNow
                # camera.Camera.run()
                # print("timeCost: ", timeCost/10**9)
            else:
                if not stoping:
                    stoping = True
                    cleanup()
                time.sleep(1)
                hardware.Switch.loadValue()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        cleanup()
            