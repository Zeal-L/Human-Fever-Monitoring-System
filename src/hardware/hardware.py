import time
import grovepi
import math
import grove_rgb_lcd

temp_humiditySensor = 4 #put the sensor to D4

moveSensor = 8 #put the sensor to D8
grovepi.pinMode(moveSensor,"INPUT")

RotaryAngleSensor = 2 #put the sensor to A0
grovepi.pinMode(RotaryAngleSensor,"INPUT")

buttonSensor = 3 #put the sensor to D2
grovepi.pinMode(buttonSensor,"INPUT")

buttonLedSensor = 2 #put the sensor to D2
grovepi.pinMode(buttonLedSensor,"OUTPUT")

switchSensor = 7 #put the sensor to D7
grovepi.pinMode(switchSensor,"INPUT")

buzzSensor = 6 #put the sensor to D0
time.sleep(1)

start = False
tempValue,humidityValue = 0,0
isMove = False
rotaryAngleValue = 0
ButtonTrigger = False

MAX_ROTARY_ANGLE = 1024

def getTempValue():
    return tempValue

def getHumidityValue():
    return humidityValue

def temp_humidity():
    global tempValue,humidityValue
    try:
        [temp,humidity] = grovepi.dht(temp_humiditySensor,1)  #put the sensor to D4
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            tempValue = temp
            humidityValue = humidity
            return temp,humidity
    except IOError:
        print ("Error")
    return 0,0


def movement():
    try:
        # return grovepi.digitalRead(moveSensor)==1
        global isMove
        isMove = grovepi.digitalRead(moveSensor) == 1
        return isMove
    except IOError:
        print ("Error")
    return False

def RotaryAngle():
    global rotaryAngleValue
    try:
        rotaryAngleValue = grovepi.analogRead(RotaryAngleSensor)
        return rotaryAngleValue
    except IOError:
        print ("Error")
    return -1
    
def Button():
    global ButtonTrigger
    try:
        ButtonTrigger = grovepi.digitalRead(buttonSensor)==0
        return ButtonTrigger
    except IOError:
        print ("Error")
    return False
        
def Switch():
    global start
    try:
        start = grovepi.digitalRead(switchSensor)==1
        return start
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
