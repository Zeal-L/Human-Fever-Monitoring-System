import time
import grovepi
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo

# 创建一个PiGPIOFactory对象，用于控制舵机
factory = PiGPIOFactory()

servo = AngularServo(18, pin_factory=factory, min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0023)
print(servo.min())  
while True:
    servo.angle = 0
    time.sleep(1)
    servo.angle = 90
    time.sleep(1)
    servo.angle = -90
    time.sleep(1)
    