from src.hardware import hardware
from src.pages import romTempPage as romTempPage
from src.pages import mainPage as mainPage

if __name__ == "__main__":
    hardware.temp_humidity()
    hardware.movement()
    hardware.RotaryAngle()
    buttonValue = hardware.Button()
    maxAngle = 1024
    subAngle = maxAngle/3
    currPage = mainPage.mainPage()
    while True:
        # print(hardware.tempValue,hardware.humidityValue)
        # rm = romTempPage.RomTempPage()
        # rm.showText()
        currPage.onRotary(hardware.rotaryAngleValue)
        hardware.temp_humidity()
        hardware.movement()
        hardware.RotaryAngle()
        # start = Switch()
        # screeBacklight()
        
        # if rotaryAngleValue > 0 and rotaryAngleValue < subAngle:
        #     backLight["r"] = 0
        #     backLight["g"] = 255
        #     backLight["b"] = 255
        #     backLight["type"] = backLightType.normal
        #     grove_rgb_lcd.setText_norefresh("temp = %.02f C  humidity =%.02f%%"%(tempValue, humidityValue))
        #     tempValue,humidityValue = temp_humidity()
        # elif rotaryAngleValue > subAngle and rotaryAngleValue < subAngle*2:
        #     backLight["r"] = 0
        #     backLight["g"] = 255
        #     backLight["b"] = 0
        #     backLight["type"] = backLightType.normal
        #     grove_rgb_lcd.setText_norefresh("Is movement: {}".format(isMove))
        #     isMove = movement()
        # elif rotaryAngleValue > subAngle*2 and rotaryAngleValue < maxAngle:
        #     backLight["r"] = 255
        #     backLight["g"] = 255
        #     backLight["b"] = 255
        #     backLight["type"] = backLightType.normal
        #     grove_rgb_lcd.setText_norefresh("button: {}".format(buttonValue))
        #     buttonValue = Button()
        # rotaryAngleValue = RotaryAngle()
        # time.sleep(0.1)