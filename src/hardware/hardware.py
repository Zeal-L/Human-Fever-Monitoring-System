import time
import grovepi
import math
import grove_rgb_lcd

# temp_humiditySensor = 4 #put the sensor to D4

# moveSensor = 8 #put the sensor to D8
# grovepi.pinMode(moveSensor,"INPUT")

# RotaryAngleSensor = 2 #put the sensor to A0
# grovepi.pinMode(RotaryAngleSensor,"INPUT")

# buttonSensor = 3 #put the sensor to D2
# grovepi.pinMode(buttonSensor,"INPUT")

# buttonLedSensor = 2 #put the sensor to D2
# grovepi.pinMode(buttonLedSensor,"OUTPUT")

# switchSensor = 7 #put the sensor to D7
# grovepi.pinMode(switchSensor,"INPUT")

# buzzSensor = 6 #put the sensor to D0
# time.sleep(1)

# start = False
# tempValue,humidityValue = 0,0
# isMove = False
# rotaryAngleValue = 0
# ButtonTrigger = False

MAX_ROTARY_ANGLE = 1024
print("hardware init")
# change to class
class Temp_humidity:
    pin = 4
    tempValue = 0
    humidityValue = 0
    lastTime = time.monotonic_ns() - 3 * 10**9
    gapTime = 3 * 10**9
    
    @staticmethod
    def setup():
        pass
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - Temp_humidity.lastTime > Temp_humidity.gapTime:
            try:
                [temp,humidity] = grovepi.dht(Temp_humidity.pin,1)
                print("temp: ", temp, "humidity: ", humidity)
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    Temp_humidity.tempValue = temp
                    Temp_humidity.humidityValue = humidity
                Temp_humidity.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")

class Movement:
    pin = 8
    isMove = False
    
    lastTime = time.monotonic_ns()
    gapTime = 1 * 10**8
    @staticmethod
    def setup():
        grovepi.pinMode(Movement.pin,"INPUT")
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - Movement.lastTime > Movement.gapTime:
            try:
                Movement.isMove = grovepi.digitalRead(Movement.pin) == 1
                Movement.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")

class RotaryAngle:
    pin = 2
    value = 0
    
    lastTime = time.monotonic_ns()
    gapTime = 0
    @staticmethod
    def setup():
        grovepi.pinMode(RotaryAngle.pin,"INPUT")
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - RotaryAngle.lastTime > RotaryAngle.gapTime:
            try:
                RotaryAngle.value = grovepi.analogRead(RotaryAngle.pin)
                RotaryAngle.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")

class ButtonLed:
    pin = 2
    on = False
    @staticmethod
    def setup():
        grovepi.pinMode(ButtonLed.pin,"OUTPUT")
    
    @staticmethod
    def loadValue():
        pass
    
    @staticmethod
    def setOn(on: bool):
        if ButtonLed.on != on:
            ButtonLed.on = on
            print("on" if on else "off")
            grovepi.digitalWrite(ButtonLed.pin, 1 if on else 0)
                
class Button:
    pin = 3
    value = False
    
    lastTime = time.monotonic_ns()
    gapTime = 0
    isButtonPressed = False  
    @staticmethod
    def setup():
        grovepi.pinMode(Button.pin,"INPUT")
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - Button.lastTime > Button.gapTime:
            try:
                isPressed = grovepi.digitalRead(Button.pin) == 0
                if isPressed and not Button.isButtonPressed:
                    Button.isButtonPressed = True
                    Button.value = True
                    ButtonLed.setOn(Button.value)
                elif isPressed and Button.isButtonPressed and Button.value:
                    Button.value = False
                    ButtonLed.setOn(True)
                elif not isPressed:
                    Button.isButtonPressed = False
                    Button.value = False
                    ButtonLed.setOn(Button.value)
                Button.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")
        print("Button: ", Button.value)
                
class Switch:
    pin = 7
    start = False
    
    lastTime = time.monotonic_ns()
    gapTime = 0
    @staticmethod
    def setup():
        grovepi.pinMode(Switch.pin,"INPUT")
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - Switch.lastTime > Switch.gapTime:
            try:
                Switch.start = grovepi.digitalRead(Switch.pin)==1
                Switch.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")




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
