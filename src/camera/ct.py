import time
import cv2
import numpy as np
from thermal import Thermal
from faceMesh import FaceMeshDetector
from rgb_depth import RGB_Depth
import math
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo

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
        
    def __del__(self):
        print("servo close")

class PTZ:
    x_servo_pin = 17
    y_servo_pin = 18
    X_MAX_DEGREE = 180
    Y_MAX_DEGREE = 120
    x_servo = Servo(x_servo_pin, -90, 90)
    y_servo = Servo(y_servo_pin, -40, 80)
    x_servo.setAngle(0)
    y_servo.setAngle(0)
    time.sleep(0.5)
    x_servo.setAngle(-10)
    y_servo.setAngle(-10)
    time.sleep(0.2)   
    x_servo.setAngle(10)
    y_servo.setAngle(10)
    time.sleep(0.2)
    x_servo.setAngle(0)
    y_servo.setAngle(0)
        
    
    @staticmethod
    def loadValue():
        pass
    
    @staticmethod
    def setAngle(xAngle, yAngle):
        PTZ.x_servo.setAngle(xAngle)
        PTZ.y_servo.setAngle(yAngle)
        
    @staticmethod
    def setXAngle(angle):
        PTZ.x_servo.setAngle(angle)
    
    @staticmethod
    def setYAngle(angle):
        PTZ.y_servo.setAngle(angle)


thermal = Thermal()
faceMesh = FaceMeshDetector()
rgb_depth = RGB_Depth()



def calculate_rotation_angle(m, n):
    
    y = 640
    x = 480
    
    # 中心
    center_x = x / 2
    center_y = y / 2
    

    # diff
    delta_x = m - center_x
    delta_y = n - center_y
    angle_x = math.atan(delta_x/ x)
    angle_y = math.atan(delta_y/ y)
    angle_x = math.degrees(angle_x)/2
    angle_y = math.degrees(angle_y)/2
    if math.fabs(angle_x) < 0.1 or math.fabs(angle_y) < 0.1:
        return [0, 0]

    angle_degrees = [angle_x, angle_y]
    
    return angle_degrees



def get_angle_offset(face_landmarks_list):
    
    # x
    # currentAngle = 
    
    average = [0, 0]  # 使用列表代替元组
    
    for cor in face_landmarks_list:
        average[0] += cor[0]
        average[1] += cor[1]
    
    average[0] /= len(face_landmarks_list) 
    average[1] /= len(face_landmarks_list)
    
    angle = calculate_rotation_angle(average[0], average[1])
    PTZ.setAngle(PTZ.x_servo.getAngle() - angle[0], PTZ.y_servo.getAngle() - angle[1])



faceMesh_img, depth_data = rgb_depth.grab()

thermal_img, thermal_data = thermal.grab()

M = np.array(
    [
        [1.33217993e+00, 2.18203388e-17, 8.67231834e+01],
        [-4.52851026e-17, 1.36744186e+00, -1.19200000e+02],
        [3.34506855e-19, -7.35082361e-36, 1.00000000e00],
    ]
).astype(np.float32)


while True:
    # thermal_img, thermal_data = thermal.grab()

    color_image, depth_data = rgb_depth.grab()

    face_landmarks_list = faceMesh.grab(color_image)

    # 对thermal_img进行透视变换
    # aligned_thermal_img = cv2.warpPerspective(
    #     thermal_img, M, (color_image.shape[1], color_image.shape[0])
    # )

    # aligned_thermal_data = cv2.warpPerspective(
    #     thermal_data, M, (color_image.shape[1], color_image.shape[0])
    # )

    # # 在图像顶部显示最小和最大温度以及帧速率
    # text = "Tmin = {:+.1f} Tmax = {:+.1f} FPS = {:.2f}".format(
    #     thermal.to_celsius(thermal_data.min()),
    #     thermal.to_celsius(thermal_data.max()),
    #     1 / (time.time() - thermal.timer),
    # )

    # cv2.putText(
    #     aligned_thermal_img,
    #     text,
    #     (5, 15),
    #     cv2.FONT_HERSHEY_SIMPLEX,
    #     0.45,
    #     (255, 255, 255),
    #     1,
    # )

    # if face_landmarks_list.__len__() != 0:
    #     T , D = thermal.get_temperature_depth(aligned_thermal_data, face_landmarks_list, depth_data)

    #     cv2.putText(
    #         aligned_thermal_img,
    #         "T={:.1f}, D={:.1f}cm".format(T, D),
    #         (15, 50),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.8,
    #         (0, 0, 255),
    #         2,
    #     )

    # # Overlay thermal_img on faceMesh_img
    # alpha = 0.5
    # overlay = cv2.addWeighted(color_image, alpha, aligned_thermal_img, 1 - alpha, 0)

    # show the image
    # cv2.imshow("overlay", overlay)
    # cv2.imshow("thermal", thermal_img)
    if face_landmarks_list.__len__() != 0:
        get_angle_offset(face_landmarks_list)
    print(color_image.shape)
    cv2.imshow("faceMesh", color_image)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break