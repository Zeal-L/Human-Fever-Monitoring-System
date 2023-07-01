import time
import grovepi
import math
import grove_rgb_lcd
import _thread

temp_humiditySensor = 4 #put the sensor to D4

moveSensor = 8 #put the sensor to D8
grovepi.pinMode(moveSensor,"INPUT")

RotaryAngleSensor = 2 #put the sensor to A0
grovepi.pinMode(RotaryAngleSensor,"INPUT")

buttonSensor = 2 #put the sensor to D2
grovepi.pinMode(buttonSensor,"INPUT")

switchSensor = 7 #put the sensor to D7
grovepi.pinMode(switchSensor,"INPUT")

time.sleep(1)

start = False

temp = 0
humidity = 0
isMove = False
rotaryAngleValue = 0
ButtonTrigger = False


def temp_humidity():
    try:
        [temp,humidity] = grovepi.dht(temp_humiditySensor,1)  #put the sensor to D4
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            return temp,humidity
    except IOError:
        print ("Error")
    return 0,0


def movement():
    try:
        return grovepi.digitalRead(moveSensor)==1
    except IOError:
        print ("Error")
    return False

def RotaryAngle():
    try:
        return grovepi.analogRead(RotaryAngleSensor)
    except IOError:
        print ("Error")
    return -1
    
def Button():
    try:
        return grovepi.digitalRead(buttonSensor)==1
    except IOError:
        print ("Error")
    return False
        
def Switch():
    try:
        # print(grovepi.digitalRead(switchSensor))
        return grovepi.digitalRead(switchSensor)==1
    except IOError:
        print ("Error")
    return False

from enum import Enum

class backLightType(Enum):
    error = 0
    warning = 1
    normal = 2

backLight = {
    "r": 0,
    "g": 0,
    "b": 0,
    "type": backLightType.normal
}

backlightCount = 0
def screeBacklight():
    global backlightCount
    if start:
        if backLight["type"] == backLightType.error:
            if backlightCount < 2:
                grove_rgb_lcd.setRGB(255,0,0)
            else:
                grove_rgb_lcd.setRGB(20,0,0)
                if backlightCount > 3:
                    backlightCount = 0
        elif backLight["type"] == backLightType.warning:
            if backlightCount < 2:
                grove_rgb_lcd.setRGB(255,255,0)
            else:
                grove_rgb_lcd.setRGB(20,20,0)
                if backlightCount > 3:
                    backlightCount = 0
        else:
            grove_rgb_lcd.setRGB(backLight["r"],backLight["g"],backLight["b"])
    else:
        grove_rgb_lcd.setRGB(0,0,0)
    backlightCount += 1


if __name__ == "__main__":
    tempValue,humidityValue = temp_humidity()
    Ismovement = movement()
    rotaryAngleValue = RotaryAngle()
    buttonValue = Button()
    maxAngle = 1024
    subAngle = maxAngle/3
    
    while True:
        start = Switch()
        screeBacklight()
        if rotaryAngleValue > 0 and rotaryAngleValue < subAngle:
            backLight["r"] = 0
            backLight["g"] = 255
            backLight["b"] = 255
            backLight["type"] = backLightType.normal
            grove_rgb_lcd.setText_norefresh("temp = %.02f C  humidity =%.02f%%"%(tempValue, humidityValue))
            tempValue,humidityValue = temp_humidity()
        elif rotaryAngleValue > subAngle and rotaryAngleValue < subAngle*2:
            backLight["r"] = 0
            backLight["g"] = 255
            backLight["b"] = 0
            backLight["type"] = backLightType.normal
            grove_rgb_lcd.setText_norefresh("Is movement: {}".format(Ismovement))
            Ismovement = movement()
        elif rotaryAngleValue > subAngle*2 and rotaryAngleValue < maxAngle:
            backLight["r"] = 255
            backLight["g"] = 255
            backLight["b"] = 255
            backLight["type"] = backLightType.normal
            grove_rgb_lcd.setText_norefresh("button: {}".format(buttonValue))
            buttonValue = Button()
        rotaryAngleValue = RotaryAngle()
        time.sleep(0.1)
        
    