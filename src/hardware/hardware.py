import time
import grovepi
import math
import grove_rgb_lcd
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from src.storage import readAndWrite

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
            # print("on" if on else "off")
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
        # print("Button: ", Button.value)
                
class Switch:
    pin = 7
    value = True
    
    lastTime = time.monotonic_ns()
    gapTime = 0
    @staticmethod
    def setup():
        grovepi.pinMode(Switch.pin,"INPUT")
    
    @staticmethod
    def loadValue():
        if time.monotonic_ns() - Switch.lastTime > Switch.gapTime:
            try:
                Switch.value = grovepi.digitalRead(Switch.pin)==1
                Switch.lastTime = time.monotonic_ns()
            except IOError:
                print ("Error")


class Servo:
    def __init__(self, pin, minAngle, maxAngle):
        self.pin = pin
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.currentAngle = 0
        self.factory = PiGPIOFactory()
        self.servo = AngularServo(self.pin, pin_factory=self.factory, min_pulse_width=0.0006, max_pulse_width=0.0023)
    
    def setAngle(self, angle):
        print("servo angle: ", self.currentAngle)
        if self.currentAngle +1 == angle or self.currentAngle -1 == angle:
            return
        angle = angle if angle <= self.maxAngle else self.maxAngle
        angle = angle if angle >= self.minAngle else self.minAngle
        self.servo.angle = angle
        self.currentAngle = angle
        print("servo angle: ", self.servo.angle)

    def getAngle(self):
        return self.currentAngle
        

class PTZ:
    x_servo_pin = 17
    y_servo_pin = 18
    X_MAX_DEGREE = 180
    Y_MAX_DEGREE = 120
    x_servo = Servo(x_servo_pin, -90, 90)
    y_servo = Servo(y_servo_pin, -40, 80)
    @staticmethod
    def setup():
        # PTZ.currentAngle = int(readAndWrite.ReadAndWrite.getValue("ServoAngle"))
        PTZ.x_servo.setAngle(0)
        PTZ.y_servo.setAngle(0)
        time.sleep(1)
        PTZ.x_servo.setAngle(-90)
        PTZ.y_servo.setAngle(-40)
        time.sleep(1)   
        PTZ.x_servo.setAngle(90)
        PTZ.y_servo.setAngle(80)
        time.sleep(1)
        PTZ.x_servo.setAngle(0)
        PTZ.y_servo.setAngle(0)
        
    
    @staticmethod
    def loadValue():
        pass
    
    @staticmethod
    def setAngle(xAngle, yAngle):
        PTZ.x_servo.setAngle(xAngle)
        PTZ.y_servo.setAngle(yAngle)
        
    @staticmethod
    def setAngle(xAngle):
        PTZ.x_servo.setAngle(xAngle)
        
    @staticmethod
    def setXAngle(angle):
        PTZ.x_servo.setAngle(angle)
    
    @staticmethod
    def setYAngle(angle):
        PTZ.y_servo.setAngle(angle)

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
    backlightCount += 1
