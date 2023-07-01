from grove_rgb_lcd import *
import grovepi
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo


# factory = PiGPIOFactory()
# servo = AngularServo(18, pin_factory=factory, min_pulse_width=0.0006, max_pulse_width=0.0023)

setText("Hello world\nLCD test")

# Slowly change the colors every 0.01 seconds.
RGB = {
    "R":255,
    "G":0,
    "B":0
}
keys_lp1 = ["G","B","R"]
keys_lp2 = ["R","G","B"]
totalChange = []
for i in range(0, 3):
    while RGB[keys_lp1[i]] < 255:
        setRGB(RGB["R"],RGB["G"],RGB["B"])
        totalChange.append((RGB["R"],RGB["G"],RGB["B"]))
        time.sleep(0.01)
        RGB[keys_lp1[i]] += 1


    while RGB[keys_lp2[i]] > 0:
        setRGB(RGB["R"],RGB["G"],RGB["B"])
        totalChange.append((RGB["R"],RGB["G"],RGB["B"]))
        time.sleep(0.01)
        RGB[keys_lp2[i]] -= 1
# for i in range(0, 255):
#     totalChange.append((i,i,i))

# print(len(totalChange))


# potentiometer = 0

# grovepi.pinMode(0,"INPUT")

# while True:
#     try:
#         # Read sensor value from potentiometer
#         sensor_value = grovepi.analogRead(0)

#         print("sensor_value = %d" %(sensor_value*(len(totalChange)/1024 if len(totalChange) > 1024 else 1024/len(totalChange))))
#         print(totalChange[sensor_value])
#         setRGB(totalChange[sensor_value][0],totalChange[sensor_value][1],totalChange[sensor_value][2])
#         time.sleep(0.001)
#     except KeyboardInterrupt:
#         break
#     except IOError:
#         print ("Error")