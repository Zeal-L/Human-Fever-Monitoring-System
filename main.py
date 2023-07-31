from src.hardware import hardware

hardware.Buzzer.start(0.1)

from src.hardware import OledScreen, grove_rgb_lcd
from src.storage import readAndWrite
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

page.currentPage = mainPage.mainPage()
        
timeGap = 0.1 * 10**9
if __name__ == "__main__":
    count = 0
    stoping = False
    fristStart = True
    process = MultiprocessHost.multiprocessing.Process(target=camera.Camera.run, args=(MultiprocessHost.Rtemp, MultiprocessHost.frame, MultiprocessHost.Ftemp, MultiprocessHost.initComplete,))
    process.start()
    
    

    def cleanup():
        print("Performing cleanup tasks...")
        hardware.PTZ.setAngle(0,0)
        OledScreen.clear()
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        grove_rgb_lcd.clearText()
        # process.terminate()
    
    try:
        while True:
            if MultiprocessHost.initComplete.value:
                if fristStart:
                    hardware.Buzzer.start(0.3)
                    hardware.Buzzer.start(0.1)
                    fristStart = False
                    # process.start()
                # print("Rtemp", MultiprocessHost.Rtemp.value, "frame", MultiprocessHost.frame.value, "Ftemp", MultiprocessHost.Ftemp.value)
                if  hardware.Switch.value:
                    stoping = False
                    timeNow = time.monotonic_ns()
                    [handWare.loadValue() for handWare in handWares]
                    page.currentPage.onRotary(hardware.RotaryAngle.value)
                    if hardware.Button.value:
                        page.currentPage.onButton()
                    timeCost = time.monotonic_ns() - timeNow
                    hardware.screeBacklight.load()
                    totalFrame = MultiprocessHost.frame.value/int(readAndWrite.ReadAndWrite.getValue("frame"))
                    grove_rgb_lcd.setText_norefresh("temp = %.02f C  progress = %.00f%%"%(MultiprocessHost.Ftemp.value, totalFrame*100))
                    # if totalFrame > 1:
                    #     MultiprocessHost.frame.value = 0
                    #     MultiprocessHost.Ftemp.value = 0
                    #     hardware.PTZ.setAngle(0,0)
                else:
                    fristStart = True
                    if not stoping:
                        stoping = True
                        cleanup()
                    time.sleep(0.3)
                    hardware.Switch.loadValue()
            else:
                time.sleep(0.3)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        cleanup()
        # process.stop()
            