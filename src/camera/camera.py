import time
import cv2
import numpy as np
from src.camera.thermal import Thermal
from src.camera.faceMesh import FaceMeshDetector
from src.camera.rgb_depth import RGB_Depth
from src.hardware import hardware
import math
import datetime as Datetime
# from thermal import Thermal
# from faceMesh import FaceMeshDetector
# from rgb_depth import RGB_Depth


class Camera:
    
    thermal = None
    faceMesh = None
    rgb_depth = None
    
    face_T = 0
    
    isStart = True
    process = None
    
    M = np.array(
        [
            [1.27480916e+00, -3.18284929e-17, 1.11709924e+02],
            [-8.18907323e-17, 1.33566434e+00, -1.08748252e+02],
            [-2.83978552e-19, -0.00000000e+00, 1.00000000e+00],
        ]
    ).astype(np.float32)
        
    @staticmethod
    def setup():
        Camera.thermal = Thermal()
        Camera.faceMesh = FaceMeshDetector()
        Camera.rgb_depth = RGB_Depth()
    
    
    @staticmethod
    def run(Rtemp, frame, Ftemp, initComplete):
        Camera.setup()
        print("Rtemp", Rtemp, "frame", frame, "Ftemp", Ftemp)
        completed = False
        lostTime = time.time()
        while True:
            print("running")
            # print time
            print(Datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            _, thermal_data = Camera.thermal.grab()
            color_image, depth_data = Camera.rgb_depth.grab()
            face_landmarks_list = Camera.faceMesh.grab(color_image)
            if completed == False:
                initComplete.value = True
                completed = True
            aligned_thermal_data = cv2.warpPerspective(
                thermal_data, Camera.M, (color_image.shape[1], color_image.shape[0])
            )
            if face_landmarks_list.__len__() != 0:
                get_angle_offset(face_landmarks_list)
                Camera.face_T = Camera.thermal.get_temperature_depth(aligned_thermal_data, face_landmarks_list, depth_data, Rtemp.value)
                print(f"{Camera.face_T} C")

                # if Camera.face_T > 35:
                #     print("Warning")
                #     _send_email("abc982210694@gmail.com", {"header": "Warning", "body": "The temperature is {:.2f} C".format(Camera.face_T)}, image=color_image)
                currentTemp = Camera.face_T
                averageTemp = Ftemp.value
                averageTemp = averageTemp * frame.value + currentTemp
                averageTemp /= frame.value + 1
                Ftemp.value = averageTemp
                frame.value += 1
                lostTime = time.time()
            else:
                print(time.time()-lostTime)
                if time.time() - lostTime > 5:
                    hardware.PTZ.setAngle(0, 0)
                    Ftemp.value = 0
                    frame.value = 0

import time
from email.header import Header, decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


from email.mime.image import MIMEImage

import cv2
import numpy as np

def _send_email(receiver: str, content: dict, image: np.ndarray) -> None:
    """
    Sends an email to the specified receiver using the SMTP protocol over SSL.

    Args:
        receiver (str): The email address of the receiver.
        content (dict): A dictionary containing the email header and body.
        image (np.ndarray): The image to be attached.

    Returns:
        None
    """
    
    # set up email
    email_address = "a.very.casual.email@gmail.com"
    specific_password = "txweqsodfbjxanme"


    host_server = "smtp.gmail.com"

    msg = MIMEMultipart()
    msg["subject"] = Header(content["header"], "utf_8")
    msg["From"] = email_address
    msg["To"] = Header(receiver, "UTF-8")

    msg.attach(MIMEText(content["body"], "plain", "utf-8"))

    # Convert image to bytes
    _, img_bytes = cv2.imencode('.jpg', image)
    img_bytes = img_bytes.tobytes()
    image = MIMEImage(img_bytes, name="image.jpg")
    msg.attach(image)

    stmp = SMTP_SSL(host_server)

    stmp.login(email_address, specific_password)
    stmp.sendmail(email_address, receiver, msg.as_string())
    stmp.quit()




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
    hardware.PTZ.setAngle(hardware.PTZ.x_servo.getAngle() - angle[0], hardware.PTZ.y_servo.getAngle() - angle[1])
