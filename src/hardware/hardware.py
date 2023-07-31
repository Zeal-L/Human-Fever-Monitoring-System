import time
import grovepi
import math
import grove_rgb_lcd
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from src.storage import readAndWrite
import src.multiprocessHost as MultiprocessHost

# change to class
class Temp_humidity:
    pin = 7
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
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    Temp_humidity.tempValue = temp
                    Temp_humidity.humidityValue = humidity
                    MultiprocessHost.Rtemp.value = temp
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
    pin = 4
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
        # if self.currentAngle +1 == angle or self.currentAngle -1 == angle:
        #     return
        angle = angle if angle <= self.maxAngle else self.maxAngle
        angle = angle if angle >= self.minAngle else self.minAngle
        self.servo.angle = angle
        self.currentAngle = angle
        
        # print("servo angle: ", self.servo.angle)

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
        PTZ.x_servo.setAngle(0)
        PTZ.y_servo.setAngle(0)
        time.sleep(0.5)
        PTZ.x_servo.setAngle(-10)
        PTZ.y_servo.setAngle(-10)
        time.sleep(0.2)   
        PTZ.x_servo.setAngle(10)
        PTZ.y_servo.setAngle(10)
        time.sleep(0.2)
        PTZ.x_servo.setAngle(0)
        PTZ.y_servo.setAngle(0)
        
    
    @staticmethod
    def loadValue():
        pass
    
    @staticmethod
    def setAngle(xAngle, yAngle):
        PTZ.x_servo.setAngle(xAngle)
        PTZ.y_servo.setAngle(yAngle)
        
        # MultiprocessHost.servoX.value = xAngle
        # MultiprocessHost.servoY.value = yAngle
        
    @staticmethod
    def setXAngle(angle):
        PTZ.x_servo.setAngle(angle)
        MultiprocessHost.servoX.value = angle
    
    @staticmethod
    def setYAngle(angle):
        PTZ.y_servo.setAngle(angle)
        MultiprocessHost.servoY.value = angle

class Buzzer:
    BuzzerPin = 6

    @staticmethod
    def setup():
        grovepi.pinMode(Buzzer.BuzzerPin,"OUTPUT")
        time.sleep(1)
    
    @staticmethod
    def start(duration = 0.5):
        grovepi.digitalWrite(Buzzer.BuzzerPin,1)		# Send HIGH to switch on LED
        grovepi.analogWrite(Buzzer.BuzzerPin,200)		# Send PWM signal to LED
        time.sleep(duration)
        grovepi.digitalWrite(Buzzer.BuzzerPin,0)
        
    @staticmethod
    def on():
        grovepi.digitalWrite(Buzzer.BuzzerPin,1)		# Send HIGH to switch on LED
        grovepi.analogWrite(Buzzer.BuzzerPin,200)		# Send PWM signal to LED
        
    @staticmethod
    def off():
        grovepi.digitalWrite(Buzzer.BuzzerPin,0)		# Send HIGH to switch on LED
        
    @staticmethod
    def loadValue():
        pass

from enum import Enum

class backLightType(Enum):
    error = 0
    warning = 1
    normal = 2

class screeBacklight():
    
    backLight = {
        "r": 0,
        "g": 0,
        "b": 0,
        "type": backLightType.normal
    }

    totalCount = 100
    currentCount = 0
    lastTime = time.monotonic_ns()
    frequency = 0.3
    @staticmethod
    def load():
        current = time.monotonic_ns()
        if current - screeBacklight.lastTime > screeBacklight.frequency * 10**9:
            screeBacklight.lastTime = current
            if screeBacklight.currentCount < screeBacklight.totalCount:
                if screeBacklight.backLight["type"] == backLightType.error:
                    if screeBacklight.currentCount % 2 == 0:
                        grove_rgb_lcd.setRGB(255,0,0)
                        Buzzer.on()
                    else:
                        grove_rgb_lcd.setRGB(20,0,0)
                        Buzzer.off()
                elif screeBacklight.backLight["type"] == backLightType.warning:
                    if screeBacklight.currentCount % 2 == 0:
                        grove_rgb_lcd.setRGB(255,255,0)
                    else:
                        grove_rgb_lcd.setRGB(20,20,0)
                else:
                    grove_rgb_lcd.setRGB(screeBacklight.backLight["r"], screeBacklight.backLight["g"], screeBacklight.backLight["b"])
                screeBacklight.currentCount += 1
                